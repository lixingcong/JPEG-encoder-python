#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_jpg.py 2016-05-14 20:16:21 >
"""
JPEG读写二进制实现
""" 


class JPG(object):
	def __init__(self):
		pass

	def read_offset(self, f):
		pass
	
	def read_APP0(self, f):
		pass

	def read_DQT(self, f):
		pass

	def read_SOF0(self, f):
		pass

	def read_DHT(self, f):
		pass

	def read_SOS(self, f):
		pass

	def read_compressed_bin(self, f):
		pass

	def read_data(self):
		pass

	def get_data(self):
		pass
	
	# ------------------------------

	def write(self, f):
		pass

	def write_APP0(self, f):
		pass

	def write_DQT(self, f):
		pass

	def write_SOF0(self, f):
		pass

	def write_DHT(self, f):
		pass

	def write_SOS(self, f):
		pass

	def write_compressed_bin(self, f):
		pass

	def write_data(self):
		pass

def test():
	pass

if __name__ == '__main__':
	test()
