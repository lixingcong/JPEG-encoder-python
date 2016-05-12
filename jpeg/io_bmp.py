#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_bmp.py 2016-05-12 10:37:38 >
"""
读写bmp文件
"""

import numpy as np
import struct

# 生成256灰度调色板，其中num是色深
def generate_colorspace(num = 256):
	output_list = []
	for i in xrange(num):
		insert_item = (struct.pack('4B', i & 0xff, i & 0xff, i & 0xff, 0))
		output_list.append(insert_item)

	# s = struct.pack('<{0}B'.format(4 * num), *output_list)
	return output_list

# 蔡丽梅《图像处理》P31例题2.1，计算BMP的真实二进制数据大小
def calc_real_datasize(width, height, isTrueColor = False):
	if isTrueColor:
		w = ((width * 8 + 31) >> 5) << 2
		return (w * height, w - width)
	else:
		return (width * height, 0)

# BMP固定文件头数据
HEADER_SIGN = 0x4d42   # offset 0
HEADER_OFFSET = 0x00000436   # offset 10
HEADER_BITMAPINFOHEADER = 0x00000028   # offset 14
HEADER_NUMOFPLANES = 0x0001   # offset 26
HEADER_BITSPERPIXEL = 0x0008   # offset 28
HEADER_COMPRESSION = 0x00000000   # offset 30
HEADER_NUMBERSOFCOLORS = 0x00000100   # offset 46
HEADER_NUMBERSOFIMPORTANTCOLORS = 0x00000100   # offset 50



class BMP(object):
	def __init__(self, filelocation, input_matrix = None):
		self.filelocation = filelocation
		self.matrix = input_matrix
		if self.matrix is not None:
			self.height = self.matrix.shape[0]
			self.width = self.matrix.shape[1]
			t = calc_real_datasize(self.width, self.height)
			self.data_size = t[0]
			self.padding_bytes_each_line = t[1]
		else:
			self.height = 0
			self.width = 0
			self.data_size = 0
			self.padding_bytes_each_line = 0
		self.header = None
		self.buffer = None
		# default value, changeable when there is no colorpan
		self.data_offset = 1078

	# 读取bmp文件头
	def read_header(self, f):
		# 分辨率
		f.seek(18)
		self.buffer = f.read(8)
		resolution = struct.unpack('<II', self.buffer)
		self.width = resolution[0]
		self.height = resolution[1]
		# 新建一个矩阵
		self.matrix = np.zeros(self.height * self.width, dtype = np.uint8).reshape(self.height, self.width)
		# 二进制流大小
		t = calc_real_datasize(self.width, self.height)
		self.data_size = t[0]
		self.padding_bytes_each_line = t[1]
		# 文件数据偏置地址
		f.seek(10)
		self.buffer = f.read(4)
		self.data_offset = struct.unpack('<I', self.buffer)[0]

	# 写入bmp文件头
	def write_header(self, f):
		self.header = struct.pack('<H', HEADER_SIGN)   # offset 0
		self.header += struct.pack('<Q', 0)   # offset 2
		self.header += struct.pack('<I', self.data_offset)   # offset 10
		self.header += struct.pack('<I', HEADER_BITMAPINFOHEADER)   # offset 14
		self.header += struct.pack('<I', self.width)   # offset 18
		self.header += struct.pack('<I', self.height)   # offset 22
		self.header += struct.pack('<H', HEADER_NUMOFPLANES)   # offset 26
		self.header += struct.pack('<H', HEADER_BITSPERPIXEL)   # offset 28
		self.header += struct.pack('<I', HEADER_COMPRESSION)   # offset 30
		self.header += struct.pack('<QI', 0, 0)   # offset 34
		self.header += struct.pack('<I', HEADER_NUMBERSOFCOLORS)   # offset 46
		self.header += struct.pack('<I', HEADER_NUMBERSOFIMPORTANTCOLORS)   # offset 50
		# 写入调色板（灰度0~255）
		HEADER_COLORSPACE_bin = generate_colorspace()
		for i in xrange(256):
			self.header += HEADER_COLORSPACE_bin[i]
		# print (self.binary).encode('hex')
		f.seek(0)
		f.write(self.header)

	def get_data(self):
		return (self.matrix, self.height, self.width)

	# 简易读取bmp，仅实现了灰度图像读取
	def read_bmp(self):
		with open(self.filelocation, 'rb') as f:
			self.read_header(f)
			f.seek(self.data_offset)
			for y in xrange(self.height - 1, -1, -1):
				for x in xrange(self.width):
					self.matrix[y, x] = ord(f.read(1))
				# 跳过几个padding字节
				f.seek(self.padding_bytes_each_line, 1)

	# 简易写入bmp，仅实现了灰度图像写入
	def write_bmp(self):
		with open(self.filelocation, 'wb') as f:
			self.write_header(f)
			# 写入二进制数据
			f.seek(self.data_offset)
			for y in xrange(self.height - 1, -1, -1):
				for x in xrange(self.width):
					f.write(chr(self.matrix[y, x]))
				# padding数据
				# for i in xrange(self.padding_bytes_each_line):
					# f.write('\x00')


	def show_bmp(self):
		pass

def test():

	# 测试图像对拷
	print "-" * 10
	my_pic1 = BMP('data/color.bmp')
	my_pic1.read_bmp()
	print "read data/color.bmp ok!"
	matrix = my_pic1.get_data()[0]

	my_pic2 = BMP('/tmp/color_copy.bmp', matrix)
	my_pic2.write_bmp()
	print "write /tmp/color_copy.bmp ok!"
	del matrix

	# 测试自定义写入图像 8x7
	print "-" * 10
	matrix_gray = np.array([
		[0, 255, 255, 255, 255, 255, 255, 255],
		[255, 255, 255, 255, 255, 255, 255, 255],
		[0, 0, 255, 255, 255, 255, 255, 255],
		[255, 255, 255, 255, 255, 255, 255, 255],
		[255, 255, 255, 255, 255, 255, 255, 255],
		[255, 255, 255, 255, 255, 0, 255, 255],
		[255, 255, 255, 255, 255, 0, 0, 255]
	])
	my_pic3 = BMP('/tmp/8x7.bmp', matrix_gray)
	my_pic3.write_bmp()
	print "write /tmp/8x7.bmp ok!"

	# 测试P129的图像
	print "-" * 10
	matrix_P129 = np.array([
		[146, 145, 143, 141, 140, 139, 140, 140],
		[135, 135, 134, 132, 131, 130, 131, 131],
		[124, 124, 123, 123, 121, 121, 121, 121],
		[116, 117, 117, 116, 116, 115, 114, 114],
		[115, 115, 116, 116, 115, 115, 114, 114],
		[120, 120, 121, 122, 122, 122, 122, 122],
		[128, 129 , 130, 131, 132, 133, 134, 135],
		[137, 138, 140, 141, 142, 144, 146, 147]
# 		[139, 144, 149, 153, 155, 155, 155, 155],
# 		[144, 151, 153, 156, 159, 156, 156, 156],
# 		[150, 155, 160, 163, 158, 156, 156, 156],
# 		[159, 161, 162, 160, 160, 159, 159, 159],
# 		[159, 160, 161, 162, 162, 155, 155, 155],
# 		[161, 161, 161, 161, 160, 157, 157, 157],
# 		[162, 162, 161, 163, 162, 157, 157, 157],
# 		[162, 162, 161, 161, 163, 158, 158, 158]
	])
	my_pic4 = BMP('/tmp/P129.bmp', matrix_P129)
	my_pic4.write_bmp()
	print "write /tmp/P129.bmp ok!"

if __name__ == '__main__':
	test()



