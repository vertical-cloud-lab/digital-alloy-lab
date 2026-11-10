"""Screen SBIR.gov's bulk award file for metal vat-photopolymerization awards.

SBIR.gov's own keyword box ANDs whole words in a way that misses most hits, so this reads the bulk
file with abstracts (https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv, ~400 MB, refreshed
monthly) and keeps awards whose title or abstract mentions a photopolymerization step and a metal
part. Contact names, phones and e-mails are dropped; only the PI name and title are kept.

    python -I scripts/sbir_metal_vpp_screen.py /tmp/sbirdata/award_data.csv out.csv
"""

import csv
import re
import sys

VPP = re.compile(
    r"stereolithograph|vat[ -]photopolymer|photopolymeri[sz]|photo-?polymer|photo-?cur(?:e|able|ing)"
    r"|light-cur(?:e|able|ing)|uv-?cur(?:e|able|ing)|digital light process|\bDLP\b|lithography-based metal"
    r"|\bLMM\b|two-photon|\b2PP\b|micro-?stereolithograph|\bP[uµ]SL\b|hydrogel infusion|photoresin"
    r"|photo-?resist|mask[- ]projection|continuous liquid interface|volumetric (?:additive|printing|3D)"
    r"|computed axial lithography", re.I)
METAL = re.compile(
    r"\bmetal(?:s|lic)?\b|copper|stainless|\bsteel|titanium|tungsten|molybdenum|niobium|tantalum|rhenium"
    r"|nickel|inconel|superalloy|cobalt|alumin(?:um|ium)\b|\bsilver\b|\bgold\b|platinum|\bMIM\b"
    r"|metal injection|refractory metal|cemented carbide|WC-Co|tungsten carbide|heavy alloy", re.I)
SINTER = re.compile(r"sinter|debind|de-bind|binder burn|burn-?out|green (?:part|body|bodies)|brown part"
                    r"|calcin|reduc(?:e|ed|tion) to (?:the )?metal|forming gas|hydrogen atmosphere", re.I)
CERAMIC_ONLY = re.compile(r"ceramic|alumina|zirconia|silicon carbide|silicon nitride|\bSiC\b|glass", re.I)

KEEP = ["Company", "Award Title", "Agency", "Branch", "Phase", "Program", "Contract", "Topic Code",
        "Solicitation Number", "Award Year", "Proposal Award Date", "Award Amount", "City", "State",
        "PI Name", "PI Title", "RI Name"]


def main(src, dst):
    csv.field_size_limit(sys.maxsize)
    rows = []
    with open(src, newline="", encoding="utf-8-sig", errors="replace") as f:
        for r in csv.DictReader(f):
            text = f"{r.get('Award Title', '')}\n{r.get('Abstract', '')}"
            vpp = VPP.findall(text)
            if not vpp:
                continue
            metal = METAL.findall(text)
            if not metal:
                continue
            sinter = SINTER.findall(text)
            out = {k: r.get(k, "") for k in KEEP}
            out["vpp_terms"] = "; ".join(sorted({v.lower() for v in vpp}))
            out["metal_terms"] = "; ".join(sorted({m.lower() for m in metal}))
            out["sinter_terms"] = "; ".join(sorted({s.lower() for s in sinter}))
            out["mentions_ceramic"] = "Y" if CERAMIC_ONLY.search(text) else ""
            out["score"] = len(set(v.lower() for v in vpp)) + len(set(m.lower() for m in metal)) + 2 * len(
                set(s.lower() for s in sinter))
            out["abstract"] = re.sub(r"\s+", " ", r.get("Abstract", ""))[:3000]
            rows.append(out)
    rows.sort(key=lambda r: -r["score"])
    with open(dst, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "candidate awards written to", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
