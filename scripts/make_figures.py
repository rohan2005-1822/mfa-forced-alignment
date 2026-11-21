"""Praat-style figures: waveform + spectrogram + word tier + phone tier.
usage: python scripts/make_figures.py results/textgrids data/corpus results/figures"""
import os, sys, wave
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
sys.path.insert(0, os.path.dirname(__file__))
from textgrid_utils import read_textgrid

tg_dir, wav_dir, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)

def load(path):
    w = wave.open(path)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
    return x / 32768.0, w.getframerate()

def draw(stem, folder, t0, t1, name):
    T = read_textgrid(f"{tg_dir}/{folder}/{stem}.TextGrid")
    x, sr = load(f"{wav_dir}/{folder}/{stem}.wav")
    seg = x[int(t0 * sr):int(t1 * sr)]; t = np.arange(len(seg)) / sr + t0
    fig, ax = plt.subplots(4, 1, figsize=(11, 6.4), sharex=True,
                           gridspec_kw={"height_ratios": [2, 3, 1, 1]})
    ax[0].plot(t, seg, lw=0.5, color="k"); ax[0].set_ylabel("waveform")
    f, tt, S = spectrogram(seg, sr, nperseg=int(0.008 * sr), noverlap=int(0.0075 * sr))
    ax[1].pcolormesh(tt + t0, f, 10 * np.log10(S + 1e-12), cmap="Greys", shading="auto",
                     vmin=-110, vmax=-50)
    ax[1].set_ylim(0, 5000); ax[1].set_ylabel("Hz")
    for a, tier, lab in ((ax[2], "words", "words"), (ax[3], "phones", "phones")):
        for xa, xb, tx in T[tier]:
            if xb < t0 or xa > t1: continue
            a.axvline(xa, color="#1b7f8c", lw=1); a.axvline(xb, color="#1b7f8c", lw=1)
            if tx:
                a.text((max(xa, t0) + min(xb, t1)) / 2, 0.5, tx, ha="center", va="center",
                       fontsize=9 if tier == "words" else 8, clip_on=True)
        a.set_ylim(0, 1); a.set_yticks([]); a.set_ylabel(lab)
    ax[3].set_xlim(t0, t1); ax[3].set_xlabel("time (s)")
    fig.suptitle(f"{stem}  {t0:.2f}-{t1:.2f} s"); fig.tight_layout()
    fig.savefig(f"{out}/{name}.png", dpi=150); plt.close(fig)
    print("saved", name)

draw("F2BJRLP1", "f2b", 11.8, 15.8, "fig1_F2BJRLP1_good_alignment")
draw("F2BJRLP1", "f2b", 20.0, 24.0, "fig2_F2BJRLP1_wburs_reduced_vowels")
for i in ("01", "02", "03"):
    draw(f"ISLE_SESS0131_BLOCKD02_{i}_sprt1", "isle_sess0131", 0.3, 2.5, f"fig_ISLE_{i}")
