#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Blood ART to PNG converter
# https://github.com/patwork/blood-art-to-png
#

import sys
import os
import struct
import png

# ----------------------------------------------------------------------------
palette = [
	0, 0, 0, 8, 8, 8, 16, 16, 16, 24, 24, 24,
	32, 32, 32, 40, 40, 40, 48, 48, 48, 56, 56, 56,
	64, 64, 64, 72, 72, 72, 80, 80, 80, 88, 88, 88,
	96, 96, 96, 104, 104, 104, 112, 112, 112, 120, 120, 120,
	128, 128, 128, 136, 136, 136, 144, 144, 144, 152, 152, 152,
	160, 160, 160, 168, 168, 168, 176, 176, 176, 188, 188, 188,
	196, 196, 196, 204, 204, 204, 212, 212, 212, 220, 220, 220,
	228, 228, 228, 236, 236, 236, 244, 244, 244, 252, 252, 252,
	24, 20, 20, 36, 28, 28, 48, 40, 40, 60, 52, 52,
	72, 60, 60, 84, 72, 72, 96, 84, 84, 112, 96, 96,
	124, 104, 104, 136, 116, 116, 148, 128, 128, 160, 136, 136,
	172, 148, 148, 184, 160, 160, 200, 172, 172, 252, 220, 220,
	0, 12, 36, 0, 16, 48, 4, 24, 56, 4, 32, 68,
	12, 40, 80, 20, 52, 92, 28, 60, 104, 36, 72, 116,
	48, 84, 128, 60, 96, 140, 76, 108, 152, 88, 124, 164,
	104, 136, 176, 120, 152, 188, 140, 168, 200, 180, 208, 240,
	20, 20, 44, 24, 28, 56, 32, 36, 72, 40, 48, 84,
	44, 60, 96, 52, 72, 112, 56, 84, 124, 64, 100, 140,
	72, 116, 152, 76, 132, 168, 80, 144, 180, 88, 156, 192,
	92, 172, 208, 100, 184, 220, 104, 200, 232, 112, 220, 252,
	12, 20, 56, 16, 24, 64, 20, 32, 76, 28, 40, 84,
	36, 44, 92, 44, 52, 104, 52, 64, 112, 60, 72, 124,
	72, 80, 132, 80, 92, 144, 92, 104, 152, 104, 112, 164,
	116, 128, 172, 132, 140, 184, 144, 152, 196, 184, 192, 240,
	16, 8, 8, 24, 12, 12, 32, 16, 16, 40, 24, 20,
	48, 28, 24, 56, 32, 32, 64, 36, 36, 76, 44, 40,
	84, 48, 44, 92, 52, 48, 100, 60, 52, 108, 64, 56,
	116, 68, 60, 124, 76, 64, 132, 80, 68, 140, 88, 72,
	148, 96, 80, 156, 108, 88, 168, 116, 96, 176, 128, 104,
	184, 136, 116, 192, 148, 124, 200, 160, 132, 212, 172, 144,
	156, 0, 0, 180, 40, 12, 204, 88, 32, 212, 112, 40,
	224, 132, 48, 232, 152, 56, 240, 172, 68, 252, 196, 80,
	8, 20, 48, 8, 24, 60, 8, 28, 72, 12, 32, 84,
	12, 32, 96, 12, 36, 108, 12, 36, 120, 12, 40, 132,
	8, 40, 144, 8, 40, 156, 8, 40, 168, 4, 36, 180,
	4, 36, 192, 0, 32, 208, 0, 32, 220, 0, 36, 252,
	0, 0, 48, 0, 0, 72, 0, 0, 96, 0, 0, 124,
	0, 0, 148, 0, 0, 172, 0, 0, 192, 0, 12, 204,
	0, 0, 236, 0, 80, 252, 0, 112, 252, 0, 152, 252,
	0, 180, 252, 0, 216, 252, 0, 252, 252, 104, 252, 252,
	20, 24, 12, 28, 32, 16, 36, 44, 24, 44, 52, 32,
	52, 64, 44, 60, 76, 52, 72, 84, 60, 80, 96, 72,
	88, 104, 84, 100, 116, 96, 112, 128, 104, 120, 136, 120,
	136, 148, 132, 148, 156, 144, 160, 168, 160, 208, 212, 208,
	4, 24, 80, 4, 36, 108, 4, 56, 140, 4, 76, 168,
	4, 96, 200, 4, 124, 216, 0, 140, 232, 0, 144, 252,
	0, 28, 0, 0, 40, 0, 4, 56, 4, 16, 72, 16,
	28, 88, 28, 40, 104, 40, 60, 120, 60, 80, 136, 80,
	0, 20, 36, 0, 28, 44, 4, 36, 56, 4, 44, 68,
	8, 52, 80, 16, 60, 88, 24, 68, 100, 32, 80, 112,
	40, 88, 120, 52, 100, 132, 60, 108, 144, 72, 120, 156,
	88, 132, 164, 100, 144, 176, 116, 156, 188, 132, 172, 200,
	4, 76, 180, 16, 84, 192, 32, 92, 208, 48, 104, 224,
	56, 116, 228, 64, 132, 232, 72, 144, 236, 80, 160, 240,
	92, 176, 240, 100, 184, 240, 116, 200, 244, 124, 212, 244,
	140, 216, 248, 148, 228, 248, 164, 232, 248, 172, 240, 252,
	28, 28, 140, 40, 44, 148, 56, 60, 160, 72, 80, 172,
	92, 100, 184, 108, 120, 196, 132, 144, 208, 156, 168, 220,
	8, 8, 20, 12, 12, 32, 20, 20, 48, 24, 28, 60,
	28, 36, 76, 36, 44, 88, 40, 56, 104, 44, 64, 116,
	48, 76, 132, 52, 80, 136, 56, 88, 140, 60, 92, 148,
	64, 100, 152, 72, 108, 156, 76, 112, 160, 80, 120, 168,
	88, 128, 172, 92, 136, 176, 100, 140, 184, 104, 148, 188,
	112, 156, 192, 120, 164, 200, 160, 200, 228, 160, 0, 188
]

