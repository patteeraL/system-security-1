"""
Exercise 1: Find the word that its hashes result matches the target hash

Algorithms:
- SHA-1

hash_target = "d54cc1fe76f5186380a0939d2fc1723c44e8a5f7"  # SHA-1 hex digest

"""
import hashlib

from wordlists import wordlists

hash_target = "d54cc1fe76f5186380a0939d2fc1723c44e8a5f7"  # SHA-1 hex digest

# List of case substitutions for brute forcing variants.
substitution = {
    "a": ["a", "A", "@", "4"],
    "b": ["b", "B", "8"],
    "c": ["c", "C"],
    "d": ["d", "D"],
    "e": ["e", "E", "3"],
    "f": ["f", "F"],
    "g": ["g", "G", "6", "9"],
    "h": ["h", "H"],
    "i": ["i", "I", "1", "!"],
    "j": ["j", "J"],
    "k": ["k", "K"],
    "l": ["l", "L", "1"],
    "m": ["m", "M"],
    "n": ["n", "N"],
    "o": ["o", "O", "0"],
    "p": ["p", "P"],
    "q": ["q", "Q"],
    "r": ["r", "R"],
    "s": ["s", "S", "$", "5"],
    "t": ["t", "T", "7"],
    "u": ["u", "U"],
    "v": ["v", "V"],
    "w": ["w", "W"],
    "x": ["x", "X"],
    "y": ["y", "Y"],
    "z": ["z", "Z", "2"],
}


def sha1_hex(text):
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()


def variants(word, max_variants=50000):
    pools = []
    for ch in word:
        pools.append(substitution.get(ch.lower(), [ch]))
    results = [""]
    for choices in pools:
        new_results = []
        for prefix in results:
            for c in choices:
                new_results.append(prefix + c)
                if len(new_results) >= max_variants:
                    return new_results
        results = new_results
    return results


def _iter_words(wordlists_value):
    if isinstance(wordlists_value, str):
        for w in wordlists_value.splitlines():
            yield w
    else:
        for w in wordlists_value:
            yield w


def main():
    for base in _iter_words(wordlists):
        base = base.strip()
        if not base:
            continue

        if sha1_hex(base) == hash_target:
            print(f"FOUND: {base}")
            return

        for cand in variants(base):
            if sha1_hex(cand) == hash_target:
                print(f"FOUND: {cand}, Hash: {sha1_hex(cand)}")
                return

    print("Not found in provided wordlist/substitutions.")



main()
