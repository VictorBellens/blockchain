import hashlib
import random
import string
import time

# Re-implented hash functions

def xor32_hash(s: str) -> str:
    """
    For each character at index i, XOR its ASCII value shifted left by
    (i % 4)*8 bits into a 32-bit accumulator.
    For an 8-char string this means:
      byte 0 = s[0] ^ s[4],  byte 1 = s[1] ^ s[5],
      byte 2 = s[2] ^ s[6],  byte 3 = s[3] ^ s[7]
    """
    h = 0
    for i, c in enumerate(s):
        shift = (i % 4) * 8
        h ^= (ord(c) << shift)
    return f"{h & 0xFFFFFFFF:08x}"


def simple_hash(s: str) -> str:
    """djb2-style polynomial hash: h = h*31 + ord(c), 32-bit."""
    hash_val = 0
    for char in s:
        hash_val = ((hash_val << 5) - hash_val + ord(char)) & 0xFFFFFFFF
    return f"{hash_val:08x}"


def sha256_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# Exercise 1

def exercise1():
    s1, s2 = "AAAABBBB", "BBBBAAAA"
    h1, h2 = xor32_hash(s1), xor32_hash(s2)
    assert s1 != s2
    assert h1 == h2, f"Hash mismatch: {h1} vs {h2}"
    print(f"[Ex1] Collision: '{s1}' and '{s2}'  =>  hash = {h1}")
    return s1, s2


# Exercise 2

def exercise2():
    target = "1b575451"
    s = "aaaA056Z"
    h = xor32_hash(s)
    assert h == target, f"Expected {target}, got {h}"
    print(f"[Ex2] Pre-image of {target}: '{s}'")
    return s


# Exercise 3

def exercise3():
    print("[Ex3] Brute-forcing collision in simple_hash (birthday attack)…")
    CHARS = string.ascii_letters + string.digits
    seen: dict[str, str] = {}
    rng = random.Random(0)
    start = time.time()
    attempts = 0
    while True:
        s = "".join(rng.choices(CHARS, k=8))
        h = simple_hash(s)
        if h in seen and seen[h] != s:
            elapsed = time.time() - start
            s2 = seen[h]
            print(f"       Found after {attempts+1:,} attempts ({elapsed:.3f}s)")
            print(f"       '{s}' and '{s2}'  =>  hash = {h}")
            assert simple_hash(s) == simple_hash(s2)
            return s, s2
        seen[h] = s
        attempts += 1


# Excercise 4

TARGETS = ["cafe", "faded", "decade"]

def exercise4():
    results = []
    for target_hex in TARGETS:
        print(f"[Ex4] Searching SHA-256 prefix '{target_hex}'…")
        start = time.time()
        counter = 0
        rng = random.Random(42)
        while True:
            suffix = "".join(rng.choices(string.ascii_letters + string.digits, k=8))
            candidate = "bitcoin" + suffix
            digest = sha256_hash(candidate)
            if digest.startswith(target_hex):
                elapsed = time.time() - start
                print(f"       '{candidate}'  =>  {digest[:16]}...  ({counter+1:,} attempts, {elapsed:.3f}s)")
                results.append(candidate)
                break
            counter += 1
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    s1_ex1, s2_ex1 = exercise1()
    print()

    s_ex2 = exercise2()
    print()

    s1_ex3, s2_ex3 = exercise3()
    print()

    ex4_strings = exercise4()
    print()

    print("=" * 60)
    print("SOLUTIONS")
    print(f"  Exercise 1 (xor32 collision):   {s1_ex1},{s2_ex1}")
    print(f"  Exercise 2 (xor32 pre-image):   {s_ex2}")
    print(f"  Exercise 3 (simple_hash coll.): {s1_ex3},{s2_ex3}")
    print(f"  Exercise 4 (SHA-256 PoW):       {','.join(ex4_strings)}")
    print("=" * 60)
