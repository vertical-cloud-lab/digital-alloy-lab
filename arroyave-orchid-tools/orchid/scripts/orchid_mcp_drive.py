#!/usr/bin/env python3
"""Drive the orchid-mcp stdio server over raw JSON-RPC (initialize, tools/list, tools/call).

Usage (run inside the scrubbed environment wrapper, data paths as arguments):

  /tmp/sbx/clean <venv>/bin/python orchid_mcp_drive.py \
      --server "<venv>/bin/orchid-mcp [--fallback]" --label fallback \
      --data-dir <orchid-data checkout> --site-dir <orchid-project.org>/data \
      --cache-dir <scratch dir> --out <results>/data --log <results>/logs/x.log

The server is started with ORCHID_DATA_DIR, ORCHID_SITE_DATA_DIR and ORCHID_OFFLINE=1, so no network is used.
Every request has its own timeout. Each response is saved trimmed (long lists cut, long strings shortened) plus
a per-call timing table; summary numbers (invariant counts, literature matches per SGTE assessment) are computed
from the untrimmed payloads.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import queue
import shlex
import statistics
import subprocess
import sys
import threading
import time
from pathlib import Path

SYSTEMS = ["Al-Cu", "Al-Si", "Al-Mg", "Al-Zr", "Cu-Ni"]
# (element, mole fraction of that element, T in K, what a reader of the accepted diagram expects there)
POINTS = {
    "Al-Cu": [("Cu", 0.02, 800.0, "FCC_A1 (Al-rich solid solution)"),
              ("Cu", 0.33, 700.0, "AL2CU (theta) or theta + neighbour")],
    "Al-Si": [("Si", 0.10, 800.0, "FCC_A1 + DIAMOND_A4 (below the 850 K eutectic)"),
              ("Si", 0.126, 900.0, "LIQUID (above the eutectic)")],
    "Al-Mg": [("Mg", 0.05, 700.0, "FCC_A1")],
    "Al-Zr": [("Zr", 0.25, 1000.0, "AL3ZR (D0_23)"),
              ("Zr", 0.002, 900.0, "FCC_A1 + AL3ZR")],
    "Cu-Ni": [("Ni", 0.30, 1000.0, "FCC_A1 (isomorphous)"),
              ("Ni", 0.50, 1650.0, "LIQUID")],
}
FORMULAS = ["Al2Cu", "Al3Zr", "Al3Mg2"]
TIMEOUT = 120.0
REDACT = {"citation", "assessment_citation"}


class Client:
    def __init__(self, cmd: list[str], env: dict[str, str], stderr_path: Path):
        self.stderr_f = open(stderr_path, "w")
        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=self.stderr_f,
                                     text=True, env=env, bufsize=1)
        self.q: queue.Queue = queue.Queue()
        self.other: list[dict] = []
        threading.Thread(target=self._reader, daemon=True).start()
        self.next_id = 1

    def _reader(self) -> None:
        for line in self.proc.stdout:  # type: ignore[union-attr]
            line = line.strip()
            if line:
                self.q.put(line)
        self.q.put(None)

    def notify(self, method: str, params: dict | None = None) -> None:
        msg = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            msg["params"] = params
        self.proc.stdin.write(json.dumps(msg) + "\n")  # type: ignore[union-attr]
        self.proc.stdin.flush()  # type: ignore[union-attr]

    def request(self, method: str, params: dict | None = None, timeout: float = TIMEOUT) -> tuple[dict, float, int]:
        mid = self.next_id
        self.next_id += 1
        t0 = time.perf_counter()
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}}) + "\n")  # type: ignore[union-attr]
        self.proc.stdin.flush()  # type: ignore[union-attr]
        deadline = t0 + timeout
        while True:
            left = deadline - time.perf_counter()
            if left <= 0:
                raise TimeoutError(f"{method} id={mid}: no response within {timeout:.0f} s")
            try:
                line = self.q.get(timeout=left)
            except queue.Empty:
                continue
            if line is None:
                raise RuntimeError(f"{method} id={mid}: server closed stdout (exit {self.proc.poll()})")
            msg = json.loads(line)
            if msg.get("id") == mid:
                return msg, time.perf_counter() - t0, len(line.encode())
            self.other.append(msg)  # notifications or stray messages

    def close(self) -> int | None:
        try:
            self.proc.stdin.close()  # type: ignore[union-attr]
            self.proc.wait(timeout=15)
        except Exception:
            self.proc.kill()
        self.stderr_f.close()
        return self.proc.returncode


def trim(obj, max_list: int = 5, max_str: int = 240, depth: int = 0):
    """Shorten a JSON payload for saving: lists cut to max_list items (count recorded), strings shortened."""
    if isinstance(obj, dict):
        # citation strings carry author lists; the saved copies keep the DOI fields and drop the names
        return {k: ("[citation text omitted in this copy; see the doi field]" if k in REDACT and isinstance(v, str)
                    else trim(v, max_list, max_str, depth + 1)) for k, v in obj.items()}
    if isinstance(obj, list):
        out = [trim(v, max_list, max_str, depth + 1) for v in obj[:max_list]]
        if len(obj) > max_list:
            out.append(f"... {len(obj) - max_list} more items trimmed (of {len(obj)})")
        return out
    if isinstance(obj, str) and len(obj) > max_str:
        return obj[:max_str] + f"... [{len(obj)} chars]"
    return obj


def parse_result(msg: dict):
    """Return (is_error, payload_or_text, error_text)."""
    if "error" in msg:
        return True, None, json.dumps(msg["error"])
    res = msg.get("result") or {}
    content = res.get("content") or []
    text = content[0].get("text") if content and isinstance(content[0], dict) else None
    payload = None
    if text is not None:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = text
    elif "structuredContent" in res:
        payload = res["structuredContent"]
    if res.get("isError"):
        return True, payload, text if isinstance(text, str) else json.dumps(payload)
    return False, payload, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--server", required=True, help="server command line, e.g. '<venv>/bin/orchid-mcp --fallback'")
    ap.add_argument("--label", required=True)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--site-dir", required=True)
    ap.add_argument("--cache-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--save-trimmed", action="store_true", help="write trimmed per-system responses")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = open(a.log, "w")

    def say(*parts):
        s = " ".join(str(p) for p in parts)
        print(s, flush=True)
        log.write(s + "\n")
        log.flush()

    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR") if k in os.environ}
    env.update({"ORCHID_DATA_DIR": a.data_dir, "ORCHID_SITE_DATA_DIR": a.site_dir, "ORCHID_OFFLINE": "1",
                "ORCHID_CACHE_DIR": a.cache_dir, "XDG_CACHE_HOME": a.cache_dir, "PYTHONUNBUFFERED": "1"})
    cmd = shlex.split(a.server)
    say(f"[{a.label}] server: {' '.join(Path(c).name if '/' in c else c for c in cmd)}  (ORCHID_OFFLINE=1)")
    t_start = time.perf_counter()
    cl = Client(cmd, env, Path(a.log).with_suffix(".stderr.log"))
    rows: list[dict] = []
    payloads: dict[str, object] = {}

    def call(tag: str, method: str, params: dict | None = None):
        try:
            msg, dt, nbytes = cl.request(method, params)
        except Exception as e:  # timeout or crash
            say(f"  {tag:<55} EXCEPTION {type(e).__name__}: {e}")
            rows.append({"label": a.label, "tag": tag, "method": method, "seconds": None, "bytes": None,
                         "is_error": True, "error": f"{type(e).__name__}: {e}"})
            return None
        if method == "tools/call":
            is_err, payload, err = parse_result(msg)
        else:
            is_err, payload, err = ("error" in msg), msg.get("result"), (json.dumps(msg.get("error")) if "error" in msg else None)
        rows.append({"label": a.label, "tag": tag, "method": method, "seconds": round(dt, 4), "bytes": nbytes,
                     "is_error": is_err, "error": err})
        payloads[tag] = payload
        say(f"  {tag:<55} {dt*1000:8.1f} ms {nbytes:>9} B {'ERROR: ' + str(err)[:300] if is_err else 'ok'}")
        return payload

    init = call("initialize", "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                             "clientInfo": {"name": "orchid-mcp-driver", "version": "0"}})
    if init is None:
        cl.close()
        return 2
    say(f"  serverInfo={init.get('serverInfo')} protocolVersion={init.get('protocolVersion')}")
    cl.notify("notifications/initialized")
    tl = call("tools/list", "tools/list")
    tools = {t["name"]: t for t in (tl or {}).get("tools", [])}
    say(f"  tools ({len(tools)}): {sorted(tools)}")

    def tool(tag: str, name: str, args: dict):
        if name not in tools:
            say(f"  {tag}: tool {name} not advertised by tools/list")
            rows.append({"label": a.label, "tag": tag, "method": name, "seconds": None, "bytes": None,
                         "is_error": True, "error": "tool not advertised"})
            return None
        return call(tag, "tools/call", {"name": name, "arguments": args})

    summary: dict[str, dict] = {}
    for system in SYSTEMS:
        A, B = system.split("-")
        s: dict = {"system": system}
        inv = tool(f"{system}/get_invariant_reactions(both)", "get_invariant_reactions",
                   {"system": system, "source": "both", "limit": 200})
        if isinstance(inv, dict):
            s["system_id"] = inv.get("system")
            s["literature_invariants_accepted"] = inv.get("literature_total")
            ev = {}
            for r in inv.get("literature") or []:
                ev[r.get("evidence_class")] = ev.get(r.get("evidence_class"), 0) + 1
            s["literature_invariants_by_evidence_class_first_page"] = ev
            calc = []
            for c in inv.get("calculated") or []:
                invs = c.get("invariants") or []
                matched = [i for i in invs if i.get("literature_matches")]
                best = [abs(i["literature_matches"][0]["dT_K"]) for i in matched]
                best_exp = []
                for i in invs:
                    ex = [m for m in i.get("literature_matches") or [] if m.get("evidence_class") == "experimental"]
                    if ex:
                        best_exp.append(min(abs(m["dT_K"]) for m in ex))
                calc.append({
                    "tdb": c.get("tdb"),
                    "assessment_doi": c.get("assessment_doi"),
                    "n_invariants_calc": len(invs),
                    "n_invariants_raw": c.get("n_invariants_raw"),
                    "n_with_literature_match": len(matched),
                    "median_abs_dT_best_match_K": round(statistics.median(best), 2) if best else None,
                    "n_with_experimental_match": len(best_exp),
                    "n_experimental_within_10K": sum(1 for d in best_exp if d <= 10),
                    "median_abs_dT_best_experimental_K": round(statistics.median(best_exp), 2) if best_exp else None,
                })
            s["sgte_assessments"] = calc
        pd = tool(f"{system}/get_phase_diagram", "get_phase_diagram", {"system": system})
        first_tdb = None
        if isinstance(pd, dict):
            s["n_calculated_diagrams"] = pd.get("n_assessments")
            s["diagram_tdbs"] = [x.get("tdb") for x in pd.get("assessments") or []]
            s["diagram_x_component"] = sorted({str(x.get("x_component")) for x in pd.get("assessments") or []})
            s["diagram_status"] = sorted({str(x.get("status")) for x in pd.get("assessments") or []})
            first_tdb = (pd.get("assessments") or [{}])[0].get("tdb")
        pts = []
        for el, xel, T, expect in POINTS.get(system, []):
            xcomp = (s.get("diagram_x_component") or ["?"])[0].upper()
            x = xel if xcomp == el.upper() else (1.0 - xel if xcomp in (A.upper(), B.upper()) else xel)
            p = tool(f"{system}/get_phase_diagram(x_{el}={xel},T={T:g})", "get_phase_diagram",
                     {"system": system, "x": x, "T": T})
            if isinstance(p, dict):
                for asmt in p.get("assessments") or []:
                    pa = asmt.get("phase_at") or {}
                    pts.append({"tdb": asmt.get("tdb"), "element": el, "x_element": xel, "T_K": T,
                                "x_component": pa.get("x_component"), "x_sent": x, "grid_x": pa.get("grid_x"),
                                "grid_T_K": pa.get("grid_T_K"), "stable_phases": pa.get("stable_phases"),
                                "error": pa.get("error"), "expected": expect})
        s["phase_at_points"] = pts
        lt = tool(f"{system}/list_tdb_files([{A},{B}])", "list_tdb_files", {"elements": [A, B]})
        lte = tool(f"{system}/list_tdb_files([{A},{B}],exact)", "list_tdb_files", {"elements": [A, B], "exact": True})
        for key, val in (("tdb_files_containing", lt), ("tdb_files_exact", lte)):
            if isinstance(val, dict):
                files = val.get("files") or val.get("results") or val.get("tdb_files") or []
                s[key] = {"total": val.get("total"), "returned": len(files),
                          "tiers": sorted({str(f.get("tier")) for f in files if isinstance(f, dict)}),
                          "names": [f.get("file") or f.get("name") for f in files if isinstance(f, dict)][:60]}
        dft = tool(f"{system}/compare_to_dft", "compare_to_dft", {"system": system})
        if isinstance(dft, dict):
            s["compare_to_dft_keys"] = sorted(dft)
        summary[system] = s
        if a.save_trimmed:
            dump = {"system": system, "server": a.label, "note": "trimmed: lists cut to 5 items, strings to 240 chars; payloads identical between the SDK and fallback servers",
                    "responses": {k: trim(v) for k, v in payloads.items() if k.startswith(system + "/")}}
            (out / f"mcp_{system.replace('-', '').lower()}_responses.json").write_text(json.dumps(dump, indent=1, ensure_ascii=False))

    fe: dict[str, dict] = {}
    for f in FORMULAS:
        r = tool(f"get_formation_enthalpy({f})", "get_formation_enthalpy", {"formula": f})
        if isinstance(r, dict):
            fe[f] = {k: r.get(k) for k in ("formula", "composition", "systems", "summary", "summaries", "n_literature")
                     if k in r}
            fe[f]["keys"] = sorted(r)
    tdb_all = tool("list_tdb_files(all)", "list_tdb_files", {"limit": 1})
    srch = tool("search_systems([Al])", "search_systems", {"elements": ["Al"], "limit": 200})
    srch_cu = tool("search_systems([Cu])", "search_systems", {"elements": ["Cu"], "limit": 200})
    bad = tool("error-probe/get_phase_diagram(bad assessment)", "get_phase_diagram",
               {"system": "Al-Cu", "assessment": "no-such-assessment"})
    rc = cl.close()
    total = time.perf_counter() - t_start
    say(f"[{a.label}] server exit code {rc}; wall {total:.2f} s; stray messages {len(cl.other)}")

    if a.save_trimmed:
        misc = {"server": a.label,
                "get_formation_enthalpy": {f: trim(payloads.get(f"get_formation_enthalpy({f})"), 6, 300) for f in FORMULAS},
                "list_tdb_files_all_first": trim(tdb_all, 3),
                "search_systems_Al": trim(srch, 40, 200),
                "search_systems_Cu": trim(srch_cu, 40, 200),
                "error_probe": payloads.get("error-probe/get_phase_diagram(bad assessment)"),
                "tools_list": [{"name": t["name"], "required": t.get("inputSchema", {}).get("required"),
                                "params": sorted(t.get("inputSchema", {}).get("properties", {}))} for t in tools.values()],
                "initialize": trim(init, 8, 400)}
        (out / "mcp_misc_responses.json").write_text(json.dumps(misc, indent=1, ensure_ascii=False))
    (out / f"mcp_summary_{a.label}.json").write_text(json.dumps({"server": a.label, "wall_s": round(total, 3),
                                                                "systems": summary, "formation_enthalpy": fe},
                                                               indent=1, ensure_ascii=False))
    with open(out / f"mcp_call_timings_{a.label}.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["label", "tag", "method", "seconds", "bytes", "is_error", "error"])
        w.writeheader()
        w.writerows(rows)
    # content hashes to compare the fallback and SDK servers
    hashes = {k: hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()[:16]
              for k, v in payloads.items() if k not in ("initialize", "tools/list")}
    (Path(a.log).with_suffix(".hashes.json")).write_text(json.dumps(hashes, indent=1))
    n_err = sum(1 for r in rows if r["is_error"])
    say(f"[{a.label}] calls {len(rows)}, errors {n_err}")
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
