[Security 1] - Password Security


Dictionary References: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt 

Prerequisite
- Python installed
- hashlib
- bcrypt


Exercises
1. Objective: Understand how attackers use pre-built word lists (dictionaries) to crack hashes of common passwords.

Scenario: You have discovered a SHA-1 hash in a compromised system:
 d54cc1fe76f5186380a0939d2fc1723c44e8a5f7.


You suspect the password is a simple, common word, possibly with some character substitutions.


Task: Write a Python program that reads a list of words, applies common substitutions, hashes the result, and checks if it matches the target hash.
Note that you might want to include substitution in your code (lowercase, uppercase, number for letter [‘o’ => 0 , ‘l’ => 1, ‘i’ => 1]).


2. Objective: To understand why modern password hashing algorithms like bcrypt are more secure than older ones like MD5 and SHA-1.

Task: Design and run an experiment to measure how many hashes each algorithm can compute in a fixed amount of time. The code must test atleast MD5 , SHA-1 , and bcrypt .
(You may also try additional algorithms like SHA256, SHA512, scrypt, Argon2.)

Hint: Use time function in python.


3. Objective: To apply the performance measurements to understand the importance of password length and algorithm choice.

Task: Based on the measurements from Exercise 2, estimate how long it would take an attacker to brute-force a password of a given length
You may assume that the password contains only upper-case, lower-case,  numbers and symbols.

What does it suggest about the length of a proper password. (ie. Use more than a year to brute force.)

4. If a given hash value is from a bcrypt algorithm, is it practical to do a brute-force attack?

5. If a given hash value is from a bcrypt algorithm, is it practical to perform a rainbow table attack?

6. You have to store a password in a database. Please explain your design/strategy for securely storing it.
(Hints: Proper hash function, Salting, Cost factor, Database Security)



## How to run (this repo)

Prereqs:
- Python installed
- `pip install bcrypt`

Files:
- `exercise1.py`: Exercise 1 (dictionary + substitutions + SHA-1 compare)
- `exercise2.py`: Exercise 2 (hashes/sec benchmark for MD5, SHA-1, bcrypt)
- `exercise3.py`: Exercise 3 (time-to-crack estimator from hashes/sec)

Run:
- `python exercise1.py`
- `python exercise2.py`
- `python exercise3.py --rate <hashes_per_sec> --charset 94 --min-len 6 --max-len 12`



## Exercise 1 (Dictionary + substitutions)

Target SHA-1:
- `d54cc1fe76f5186380a0939d2fc1723c44e8a5f7`

Result (found by `exercise1.py` using the 10k list + substitutions):
- **Password = `ThaiLanD`**



## Exercise 2 (Hash speed experiment)

On this machine (2-second window):
- **MD5**: ~1.33 million hashes/sec
- **SHA-1**: ~1.37 million hashes/sec
- **bcrypt (rounds=12)**: ~4.7 hashes/sec

Key takeaway:
- MD5/SHA-1 are extremely fast → attackers can test huge numbers of guesses quickly.
- bcrypt is intentionally slow (and tunable via cost) → slows down guessing attacks dramatically.



## Exercise 3 (Brute-force time estimate)

Assumptions used by `exercise3.py`:
- Character set = 94 printable ASCII characters
- Average case = attacker needs ~50% of the total search space
- Time ≈ \((94^L / 2) / \text{guesses_per_sec}\)

Using the measured **SHA-1** speed (~1.366 million guesses/sec):
- length 7: ~274.6 days (average)
- length 8: ~70.7 years (average)  → **“> 1 year” starts around length ≈ 8**

So, for a brute force scenario, this suggests:
- **Short passwords are very risky**, even with mixed characters.
- A “proper password” should be long enough that attacks take > 1 year; with these assumptions and this machine, **8+ random characters** already crosses 1 year for SHA-1, and longer is much safer.



## Exercise 4: If the hash is bcrypt, is brute-force practical?

**Not practical** (for strong passwords), because:
- bcrypt is slow by design (cost factor), so guesses/sec is tiny compared with MD5/SHA‑1.
- With the measured ~4.7 guesses/sec, even length 6 over 94 chars is already thousands of years on average.

(Attackers can use GPUs/ASICs and parallelism, but bcrypt still massively increases cost vs MD5/SHA‑1. The bigger the cost factor, the harder it gets.)



## Exercise 5: If the hash is bcrypt, is a rainbow table attack practical?

**Not practical**, because:
- bcrypt includes a **salt** as part of its hash format.
- Salts force attackers to regenerate their precomputed table reuse per-salt.
- bcrypt is also slow, so generating tables is expensive.


## Exercise 6: Secure password storage design/strategy

- **Use a modern password hashing**: `bcrypt`, `scrypt`, or **`Argon2id`**.
- **Provide unique random salt per user**: generated automatically by the KDF (bcrypt/Argon2); stored with the hash (this is safe).
- **Tune cost factor**: - bcrypt: increase rounds until verification is ~100–300ms on your server (typical guidance; choose what your UX/infra can handle). - revisit over time as hardware improves.
- **Add pepper** (extra secret): store a server-side secret (not in DB) and include it in the password hashing input; rotate carefully.
- **Never store plaintext passwords**, and never store unsalted MD5/SHA‑1/SHA‑256 for passwords.
- **Protect the database**:
  - encryption at rest, least-privilege DB accounts, patching, backups protected, audit logging.
  - application-level rate limiting / account lockout for online guessing.
  - use TLS for in-transit protection and protect secrets/configs.

What gets stored in the DB:
- `username/email`
- `password_hash` (which already encodes algorithm + salt`)