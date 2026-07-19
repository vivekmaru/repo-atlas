#!/usr/bin/env python3
"""Fetch the pinned Mermaid browser bundle for a generated repo atlas.

The script downloads Mermaid's npm tarball, verifies its published SHA-512
integrity value, then writes the browser bundle and Mermaid's MIT license next
to each other. It has no runtime dependencies beyond Python's standard library.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import tarfile
from pathlib import Path
from urllib.request import urlopen


VERSION = "11.16.0"
TARBALL_URL = f"https://registry.npmjs.org/mermaid/-/mermaid-{VERSION}.tgz"
TARBALL_SHA512 = "Zvm3kbstgdpvIJPPItlL7fppIZ3kibvc1oZIGxdvk9t6UFz6flv+Jw7FtRGKwfcI8OckmH04LqG6LlS6X4B1pA=="
BUNDLE_PATH = "package/dist/mermaid.min.js"
LICENSE_PATH = "package/LICENSE"


def extract_member(archive: tarfile.TarFile, path: str) -> bytes:
    member = archive.getmember(path)
    handle = archive.extractfile(member)
    if handle is None:
        raise ValueError(f"Could not extract {path} from Mermaid {VERSION}.")
    return handle.read()


def fetch_bundle(destination: Path, force: bool) -> None:
    license_destination = destination.with_name("mermaid.LICENSE")
    existing = [path for path in (destination, license_destination) if path.exists()]
    if existing and not force:
        names = ", ".join(str(path) for path in existing)
        raise FileExistsError(f"Refusing to overwrite {names}. Re-run with --force.")

    with urlopen(TARBALL_URL) as response:
        payload = response.read()
    actual = base64.b64encode(hashlib.sha512(payload).digest()).decode("ascii")
    if actual != TARBALL_SHA512:
        raise ValueError(
            f"Mermaid {VERSION} integrity check failed: expected {TARBALL_SHA512}, got {actual}."
        )

    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        bundle = extract_member(archive, BUNDLE_PATH)
        license_text = extract_member(archive, LICENSE_PATH)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(bundle)
    license_destination.write_bytes(license_text)
    print(f"Wrote Mermaid {VERSION} to {destination}")
    print(f"Wrote Mermaid license to {license_destination}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "destination",
        type=Path,
        help="Target path for mermaid.min.js, for example docs/repo-atlas/vendor/mermaid.min.js.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing Mermaid files.")
    args = parser.parse_args()
    fetch_bundle(args.destination, args.force)


if __name__ == "__main__":
    main()
