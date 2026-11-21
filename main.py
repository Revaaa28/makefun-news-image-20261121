#!/usr/bin/env python3
"""Entry point for the news-image-20261121 make.fun submission.

The rendered front page (entry.png) ships in this repository; the
competition rules explicitly allow shipping the image and having the
program copy it. This program validates the PNG (signature, chunk CRCs,
dimensions, size cap) and then writes it to the output location.

Python 3.13, standard library only, no network.
"""
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024  # 1 MiB
MAX_DIM = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate_png(path):
    """Return (width, height, size) for a well-formed PNG, else raise."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError(f"PNG too large: {size} bytes > {MAX_BYTES}")
    width = height = None
    with open(path, "rb") as fh:
        if fh.read(8) != PNG_SIGNATURE:
            raise ValueError("bad PNG signature")
        while True:
            header = fh.read(8)
            if len(header) < 8:
                raise ValueError("truncated chunk header")
            length, ctype = struct.unpack(">I4s", header)
            data = fh.read(length)
            if len(data) < length:
                raise ValueError("truncated chunk data")
            (stored_crc,) = struct.unpack(">I", fh.read(4))
            if zlib.crc32(ctype + data) & 0xFFFFFFFF != stored_crc:
                raise ValueError(f"CRC mismatch in chunk {ctype!r}")
            if ctype == b"IHDR":
                width, height = struct.unpack(">II", data[:8])
            if ctype == b"IEND":
                break
    if width is None or height is None:
        raise ValueError("missing IHDR")
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"dimensions {width}x{height} exceed {MAX_DIM}px")
    return width, height, size


def output_path():
    """MAKEFUN_OUTPUT_DIR wins when set; otherwise the default /output."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.png")


def main():
    _, _, expected = validate_png(SOURCE)
    out_path = output_path()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    written = 0
    with open(SOURCE, "rb") as src, open(out_path, "wb") as dst:
        while True:
            block = src.read(65536)
            if not block:
                break
            dst.write(block)
            written += len(block)
    if written != expected:
        raise IOError(f"copied {written} bytes, expected {expected}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
