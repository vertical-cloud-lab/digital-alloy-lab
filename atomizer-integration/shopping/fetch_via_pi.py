#!/usr/bin/env python3
"""Fetch a web page through a lab Raspberry Pi, so the request leaves from the Pi's campus connection.

It runs curl on the Pi over Tailscale SSH and writes the page to a local file. Nothing is written on the Pi.
The Pi is chosen by environment-variable *names* (default ``CUBXL_PI``, i.e. ``CUBXL_PI_USERNAME`` and
``CUBXL_PI_HOSTNAME``); their values are never printed, and ssh error lines are redacted before they are shown.

    python fetch_via_pi.py URL OUT.html [--pi CUBXL_PI] [--log /tmp/shop/log.jsonl]

Each call is one page load through the Pi. A JSON line per call (URL, HTTP status, final URL, bytes, UTC time)
goes to the log, so the order list can say how many pages went through the Pi.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/131.0.0.0 Safari/537.36")
MARK = "__FETCH_VIA_PI_STATUS__"


def redact(text: str, secrets: list[str]) -> str:
    for s in secrets:
        if s:
            text = text.replace(s, "<redacted>")
    text = re.sub(r"\b\d{1,3}(\.\d{1,3}){3}\b", "<ip>", text)
    return re.sub(r"\b[0-9a-f]{0,4}(:[0-9a-f]{0,4}){2,7}\b", "<ip>", text, flags=re.I)


def fetch(url: str, out: Path, pi: str = "CUBXL_PI", log: Path | None = None, rate: str = "300k",
          timeout: int = 40) -> dict:
    user, host = os.environ.get(f"{pi}_USERNAME", ""), os.environ.get(f"{pi}_HOSTNAME", "")
    if not user or not host:
        raise SystemExit(f"{pi}_USERNAME / {pi}_HOSTNAME not set")
    curl = ["curl", "-sL", "--compressed", "--max-time", str(timeout), "--limit-rate", rate,
            "-A", UA, "-H", "Accept-Language: en-US,en;q=0.9",
            "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "-w", f"\\n{MARK}:%{{http_code}}:%{{url_effective}}\\n", url]
    remote = " ".join(shlex.quote(c) for c in curl)
    cmd = ["ssh", "-C", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=15",
           f"{user}@{host}", remote]
    t0 = dt.datetime.now(dt.timezone.utc)
    p = subprocess.run(cmd, capture_output=True, timeout=timeout + 30)
    body = p.stdout
    status, final = None, url
    k = body.rfind(MARK.encode())
    if k >= 0:
        tail = body[k + len(MARK) + 1:].decode("utf-8", "replace").strip()
        code, _, final = tail.partition(":")
        status = int(code) if code.isdigit() else None
        body = body[:k].rstrip(b"\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(body)
    rec = dict(url=url, final_url=final, status=status, bytes=len(body), out=str(out),
               fetched_utc=t0.strftime("%Y-%m-%dT%H:%M:%SZ"), ssh_rc=p.returncode)
    if p.returncode != 0 and not body:
        rec["error"] = redact(p.stderr.decode("utf-8", "replace").strip()[-300:], [user, host])
    if log:
        with log.open("a") as f:
            f.write(json.dumps(rec) + "\n")
    return rec


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("url")
    ap.add_argument("out", type=Path)
    ap.add_argument("--pi", default="CUBXL_PI", help="prefix of the *_USERNAME/*_HOSTNAME variables")
    ap.add_argument("--log", type=Path, default=Path("/tmp/shop/log.jsonl"))
    a = ap.parse_args()
    rec = fetch(a.url, a.out, a.pi, a.log)
    print(json.dumps({k: rec[k] for k in ("status", "bytes", "final_url", "fetched_utc") if k in rec}
                     | ({"error": rec["error"]} if "error" in rec else {})))
    sys.exit(0 if rec.get("status") else 1)


if __name__ == "__main__":
    main()
