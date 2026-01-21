"""
Exercise 3: Estimate brute-force time from a measured hashing rate.

Assumptions:
- Each guess requires one hash computation.
- Search space size is (charset_size ** length).
- On average, attacker finds the password halfway through the search space.

Run examples:
  python exercise3.py --rate 50000000 --charset 94 --min-len 8 --max-len 12
  python exercise3.py --rate 100 --charset 94 --min-len 6 --max-len 10
"""

import argparse
import math


def format_seconds(seconds: float) -> str:
    minute = 60
    hour = 60 * minute
    day = 24 * hour
    year = 365 * day

    if seconds < 1:
        return f"{seconds:.3f} s"
    if seconds < minute:
        return f"{seconds:.2f} s"
    if seconds < hour:
        return f"{seconds / minute:.2f} min"
    if seconds < day:
        return f"{seconds / hour:.2f} hr"
    if seconds < year:
        return f"{seconds / day:.2f} days"
    return f"{seconds / year:.2f} years"


def estimate_bruteforce_time() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rate", type=float, required=True, help="hashes per second")
    parser.add_argument("--charset", type=int, default=94, help="size of character set (default 94 = printable ASCII)")
    parser.add_argument("--min-len", type=int, default=8)
    parser.add_argument("--max-len", type=int, default=12)
    args = parser.parse_args()

    rate = args.rate
    charset = args.charset
    min_len = args.min_len
    max_len = args.max_len

    if rate <= 0:
        raise SystemExit("rate must be > 0")
    if charset <= 1:
        raise SystemExit("charset must be > 1")
    if min_len <= 0 or max_len < min_len:
        raise SystemExit("invalid min-len/max-len")

    print(f"Rate: {rate:.1f} guesses/sec")
    print(f"Charset size: {charset}")
    print("Assume average-case (50% of search space)\n")

    seconds_per_year = 365 * 24 * 60 * 60

    for length in range(min_len, max_len + 1):
        total_space = charset**length 
        avg_guesses = total_space / 2.0
        seconds = avg_guesses / rate
        # Use ASCII
        print(f"len={length:2d}  space~{total_space:.3e}  avg time~{format_seconds(seconds)}")

    # Smallest length for which the average crack time exceeds 1 year.
    length_for_one_year = math.ceil(math.log(2 * rate * seconds_per_year, charset))
    print(
        f"\nAverage time > 1 year threshold at about length >= {length_for_one_year} "
    )


if __name__ == "__main__":
    estimate_bruteforce_time()
