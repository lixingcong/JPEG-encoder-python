#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_jpg.py 2016-05-16 17:56:40 >
"""
JPEG读写二进制实现,baseline
注意：在ubuntu 16.04(Linux 4.4) 下运行GIMP图片处理，导出为jpg格式，质量随便选
但是，高级选项，取消勾选“优化”、“渐进”、“缩略图”等所有选项！！否则不兼容
"""

import numpy as np
import struct
import zig_zag_scan
import jpeg_code

# JPEG固定文件头数据

HEADER_SOI = '\xff\xd8'
HEADER_APP0 = '\xff\xe0'
HEADER_DQT = '\xff\xdb'
HEADER_SOF0 = '\xff\xc0'
HEADER_DHT = '\xff\xc4'
HEADER_SOS = '\xff\xda'
HEADER_EOC = '\xff\xd9'

HEADER_DHT_DC = '\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'
HEADER_DHT_AC = '\x00\xb5\x10\x00\x02\x01\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01\x7d\x01\x02\x03\x00\x04\x11\x05\x12\x21\x31\x41\x06\x13\x51\x61\x07\x22\x71\x14\x32\x81\x91\xa1\x08\x23\x42\xb1\xc1\x15\x52\xd1\xf0\x24\x33\x62\x72\x82\x09\x0a\x16\x17\x18\x19\x1a\x25\x26\x27\x28\x29\x2a\x34\x35\x36\x37\x38\x39\x3a\x43\x44\x45\x46\x47\x48\x49\x4a\x53\x54\x55\x56\x57\x58\x59\x5a\x63\x64\x65\x66\x67\x68\x69\x6a\x73\x74\x75\x76\x77\x78\x79\x7a\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa'
HEADER_APP0_DATA = '\x00\x10\x4A\x46\x49\x46\x00\x01\x01\x01\x00\x01\x00\x01\x00\x00'
HEADER_DQT_DATA = '\x00\x43\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'


