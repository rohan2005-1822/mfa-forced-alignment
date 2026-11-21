#!/usr/bin/env bash
# Full forced-alignment pipeline: raw files -> clean corpus -> validate -> G2P suggestions
# -> custom dictionary -> MFA align -> statistics + figures.
#
# usage:  bash run_pipeline.sh <raw_dir>
#   raw_dir must contain  wav/  and  transcripts/  (the files given with the assignment)
# Requires MFA 3.x on PATH (conda activate aligner) and python3 with numpy, scipy, matplotlib.
set -euo pipefail
RAW="${1:?usage: bash run_pipeline.sh <raw_dir>}"
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$HERE/work"; CORPUS="$WORK/corpus"; OUT="$HERE/results"
mkdir -p "$WORK" "$OUT"

echo "[1/7] prepare corpus (NIST->WAV, clean transcripts)"
python3 "$HERE/scripts/prepare_corpus.py" "$RAW" "$CORPUS"

echo "[2/7] download pretrained models"
mfa model download acoustic english_us_arpa
mfa model download dictionary english_us_arpa
mfa model download g2p english_us_arpa
BASE_DICT="$(find "${MFA_ROOT_DIR:-$HOME/Documents/MFA}" -name english_us_arpa.dict | head -1)"

echo "[3/7] find out-of-vocabulary words"
python3 "$HERE/scripts/find_oov.py" "$CORPUS" "$BASE_DICT" | tee "$OUT/oov_words.txt"

echo "[4/7] G2P suggestions for OOV words (reviewed by hand, see dictionary/custom_additions.dict)"
mfa g2p "$CORPUS" english_us_arpa "$OUT/g2p_suggestions.txt" --dictionary_path english_us_arpa --clean

echo "[5/7] build custom dictionary"
python3 "$HERE/scripts/build_dictionary.py" "$BASE_DICT" "$HERE/dictionary/custom_additions.dict" "$WORK/custom.dict"

echo "[6/7] align"
mfa align "$CORPUS" "$WORK/custom.dict" english_us_arpa "$OUT/textgrids" --clean --single_speaker --output_format long_textgrid

echo "[7/7] statistics and figures"
python3 "$HERE/scripts/analyze_alignment.py" "$OUT/textgrids" "$OUT/alignment_summary.csv"
python3 "$HERE/scripts/make_figures.py" "$OUT/textgrids" "$CORPUS" "$OUT/figures"
echo "done: $OUT"
