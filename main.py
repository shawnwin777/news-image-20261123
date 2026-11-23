"""news-image-20261123 entry: copy the front-page image to /output/entry.png.

Deterministic, standard library only, no network. The image is the
newspaper front page "The World in One Day — 23 November 2026" held in
this repository as entry.png.
"""

import hashlib
import os
import shutil
from pathlib import Path


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / "entry.png"
    shutil.copyfile(source, destination)
    # Self-verification: the output must be byte-identical to the source.
    if sha256_of(source) != sha256_of(destination):
        raise SystemExit("entry.png copy failed sha256 verification")


if __name__ == "__main__":
    main()
