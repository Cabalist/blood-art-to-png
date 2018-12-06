#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Blood ART to PNG converter
# https://github.com/patwork/blood-art-to-png
#

import os
import struct
import sys
from typing import Dict, Tuple, Union

import png

from palette import palette


def fatalError(e: Union[None, str, Exception]) -> None:
    if isinstance(e, str):
        sys.stderr.write(e)
        sys.exit(2)

    elif isinstance(e, IOError):
        sys.stderr.write(f'I/O error({e.errno}): {e.strerror}\n')
        sys.exit(3)

    else:
        sys.stderr.write(f'Error: {sys.exc_info()[0]}\n')
        sys.exit(4)


# ----------------------------------------------------------------------------
def initInfo() -> dict:
    return {}


# ----------------------------------------------------------------------------
def addInfo(info: Dict[str, Dict[str, int]], section: str, key: str, val: int):
    if not section in info:
        info[section] = {}
    info[section][key] = val


def writeInfo(path: str, info: Dict[str, Dict[str, int]]) -> None:
    name = os.path.splitext(path)[0] + '.ini'
    with open(name, 'w') as f:
        for section in sorted(info):
            f.write(f'[{section}]\n')
            for key in sorted(info[section]):
                f.write(f'{key[2:]}={info[section][key]}\n')
            f.write('\n')


def extractPNG(raw_8bpp: Tuple[int], xsize: int, ysize: int, extended: int, index: int, info: Dict[str, Dict[str, int]]) -> None:
    name = f'tile{index:06d}.png'
    args = struct.unpack('BbbB', struct.pack('<L', extended))
    raw_32bpp = []
    has_alpha = False

    for y in range(0, ysize):
        offset = y
        row = []
        for x in range(0, xsize):
            col = raw_8bpp[offset]
            offset = offset + ysize
            if col == 255:
                row.append(0)
                row.append(0)
                row.append(0)
                row.append(0)
                has_alpha = True
            else:
                idx = col * 3
                row.append(palette[idx + 2])
                row.append(palette[idx + 1])
                row.append(palette[idx])
                row.append(255)
        raw_32bpp.append(row)

    png.from_array(raw_32bpp, 'RGBA').save(name)

    addInfo(info, name, '0.index', index)
    addInfo(info, name, '1.width', xsize)
    addInfo(info, name, '2.height', ysize)
    addInfo(info, name, '3.alpha', 1 if has_alpha else 0)
    addInfo(info, name, '4.xoffset', args[1])
    addInfo(info, name, '5.yoffset', args[2])
    addInfo(info, name, '6.ext1', args[0])
    addInfo(info, name, '7.ext2', args[3])


def unpackART(raw: bytes, info: Dict[str, Dict[str, int]]) -> None:
    art_header = struct.unpack_from('<LLLL', raw)
    art_version = art_header[0]
    art_start = art_header[2]
    art_end = art_header[3]
    art_count = art_end - art_start + 1

    if art_version != 1:
        fatalError(f'invalid ART version number: {art_version}\n')

    addInfo(info, 'header', '0.version', art_version)
    addInfo(info, 'header', '1.start', art_start)
    addInfo(info, 'header', '2.end', art_end)
    addInfo(info, 'header', '3.count', art_count)

    tiles_xsizes = struct.unpack_from(f'<{art_count:d}H', raw, 16)
    tiles_ysizes = struct.unpack_from(f'<{art_count:d}H', raw, 16 + art_count * 2)
    tiles_extended = struct.unpack_from(f'<{art_count:d}L', raw, 16 + art_count * 4)

    art_offset = 16 + art_count * (2 + 2 + 4)

    for i in range(0, art_count):
        size = tiles_xsizes[i] * tiles_ysizes[i]
        if size == 0:
            continue
        raw_8bpp = struct.unpack_from(f'{size:d}B', raw, art_offset)
        art_offset = art_offset + size
        extractPNG(raw_8bpp, tiles_xsizes[i], tiles_ysizes[i], tiles_extended[i], art_start + i, info)


def processFile(path: str) -> None:
    info = initInfo()

    try:
        with open(path, 'rb') as f:
            raw = f.read()
            unpackART(raw, info)

    except IOError as e:
        fatalError(e)

    except:
        fatalError(None)

    writeInfo(path, info)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print(f'usage: {sys.argv[0]} file1.art [file2.art] [...]')
        sys.exit(1)

    for filename in sys.argv[1:]:
        print(f'processing file: {filename}')
        processFile(filename)

    sys.exit(0)
