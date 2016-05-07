#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_bmp.py 2016-05-07 21:27:34 >
"""
读写bmp文件
""" 

import os
import struct

		
def read_bmp(filelocation):
	with open(filelocation, 'rb') as f:
		f.seek(18)
		buf = f.read(8)
		size = struct.unpack('<II', buf)
		print size[0], size[1]

		f.seek(10)
		buf = f.read(4)
		size = struct.unpack('<I', buf)
		print size[0]

def write_bmp(filelocation):
	pass

def test():
	read_bmp('data/color.bmp')

if __name__ == '__main__':
	test()

		
		
