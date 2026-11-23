#!/usr/bin/env python3
"""The World in One Day -- 23 November 2026.

Deterministic entrypoint: copies the submitted front-page image
(repo/entry.png) into the output directory given by the
MAKEFUN_OUTPUT_DIR environment variable (default /output) as
entry.png, and exits nonzero if anything goes wrong.

Python standard library only; no network, no randomness.
"""

import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "entry.png")


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    if not os.path.isfile(SOURCE):
        print(f"error: source image not found: {SOURCE}", file=sys.stderr)
        return 1
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        shutil.copyfile(SOURCE, OUTPUT_FILE)
    except OSError as exc:
        print(f"error: failed to copy entry image: {exc}", file=sys.stderr)
        return 1
    if sha256_file(SOURCE) != sha256_file(OUTPUT_FILE):
        print("error: sha256 mismatch after copy", file=sys.stderr)
        return 1
    print(f"wrote {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
