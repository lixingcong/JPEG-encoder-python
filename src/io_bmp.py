#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_bmp.py 2016-05-07 23:45:35 >
"""
读写bmp文件
""" 

import os
import struct

def generate_colorspace(num):
	output_list = []
	for i in xrange(num):
		output_list.append(i)
		output_list.append(i)
		output_list.append(i)
		output_list.append(0)
	s = struct.pack('<{0}B'.format(4 * num), *output_list)
	return s

# Header of BMP固定格式
HEADER_SIGN = 0x4d42 # offset 0
HEADER_OFFSET = 0x00000436 # offset 10
HEADER_BITMAPINFOHEADER = 0x00000028 # offset 14
HEADER_NUMOFPLANES = 0x0001 # offset 26
HEADER_BITSPERPIXEL = 0x0008 # offset 28
HEADER_COMPRESSION = 0x00000000 # offset 30
HEADER_NUMBERSOFCOLORS = 0x00000100 # offset 46
HEADER_NUMBERSOFIMPORTANTCOLORS = 0x00000100 # offset 50



class BMP(object):
	def __init__(self, filelocation, height=0, width=0, binary=None):
		self.filelocation = filelocation
		self.height = height
		self.width = width
		self.data_size = height * width
		self.binary = binary
		self.buffer = None

	def read_header(self, f):
		# 分辨率
		f.seek(18)
		self.buffer = f.read(8)
		resolution = struct.unpack('<II', self.buffer)
		self.width = resolution[0]
		self.height = resolution[1]
		self.data_size = self.width * self.height

	def get_header(self):
		return (self.height, self.width)
		
	def write_header(self, f):
		
		HEADER_COLORSPACE = generate_colorspace(256)
		

	def get_data(self):
		return (self.height, self.width, self.binary)
	
	# 简易读取bmp，仅实现了灰度图像读取
	def read_bmp(self):
		with open(self.filelocation, 'rb') as f:
			self.read_header(f)
			# 数据偏移
			f.seek(10)
			self.buffer = f.read(4)
			offset_ = struct.unpack('<I', self.buffer)
			offset = offset_[0]
			# 读取二进制
			f.seek(offset)
			self.binary = f.read(self.data_size)

	def write_bmp(self):
		pass

	def show_bmp(self):
		pass
	
def test():
	# my_pic = BMP('data/color.bmp')
	# my_pic.read_bmp()
	# (height, width) = my_pic.get_header()
	# print height, width
	t = generate_colorspace(3)
	print repr(t)

if __name__ == '__main__':
	test()

		
		
