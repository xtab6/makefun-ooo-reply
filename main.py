#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply.

Writes a single out-of-office auto-reply line to /output/entry.txt.
Python standard library only; no network, no input files.
"""

import os
import shutil
import sys

LINE = (
    "Out of office until Monday. My inbox has a restraining order against me "
    "\u2014 I am legally required to stay 500 feet away from it."
)


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    # Clean only the contents of the output folder, never the folder itself:
    # the grader mounts that folder and removing it fails with EPERM.
    for name in os.listdir(out_dir):
        path = os.path.join(out_dir, name)
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    text = LINE
    if not 1 <= len(text) <= 160:
        raise ValueError(f"entry must be 1-160 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    with open(
        os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline=""
    ) as handle:
        handle.write(text)
    # Read-back verification: the file on disk must be exactly the line.
    with open(
        os.path.join(out_dir, "entry.txt"), encoding="utf-8", newline=""
    ) as handle:
        if handle.read() != text:
            raise ValueError("entry.txt round-trip mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
