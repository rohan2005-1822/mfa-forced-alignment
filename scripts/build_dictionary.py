"""Copy the pretrained english_us_arpa dictionary and append the manual entries.
usage: python scripts/build_dictionary.py <base.dict> <additions.dict> <out.dict>"""
import shutil, sys
base, add, out = sys.argv[1:4]
shutil.copy(base, out)
with open(out, "a") as o:
    o.write(open(add).read())
print("wrote", out)