class JPG(object):
	def __init__(self, filelocation, input_matrix = None):
		self.filelocation = filelocation
		self.matrix = input_matrix
		self.hex = ''
		if self.matrix is not None:
			self.height = self.matrix.shape[0]
			self.width = self.matrix.shape[1]
		else:
			self.height = 0
			self.width = 0

		# 偏移量字典
		self.offset_dict = {
			'APP0': None,
			'DQT': [],
			'SOF0': None,
			'DHT': [],
			'SOS': None,
			'EOC': None
		}
		self.DQT = {}
		self.colors = {}
		# self.DHT = {}


	# ------------------------------
	def read_offset(self, f):
		index = 2
		# 从APP0开始扫描
		f.seek(2)
		print "reading offset"
		while True:
			buffer = f.read(1)
			# 到达EOF
			if not buffer:
				break
			if buffer == '\xff':
				buffer += f.read(1)
				if buffer == HEADER_APP0:
					self.offset_dict['APP0'] = index
					index += 1
				elif buffer == HEADER_DQT:
					self.offset_dict['DQT'].append(index)
					index += 1
				elif buffer == HEADER_SOF0:
					self.offset_dict['SOF0'] = index
					index += 1
				elif buffer == HEADER_DHT:
					self.offset_dict['DHT'].append(index)
					index += 1
				elif buffer == HEADER_SOS:
					self.offset_dict['SOS'] = index
					index += 1
				elif buffer == HEADER_EOC:
					self.offset_dict['EOC'] = index
					break
				else:
					# 向后移动指针
					f.seek(-1, 1)
			index += 1
		for i in self.offset_dict:
			print " ", i, "->", self.offset_dict[i]

	def read_APP0(self):
		# 自定义的图像信息，这里忽略，但是写入需要这个APP0
		pass

	def read_DQT(self, f):
		print 'reading DQT'
		for offset in self.offset_dict['DQT']:
			f.seek(offset + 2)
			buffer = f.read(2)
			length = struct.unpack('>H', buffer)[0]
			buffer = ord(f.read(1))
			# 高四位精度，低四位id
			precision = 0 if (buffer >> 4) == 1 else 1
			precision + 1
			id = (buffer & 0x03)
			length -= 3
			this_dqt_list = []
			for i in xrange(0, length, precision):
				buffer = f.read(precision)
				if precision == 1:   # 8bit精度
					this_dqt_list.append(ord(buffer))
				else:   # 十六位精度，这个没有实现
					pass
			# 利用z-z顺序转成矩阵
			self.DQT[id] = zig_zag_scan.restore_matrix_from_1x64(this_dqt_list)
		# print self.DQT

	def read_SOF0(self, f):
		print "reading SOF0"
		f.seek(self.offset_dict['SOF0'] + 2)
		# length = struct.unpack('H', f.read(2))
		# 跳过自读取length和精度
		f.seek(3, 1)
		self.height = struct.unpack('>H', f.read(2))[0]
		self.width = struct.unpack('>H', f.read(2))[0]
		colors = ord(f.read(1))
		for color in xrange(colors):
			id = ord(f.read(1))
			# 采样系数，不太懂，灰度图还有采样系数？
			sp = ord(f.read(1))
			v = sp & 0x0f   # 垂直
			h = sp >> 4   # 水平
			dqt_id = ord(f.read(1))   # 量化表id
			self.colors[id] = [v, h, dqt_id]
		# print self.colors
		# print self.width, self.height

	def read_DHT(self, f):
		# TODO: build DHT dynamically
		# 动态读取/生成哈夫曼表可以有效压缩体积，我就不要耗时间在上面了
		print "reading DHT"
		return
		for offset in self.offset_dict['DHT']:
			f.seek(offset + 4)
			id = ord(f.read(1))
			for i in xrange(16):
				pass

	def read_SOS(self, f):
		f.seek(self.offset_dict['SOS'] + 2)
		# 灰度图直接省略读取颜色分量
		length = struct.unpack('>H', f.read(2))[0]
		f.seek(length - 2, 1)
		ff_counter = 0
		while True:
			buffer = f.read(1)
			if buffer == '\xff':
				buffer = f.read(1)
				# 转义，将'\xff00'转成'\xff'
				if buffer == '\x00':
					buffer = '\xff'
					ff_counter += 1
				elif  buffer == '\xd9':
					break
			self.hex += buffer.encode('hex')
		print "  0xff00 meets %d times" % ff_counter
		self.matrix = jpeg_code.jpeg_decode(self.hex, self.width, self.height, self.DQT[0])

	def read_data(self):
		with open(self.filelocation, 'rb') as f:
			self.read_offset(f)
			self.read_DQT(f)
			self.read_SOF0(f)
			# self.read_DHT(f)
			self.read_SOS(f)

	def get_data(self):
		return (self.matrix, self.width, self.height, self.DQT)

	def get_hex(self):
		return self.hex

	# ------------------------------
	def write_data(self):
		with open(self.filelocation, 'wb') as f:
			f.write('\xff\xd8')
			self.write_APP0(f)
			self.write_DQT(f)
			self.write_SOF0(f)
			self.write_DHT(f)
			self.write_SOS(f)
			f.write(HEADER_EOC)
			
	def write_APP0(self, f):
		f.write(HEADER_APP0)
		f.write(HEADER_APP0_DATA)

	def write_DQT(self, f):
		f.write(HEADER_DQT)
		f.write(HEADER_DQT_DATA)
			

	def write_SOF0(self, f):
		f.write(HEADER_SOF0)
		data = ['\x00\x0B\x08', '\x01\x01\x11\x00']
		width = struct.pack('>H', self.width)
		height = struct.pack('>H', self.height)
		f.write(data[0] + height + width + data[1])

	def write_DHT(self, f):
		# DC表 lenght=31
		f.write(HEADER_DHT)
		f.write(HEADER_DHT_DC)
		# AC表 lenght=181
		f.write(HEADER_DHT)
		f.write(HEADER_DHT_AC)
		
	def write_SOS(self, f):
		f.write(HEADER_SOS)
		# 偷懒了，直接使用别的文件二进制
		f.write('\x00\x08\x01\x01\x00\x00\x3F\x00')
		self.hex = jpeg_code.jpeg_encode(self.matrix)
		l = len(self.hex)
		binary = ''
		index = 0
		# 写入转义\xff\x00
		while index < l:
			this_byte = self.hex[index:index + 2].decode('hex')
			binary += this_byte
			if this_byte == '\xff':
				binary += '\x00'
			index += 2
		f.write(binary)
		
# 实现灰度图像jpg文件的对烤
def test():
	my_pic1 = JPG('/tmp/43.jpg')
	my_pic1.read_data()
	matrix = my_pic1.get_data()[0]

	print "\n\nencode a jpg"
	my_pic1 = JPG('/tmp/test_jpg_formpy.jpg', matrix)
	my_pic1.write_data()

if __name__ == '__main__':
	test()
