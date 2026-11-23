"""nova-toolkit — a tiny command-line toolkit.

Usage:
    python nova.py password <password>
    python nova.py hash <file> [expected-hash]
"""

import sys

from file_hash import hash_file, verify
from password_check import check

BANNER = r"""
 _ __   _____   ____ _
| '_ \ / _ \ \ / / _` |   nova-toolkit
| | | | (_) \ V / (_| |   >_ stay curious
|_| |_|\___/ \_/ \__,_|
"""


def main(argv: list) -> int:
    print(BANNER)
    if len(argv) < 2 or argv[0] not in {"password", "hash"}:
        print(__doc__)
        return 1

    command, target = argv[0], argv[1]
    if command == "password":
        result = check(target)
        print(f"[{result['label'].upper()}] ~{result['entropy']} bits of entropy")
        for tip in result["tips"]:
            print("  - " + tip)
    else:
        for name, digest in hash_file(target).items():
            print(f"{name:>7}: {digest}")
        if len(argv) > 2:
            print("\nMATCH ✔" if verify(target, argv[2]) else "\nNO MATCH ✘")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
