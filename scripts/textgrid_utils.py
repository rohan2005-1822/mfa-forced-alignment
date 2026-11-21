import re

def read_textgrid(fn):
    """Return {tier_name: [(xmin, xmax, text), ...]} for a Praat long-format TextGrid."""
    t = open(fn, encoding="utf-8").read()
    tiers = {}
    for m in re.finditer(r'name = "(\w+)".*?(?=item \[|\Z)', t, re.S):
        iv = re.findall(r'xmin = ([\d.]+)\s+xmax = ([\d.]+)\s+text = "(.*?)"', m.group(0))
        tiers[m.group(1)] = [(float(a), float(b), c) for a, b, c in iv]
    return tiers