# ----------------------------------------------------------------------------
def fatalError(e):

	if isinstance(e, str):
		sys.stderr.write(e)
		sys.exit(2)

	elif isinstance(e, IOError):
		sys.stderr.write('I/O error(%s): %s\n' % (e.errno, e.strerror))
		sys.exit(3)

	else:
		sys.stderr.write('Error: %s\n' % sys.exc_info()[0])
		sys.exit(4)

# ----------------------------------------------------------------------------
def initInfo():
	return {}

# ----------------------------------------------------------------------------
def addInfo(info, section, key, val):
	if not section in info:
		info[section] = {}
	info[section][key] = val

# ----------------------------------------------------------------------------
def writeInfo(filename, info):
	name = os.path.splitext(filename)[0] + '.ini'
	with open(name, 'w') as f:
		for section in sorted(info):
			f.write('[%s]\n' % section)
			for key in sorted(info[section]):
				f.write('%s=%s\n' % (key[2:], info[section][key]))
			f.write('\n')

# ----------------------------------------------------------------------------
def extractPNG(raw_8bpp, xsize, ysize, extended, index, info):

	name = 'tile%0.6d.png' % index
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

# ----------------------------------------------------------------------------
def unpackART(raw, info):

	art_header = struct.unpack_from('<LLLL', raw)
	art_version = art_header[0]
	art_start = art_header[2]
	art_end = art_header[3]
	art_count = art_end - art_start + 1

	if art_version != 1:
		fatalError('invalid ART version number: %d\n' % art_version)

	addInfo(info, 'header', '0.version', art_version)
	addInfo(info, 'header', '1.start', art_start)
	addInfo(info, 'header', '2.end', art_end)
	addInfo(info, 'header', '3.count', art_count)

	tiles_xsizes = struct.unpack_from('<%dH' % art_count, raw, 16)
	tiles_ysizes = struct.unpack_from('<%dH' % art_count, raw, 16 + art_count * 2)
	tiles_extended = struct.unpack_from('<%dL' % art_count, raw, 16 + art_count * 4)

	art_offset = 16 + art_count * (2 + 2 + 4)

	for i in range(0, art_count):
		size = tiles_xsizes[i] * tiles_ysizes[i]
		if size == 0:
			continue
		raw_8bpp = struct.unpack_from('%dB' % size, raw, art_offset)
		art_offset = art_offset + size
		extractPNG(raw_8bpp, tiles_xsizes[i], tiles_ysizes[i], tiles_extended[i], art_start + i, info)

# ----------------------------------------------------------------------------
def processFile(filename):

	info = initInfo()

	try:
		with open(filename, 'rb') as f:
			raw = f.read()
			unpackART(raw, info)

	except IOError as e:
		fatalError(e)

	except:
		fatalError(None)

	writeInfo(filename, info)

# ----------------------------------------------------------------------------
if __name__ == '__main__':

	if len(sys.argv) == 1:
		print 'usage: %s file1.art [file2.art] [...]' % (sys.argv[0])
		sys.exit(1)

	for filename in sys.argv[1:]:
		print 'processing file: %s' % (filename)
		processFile(filename)

	sys.exit(0)

# EoF
# vim: noexpandtab tabstop=4 softtabstop=4 shiftwidth=4
