"""
Exercise 2: Measure how many hashes/second can be computed in a fixed time window.

Algorithms:
- MD5
- SHA-1
- bcrypt
"""

import hashlib
import time

import bcrypt


def benchmark(duration: float, fn) -> tuple[int, float]:
    start = time.perf_counter()
    end = start + duration
    count = 0
    while time.perf_counter() < end:
        fn()
        count += 1
    elapsed = time.perf_counter() - start
    return count, elapsed


def main():
    duration = 2.0

    msg = b"Chulalongkorn"

    # bcrypt needs a salt; keep it constant for benchmarking so we only
    # measure the cost of the hash function itself.
    salt = bcrypt.gensalt(rounds=12)

    def md5_hash():
        hashlib.md5(msg).digest()

    def sha1_hash():
        hashlib.sha1(msg).digest()

    def bcrypt_hash():
        bcrypt.hashpw(msg, salt)

    tests = [
        ("MD5", md5_hash),
        ("SHA-1", sha1_hash),
        ("bcrypt (rounds=12)", bcrypt_hash),
    ]

    print(f"Benchmark window: {duration:.1f}s\n")
    for name, fn in tests:
        n, elapsed = benchmark(duration, fn)
        rate = n / elapsed if elapsed > 0 else 0.0
        print(f"{name:18}  {n:10d} hashes  in {elapsed:6.3f}s  ->  {rate:12.1f} hashes/sec")


if __name__ == "__main__":
    main()
