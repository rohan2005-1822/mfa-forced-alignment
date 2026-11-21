"""Summary statistics of the alignments -> results/alignment_summary.csv
usage: python scripts/analyze_alignment.py results/textgrids results/alignment_summary.csv"""
import csv, glob, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from textgrid_utils import read_textgrid

tg_dir, out = sys.argv[1:3]
rows = []
for fn in sorted(glob.glob(f"{tg_dir}/*/*.TextGrid")):
    T = read_textgrid(fn)
    words = [x for x in T["words"] if x[2]]
    phones = [x for x in T["phones"] if x[2]]
    dur = [b - a for a, b, _ in phones]
    rows.append({
        "file": os.path.basename(fn)[:-9],
        "duration_s": round(T["words"][-1][1], 2),
        "words": len(words), "phones": len(phones),
        "phones_le_30ms": sum(d < 0.0305 for d in dur),
        "phones_le_10ms": sum(d < 0.0105 for d in dur),
        "mean_phone_ms": round(1000 * sum(dur) / len(dur), 1),
        "pauses_gt_400ms": sum(1 for a, b, c in T["words"] if not c and 0 < a and b - a > 0.4),
    })
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
