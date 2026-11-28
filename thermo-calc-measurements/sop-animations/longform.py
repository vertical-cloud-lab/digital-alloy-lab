"""The five SOP videos as one long-form video with chapters and narration (#262, PR #263).

    python longform.py cards       # out/mp4/lf_intro.mp4 and lf_outro.mp4: title cards at the SOP videos' size and rate
    python longform.py build       # out/mp4/sop_longform.mp4: intro, SOP 01-05, outro; narration mixed in at -16 LUFS;
                                   # out/longform.json (every part's offset, every line's time), out/longform_chapters.txt
    python longform.py check       # every narration line transcribed back by faster-whisper -> out/narration_check.json
    python longform.py small       # out/mp4/sop0N_720p.mp4: each SOP at 1280x720, small enough to commit

Narration is ``narration.json``: a list of ``{"sop": "sop01", "at": "<sub-step label, or the start of its
caption>", "dt": 0.4, "text": "..."}``. Each line starts dt seconds after the start of the sub-step it names. It is
spoken by Kokoro-82M (kokoro-onnx, Apache-2.0 weights, voice af_heart: an open local voice, not a clone of anyone)
from its phonemes, with SAY respellings for the words espeak gets wrong, each line levelled, and the whole track
normalised to -16 LUFS (EBU R128), as byu-vcl's long-forms are. A line that would overlap the one before it is pushed
later and the push is reported.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
MP4 = OUT / "mp4"
SOPS = ["sop01", "sop02", "sop03", "sop04", "sop05"]
NARRATION = HERE / "narration.json"
TTS_DIR = Path("/tmp/sop_tts")
VOICE = os.environ.get("NARRATION_VOICE", "af_heart")
SPEED = float(os.environ.get("NARRATION_SPEED", "0.96"))
SR = 24000
KOKORO = (os.environ.get("KOKORO_MODEL", "/tmp/kokoro/kokoro-v1.0.onnx"),
          os.environ.get("KOKORO_VOICES", "/tmp/kokoro/voices-v1.0.bin"))
LINE_RMS_DB = -18.0
GAP = 0.35                      # s of silence kept between lines

# how the voice should say what the captions write
SAY = {
    "DSC": "D S C", "DTA": "D T A", "STA": "S T A", "ICP-OES": "I C P O E S", "ICP": "I C P", "OES": "O E S",
    "O/N/H": "oxygen, nitrogen and hydrogen", "LPBF": "L P B F", "SEM": "S E M", "SEM-BSE": "S E M backscatter",
    "EDS": "E D S", "XRD": "X R D", "HV": "H V", "HV0.5": "H V zero point five", "HV1": "H V one",
    "HV0.05": "H V zero point zero five", "%IACS": "percent I A C S", "IACS": "I A C S", "CRM": "C R M",
    "ESPEI": "ESPY", "ORCHID": "orchid", "pycalphad": "pie calphad", "CALPHAD": "calphad", "Thermo-Calc": "Thermo Calc",
    "TC-PRISMA": "T C Prisma", "JMAK": "J mack", "PTFE": "P T F E", "HF": "H F", "BYU": "B Y U", "LFA": "L F A",
    "LECO": "Leco", "NETZSCH": "Netch", "aluminium": "aluminum", "Keller's": "Kellers", "Fiji": "Fiji",
    "Al": "aluminum", "Cu": "copper", "Mg": "magnesium", "Zn": "zinc", "Si": "silicon", "Ar": "argon",
    "µm": "microns", "µL": "microliters", "°C": "degrees C", "K/min": "kelvin per minute",
}


def _word(keys):
    return re.compile(r"(?<![\w-])(" + "|".join(map(re.escape, sorted(keys, key=len, reverse=True))) + r")(?![\w-])")


def spoken(text: str) -> str:
    return _word(SAY).sub(lambda m: SAY[m.group(1)], text)


def tts(lines: list[dict]) -> list[Path]:
    import soundfile as sf
    TTS_DIR.mkdir(parents=True, exist_ok=True)
    k, out = None, []
    for ln in lines:
        text = spoken(ln["text"])
        key = hashlib.sha256(f"{VOICE}|{SPEED}|{text}".encode()).hexdigest()[:16]
        p = TTS_DIR / f"{key}.wav"
        if not p.exists():
            if k is None:
                from kokoro_onnx import Kokoro
                k = Kokoro(*KOKORO)
            y, sr = k.create(text, voice=VOICE, speed=SPEED, lang="en-us")
            assert sr == SR, sr
            sf.write(str(p), y, sr)
        out.append(p)
    return out


def probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,nb_frames:format=duration", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    s = d["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return dict(w=s["width"], h=s["height"], fps=float(num) / float(den), dur=float(d["format"]["duration"]))


# =================================================================================================== cards
def cards():
    meta = probe(MP4 / "sop01.mp4")
    os.environ["VIZ3D_SIZE"] = f"{meta['w']}x{meta['h']}"
    os.environ["VIZ3D_FPS"] = str(int(round(meta["fps"])))
    import stage as S
    sc = S.SOPScene("lf_intro", "", gif=False)
    sc.card("Measuring what Thermo-Calc calculates: five draft SOPs, step by step",
            ["01  DSC melting and freezing of atomized powder",
             "02  Single tracks and heat-source calibration",
             "03  Archimedes density, pores and cracks",
             "04  Hardness, eddy-current conductivity and aging",
             "05  Composition (ICP-OES) and O/N/H, sent out"],
            seconds=9.0, label="intro",
            note="Draft SOPs from thermo-calc-measurements/sops (DAL #262, PR #263). Instruments modelled from "
                 "published specifications and registered to footage; data panels are synthetic examples.")
    sc.save()
    sc = S.SOPScene("lf_outro", "", gif=False)
    sc.card("What is checked, and what is not",
            ["Each new instrument: published W x D x H, fitted to reference frames (RMS px in notes/)",
             "Every frame: a collision audit of everything that moves (out/collisions/)",
             "Data panels: synthetic inputs through the repo's own analysis code, not measurements",
             "Nothing here has been run on our instruments yet: the SOPs are drafts"],
            seconds=10.0, label="outro",
            note="Code: thermo-calc-measurements/sop-animations. CAD framework from byu-vcl PR 318 (vertical-lab).")
    sc.save()


# =================================================================================================== build
def _locate(meta: dict, at: str) -> dict:
    for s in meta["substeps"]:
        if s.get("label") == at:
            return s
    for s in meta["substeps"]:
        if s.get("caption", "").startswith(at):
            return s
    raise KeyError(f"no sub-step {at!r} in {meta['name']}")


def build():
    parts = ["lf_intro", *SOPS, "lf_outro"]
    files = [MP4 / f"{p}.mp4" for p in parts]
    for f in files:
        if not f.exists():
            raise SystemExit(f"missing {f}")
    info = [probe(f) for f in files]
    same = len({(i["w"], i["h"], round(i["fps"], 3)) for i in info}) == 1
    video = MP4 / "sop_longform_video.mp4"
    lst = MP4 / "longform.concat.txt"
    lst.write_text("".join(f"file '{f.name}'\n" for f in files))
    # delivered at 1920 x 1080 and 30 fps whatever each part was drawn at (chapters drawn at 15 fps are doubled)
    W, H, FPS_OUT = (int(v) for v in os.environ.get("LONGFORM_FORMAT", "1920x1080x30").split("x"))
    ins, filt = [], []
    for i, f in enumerate(files):
        ins += ["-i", str(f)]
        filt.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=decrease:flags=lanczos,"
                    f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:white,fps={FPS_OUT},setsar=1[v{i}]")
    filt.append("".join(f"[v{i}]" for i in range(len(files))) + f"concat=n={len(files)}:v=1:a=0[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(filt), "-map", "[v]",
                    "-c:v", "libx264", "-preset", os.environ.get("LONGFORM_PRESET", "veryfast"), "-crf", "20",
                    "-pix_fmt", "yuv420p", str(video)], check=True)
    lst.unlink()
    offsets, t = {}, 0.0
    for p, i in zip(parts, info):
        offsets[p] = t
        t += i["dur"]
    total = t
    # ---------------------------------------------------------------------------- narration
    lines = json.loads(NARRATION.read_text()) if NARRATION.exists() else []
    placed = []
    if lines:
        import soundfile as sf
        metas = {p: json.loads((OUT / f"{p}.json").read_text()) for p in SOPS}
        wavs = tts(lines)
        track = np.zeros(int((total + 2.0) * SR), np.float32)
        last_end = 0.0
        for ln, w in zip(lines, wavs):
            meta = metas[ln["sop"]]
            s = _locate(meta, ln["at"])
            want = offsets[ln["sop"]] + s["start_frame"] / meta["fps"] + float(ln.get("dt", 0.4))
            y, sr = sf.read(str(w), dtype="float32")
            rms = float(np.sqrt(np.mean(y ** 2))) or 1e-6
            y = y * (10 ** (LINE_RMS_DB / 20) / rms)
            y = np.clip(y, -0.89, 0.89)
            start = max(want, last_end + GAP)
            i0 = int(start * SR)
            track[i0:i0 + len(y)] += y[: max(0, len(track) - i0)]
            end = start + len(y) / SR
            sub_end = offsets[ln["sop"]] + (s["end_frame"] + 1) / meta["fps"]
            placed.append(dict(sop=ln["sop"], at=ln["at"], text=ln["text"], want_s=round(want, 2),
                               start_s=round(start, 2), end_s=round(end, 2), pushed_s=round(start - want, 2),
                               runs_past_substep_s=round(max(0.0, end - sub_end), 2)))
            last_end = end
        wav = MP4 / "sop_longform_narration.wav"
        sf.write(str(wav), track, SR)
        dst = MP4 / "sop_longform.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(wav), "-map", "0:v",
                        "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac",
                        "-b:a", "160k", "-ar", "48000", "-t", f"{total:.3f}", "-movflags", "+faststart", str(dst)],
                       check=True)
        video.unlink()
        wav.unlink()
        srt = []
        for k, p in enumerate(placed, 1):
            srt.append(f"{k}\n{_ts(p['start_s'])} --> {_ts(p['end_s'])}\n{p['text']}\n")
        (OUT / "sop_longform.srt").write_text("\n".join(srt))
    else:
        video.rename(MP4 / "sop_longform.mp4")
    # ---------------------------------------------------------------------------- chapters
    chapters = [(0.0, "Intro")]
    titles = {"sop01": "SOP 01 · DSC", "sop02": "SOP 02 · Single tracks", "sop03": "SOP 03 · Density",
              "sop04": "SOP 04 · Hardness, conductivity, aging", "sop05": "SOP 05 · Composition, O/N/H"}
    for p in SOPS:
        meta = json.loads((OUT / f"{p}.json").read_text())
        seen = set()
        for s in meta["substeps"]:
            ch = s.get("chapter", p)
            if ch in seen:
                continue
            seen.add(ch)
            t0 = offsets[p] + s["start_frame"] / meta["fps"]
            name = s["caption"] if s.get("card") else (s.get("label") or s.get("caption", ""))
            name = re.sub(r"\s+", " ", name.split("|")[0]).strip()
            label = titles[p] if len(seen) == 1 else f"{titles[p].split(' · ')[0]} · {name}"
            if not chapters or t0 - chapters[-1][0] >= 10.5:
                chapters.append((t0, label[:90]))
    chapters.append((offsets["lf_outro"], "What is checked, and what is not"))
    txt = "\n".join(f"{_mmss(t)} {name}" for t, name in chapters)
    (OUT / "longform_chapters.txt").write_text(txt + "\n")
    (OUT / "longform.json").write_text(json.dumps(dict(parts=parts, offsets_s=offsets, total_s=round(total, 2),
                                                       same_encoding=same, narration=placed,
                                                       chapters=[[round(t, 2), n] for t, n in chapters]), indent=1)
                                       + "\n")
    pushed = [p for p in placed if p["pushed_s"] > 0.5 or p["runs_past_substep_s"] > 1.0]
    print(f"sop_longform.mp4: {total / 60:.1f} min, {len(placed)} lines, {len(chapters)} chapters, "
          f"{len(pushed)} lines pushed or running long")
    for p in pushed:
        print("  ", p)


def _ts(t: float) -> str:
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def _mmss(t: float) -> str:
    m, s = divmod(int(t), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


# =================================================================================================== check
def check(model_size: str = "base.en"):
    import jiwer
    import soundfile as sf
    from faster_whisper import WhisperModel
    from scipy.signal import resample_poly
    lines = json.loads(NARRATION.read_text())
    wavs = tts(lines)
    m = WhisperModel(model_size, device="cpu", compute_type="int8")
    rows = []
    for ln, w in zip(lines, wavs):
        y, sr = sf.read(str(w), dtype="float32")
        y16 = resample_poly(y, 2, 3).astype(np.float32)
        segs, _ = m.transcribe(y16, language="en", beam_size=5)
        heard = " ".join(s.text for s in segs).strip()
        a, b = _norm(spoken(ln["text"])), _norm(heard)
        rows.append(dict(text=ln["text"], heard=heard, wer=round(jiwer.wer(a, b), 3)))
    bad = [r for r in rows if r["wer"] > 0.15]
    (OUT / "narration_check.json").write_text(json.dumps(dict(model=model_size, lines=len(rows),
                                                              mean_wer=round(float(np.mean([r["wer"] for r in rows])), 3),
                                                              flagged=bad, rows=rows), indent=1) + "\n")
    print(f"{len(rows)} lines, mean WER {np.mean([r['wer'] for r in rows]):.3f}, {len(bad)} over 0.15")
    for r in bad:
        print("  ", r)


def _norm(s: str) -> str:
    from num2words import num2words
    s = s.replace("°", " degrees").replace("%", " percent ")
    s = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", s)
    s = re.sub(r"(\d),(\d{3})", r"\1\2", s)
    s = re.sub(r"\d+(\.\d+)?", lambda m: " " + num2words(float(m.group()) if "." in m.group() else int(m.group()))
               + " ", s)
    s = re.sub(r"(?<=[A-Z])-(?=[A-Z])", "", s)                   # ICP-OES -> ICPOES
    s = re.sub(r"(?<=[A-Z])(?=\d)|(?<=\d)(?=[A-Z])", " ", s)       # HV0.5 -> HV 0.5
    s = s.lower().replace("-", " ")
    s = re.sub(r"[^a-z' ]", " ", s)
    out, single = [], False
    for w in s.split():                       # letters said one by one, written as one word: i c p -> icp
        one = len(w) == 1 and w != "a"
        if one and single:
            out[-1] += w
        else:
            out.append(w)
        single = one
    return " ".join(out)


# =================================================================================================== small copies
def small():
    for p in SOPS:
        src = MP4 / f"{p}.mp4"
        if not src.exists():
            continue
        dst = MP4 / f"{p}_720p.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", "scale=1280:-2", "-c:v", "libx264",
                        "-preset", "slow", "-crf", "27", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(dst)],
                       check=True)
        print(dst.name, f"{dst.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    {"cards": cards, "build": build, "check": check, "small": small}[sys.argv[1]]()
