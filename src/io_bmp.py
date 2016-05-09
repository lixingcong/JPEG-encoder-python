#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_bmp.py 2016-05-09 21:25:07 >
"""
读写bmp文件
""" 

import numpy as np
import struct

def generate_colorspace(num):
	output_list = []
	for i in xrange(num):
		insert_item = (struct.pack('4B', i & 0xff, i & 0xff, i & 0xff, 0))
		output_list.append(insert_item)
	
	#s = struct.pack('<{0}B'.format(4 * num), *output_list)
	return output_list

# 蔡丽梅《图像处理》P31例题2.1，计算BMP的真实二进制数据大小
def calc_real_datasize(width, height):
	bit_per_pixel = 8
	w = ((width * bit_per_pixel + 31) >> 5) << 2
	return (w * height)

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
		self.data_size = calc_real_datasize(self.width, self.height)
		self.binary = binary
		self.header = None
		self.buffer = None
		# default value, changeable
		self.data_offset = 1078

	def read_header(self, f):
		# 分辨率
		f.seek(18)
		self.buffer = f.read(8)
		resolution = struct.unpack('<II', self.buffer)
		self.width = resolution[0]
		self.height = resolution[1]
		self.data_size = self.width * self.height
		# 文件数据偏置
		f.seek(10)
		self.buffer = f.read(4)
		self.data_offset = struct.unpack('<I', self.buffer)[0]
		

	# def get_header(self):
	# 	return (self.height, self.width)
		
	def write_header(self, f):
		self.header = struct.pack('<H', HEADER_SIGN) #offset 0
		self.header += struct.pack('<Q', 0) # offset 2
		self.header += struct.pack('<I', self.data_offset) # offset 10
		self.header += struct.pack('<I', HEADER_BITMAPINFOHEADER) # offset 14
		self.header += struct.pack('<I', self.width) # offset 18
		self.header += struct.pack('<I', self.height) # offset 22
		self.header += struct.pack('<H', HEADER_NUMOFPLANES) # offset 26
		self.header += struct.pack('<H', HEADER_BITSPERPIXEL) # offset 28
		self.header += struct.pack('<I', HEADER_COMPRESSION) # offset 30
		self.header += struct.pack('<QI', 0, 0) # offset 34
		self.header += struct.pack('<I', HEADER_NUMBERSOFCOLORS) # offset 46
		self.header += struct.pack('<I', HEADER_NUMBERSOFIMPORTANTCOLORS) # offset 50
		# 写入颜色RLE码字
		HEADER_COLORSPACE_bin = generate_colorspace(256)
		for i in xrange(256):
			self.header += HEADER_COLORSPACE_bin[i]
		# print (self.binary).encode('hex')
		f.seek(0)
		f.write(self.header)

	def get_data(self):
		return (self.height, self.width, self.binary)
	
	# 简易读取bmp，仅实现了灰度图像读取
	def read_bmp(self):
		with open(self.filelocation, 'rb') as f:
			self.read_header(f)
			f.seek(self.data_offset)
			self.binary = f.read(self.data_size)

	def write_bmp(self):
		with open(self.filelocation, 'wb') as f:
			self.write_header(f)
			f.seek(self.data_offset)
			f.write(self.binary)

	def show_bmp(self):
		pass
	
def test():
	my_pic = BMP('data/color.bmp')
	my_pic.read_bmp()
	height, width, bin_1 = my_pic.get_data()

	my_pic1 = BMP('/tmp/3g.bmp', height, width, bin_1)
	my_pic1.write_bmp()

if __name__ == '__main__':
	test()

		
		
