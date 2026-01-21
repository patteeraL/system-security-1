from pathlib import Path

# Load the local dictionary file (relative to this repo) so it works on any machine.
_HERE = Path(__file__).resolve().parent
_WORDLIST_PATH = _HERE / "10k-most-common.txt"

with _WORDLIST_PATH.open("r", encoding="utf-8", errors="ignore") as f:
    wordlists = f.read()
