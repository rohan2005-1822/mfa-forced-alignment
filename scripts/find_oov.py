"""List corpus words that are missing from a dictionary.
usage: python scripts/find_oov.py <corpus_dir> <dictionary>"""
import glob, sys
corpus, dic = sys.argv[1:3]
known = {l.split()[0].lower() for l in open(dic) if l.strip()}
words = set()
for f in glob.glob(f"{corpus}/*/*.lab"):
    words |= set(open(f).read().split())
oov = sorted(w for w in words if w not in known)
print(len(oov), "OOV words:", oov)
