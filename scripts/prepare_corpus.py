"""Build an MFA-ready corpus from the raw assignment files.

usage: python scripts/prepare_corpus.py <raw_dir> <out_dir>
  raw_dir  contains  wav/  and  transcripts/  (the files given with the assignment)
  out_dir  gets      f2b/  and  isle_sess0131/  with  name.wav + name.lab

- NIST SPHERE wavs (the F2BJRLP files) are converted to plain RIFF WAV (MFA cannot read NIST).
- Transcripts are cleaned: lowercase, punctuation removed, hyphens -> spaces,
  "S.J.C." -> "S J C".
"""
import glob, os, re, shutil, sys, wave

def clean(t):
    t = t.replace("S.J.C.", "S J C")
    t = re.sub(r"(?<=\w)- (?=\w)", " ", t)   # "seventy- six"
    t = t.replace("-", " ")                   # "de-politicize"
    t = re.sub(r"[^\w' ]", " ", t.replace("\n", " "))
    return re.sub(r"\s+", " ", t).strip().lower() + "\n"

def main(raw, out):
    for d in ("f2b", "isle_sess0131"):
        os.makedirs(f"{out}/{d}", exist_ok=True)
    for w in sorted(glob.glob(f"{raw}/wav/*.wav")):
        name = os.path.basename(w); stem = name[:-4]
        folder = "f2b" if stem.upper().startswith("F2B") else "isle_sess0131"
        dst = f"{out}/{folder}/{name}"
        data = open(w, "rb").read()
        if data[:7] == b"NIST_1A":
            hdr = int(data[8:16])                       # header size, normally 1024
            f = wave.open(dst, "wb")
            f.setnchannels(1); f.setsampwidth(2); f.setframerate(16000)
            f.writeframes(data[hdr:]); f.close()
        else:
            shutil.copy(w, dst)
        txt = glob.glob(f"{raw}/transcripts/{stem}.*")[0]
        open(f"{out}/{folder}/{stem}.lab", "w").write(clean(open(txt).read()))
        print("prepared", folder, stem)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
