#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_bmp.py 2016-05-07 21:43:33 >
"""
读写bmp文件
""" 

import os
import struct

class BMP(object):
	def __init__(self, filelocation, height=0, width=0, binary=None):
		self.filelocation = filelocation
		self.height = height
		self.width = width
		self.data_size = height * width
		self.binary = binary

	def get_header(self):
		pass

	def write_header(self):
		pass
	
	# 简易读取bmp，仅实现了灰度图像读取
	def read_bmp(self):
		with open(filelocation, 'rb') as f:
			# 分辨率
			f.seek(18)
			buf = f.read(8)
			size = struct.unpack('<II', buf)
			width = size[0]
			height = size[1]
			data_size = width * height
			# 数据偏移
			f.seek(10)
			buf = f.read(4)
			offset_ = struct.unpack('<I', buf)
			offset = offset_[0]
			# 读取二进制
			f.seek(offset)
			f.read(data_size)

	def write_bmp(self):
		pass

	def show_bmp(self):
		pass
	
def test():
	pass
	# read_bmp('data/color.bmp')

if __name__ == '__main__':
	test()

		
		
