#!/usr/bin/env python3
"""Entry-point for THE WORLD TODAY, Monday 23 November 2026 (news-23 b159 heroes-scene).

Stdlib-only: validates the bundled entry.png (PNG header, chunk CRCs, size,
dimensions) and copies it byte-for-byte to MAKEFUN_OUTPUT_DIR/entry.png.
Never writes next to this file.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "869368d8dede099c867ec40ddb14e8793de9ed66229c99987325031d64752ed9"  # entry.png, filled in after final render
EXPECTED_SIZE = 155836

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def check_png(path):
    """Validate PNG: signature, IHDR first chunk 1024x1024, CRC per chunk."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad PNG signature")
    if len(data) < 10000:
        raise ValueError("PNG too small")
    if len(data) > 1024 * 1024:
        raise ValueError("PNG over 1 MiB")
    # first chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8, colour 2/6
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    w, h, depth, colour, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        raise ValueError("PNG is not 1024x1024")
    if depth != 8 or colour not in (2, 6):
        raise ValueError("unsupported bit depth / colour type")
    if comp != 0 or filt != 0 or inter != 0:
        raise ValueError("unsupported compression/filter/interlace")
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(data[12:29]) & 0xFFFFFFFF != ihdr_crc:
        raise ValueError("CRC mismatch in chunk b'IHDR'")
    # walk remaining chunks, checking CRCs; IEND must be last, 0 bytes
    pos = 33
    idat_total = 0
    last_type = None
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + clen
        if end > len(data):
            raise ValueError("truncated chunk %r" % ctype)
        stored = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != stored:
            raise ValueError("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                raise ValueError("empty IDAT chunk")
            idat_total += clen
        last_type = ctype
        pos = end
        if ctype == b"IEND":
            if clen != 0:
                raise ValueError("IEND must be 0 bytes")
            break
    if last_type != b"IEND" or pos != len(data):
        raise ValueError("missing IEND or trailing data after IEND")
    if idat_total < 1000:
        raise ValueError("IDAT payload too small")
    return data


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        raise SystemExit("MAKEFUN_OUTPUT_DIR is empty")
    repo = os.path.dirname(os.path.abspath(__file__))
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        raise SystemExit("MAKEFUN_OUTPUT_DIR is a file")
    if out_dir_abs == repo or out_dir_abs.startswith(repo + os.sep):
        raise SystemExit("MAKEFUN_OUTPUT_DIR must be outside the repo")
    data = check_png(SOURCE)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        raise SystemExit("size mismatch: got %d, expected %d" % (len(data), EXPECTED_SIZE))
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 and sha != EXPECTED_SHA256:
        raise SystemExit("sha256 mismatch")
    os.makedirs(out_dir_abs, exist_ok=True)
    out_path = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(SOURCE):
        raise SystemExit("output would overwrite the source image")
    with open(out_path, "wb") as f:
        f.write(data)
    # re-read to confirm byte-identical output
    with open(out_path, "rb") as f:
        out_data = f.read()
    if out_data != data:
        raise SystemExit("output differs from source")
    print("wrote %s (%d bytes, sha256 %s)" % (out_path, len(data), sha))
    return 0


if __name__ == "__main__":
    sys.exit(main())
