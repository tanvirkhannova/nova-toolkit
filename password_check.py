"""Password strength checker for nova-toolkit."""

import math
import string

COMMON = {"password", "123456", "qwerty", "letmein", "admin", "welcome", "iloveyou"}


def entropy_bits(pw: str) -> float:
    """Estimate entropy from the size of the character pool used."""
    pool = 0
    if any(c in string.ascii_lowercase for c in pw):
        pool += 26
    if any(c in string.ascii_uppercase for c in pw):
        pool += 26
    if any(c in string.digits for c in pw):
        pool += 10
    if any(c in string.punctuation for c in pw):
        pool += len(string.punctuation)
    if any(c not in string.printable for c in pw):
        pool += 100
    return len(pw) * math.log2(pool) if pool else 0.0


def check(pw: str) -> dict:
    """Return a score (0-4), a label, entropy and improvement tips."""
    tips = []
    if pw.lower() in COMMON:
        return {"score": 0, "label": "very weak", "entropy": 0.0,
                "tips": ["This is one of the most common passwords — never use it."]}
    if len(pw) < 12:
        tips.append("Use at least 12 characters.")
    if not any(c.isupper() for c in pw):
        tips.append("Add an uppercase letter.")
    if not any(c.isdigit() for c in pw):
        tips.append("Add a number.")
    if not any(c in string.punctuation for c in pw):
        tips.append("Add a symbol like ! @ # $.")

    bits = entropy_bits(pw)
    score = 0 if bits < 28 else 1 if bits < 36 else 2 if bits < 60 else 3 if bits < 80 else 4
    labels = ["very weak", "weak", "fair", "strong", "very strong"]
    return {"score": score, "label": labels[score], "entropy": round(bits, 1), "tips": tips}


if __name__ == "__main__":
    import sys
    result = check(sys.argv[1] if len(sys.argv) > 1 else input("Password: "))
    print(f"[{result['label'].upper()}] ~{result['entropy']} bits of entropy")
    for tip in result["tips"]:
        print("  - " + tip)
