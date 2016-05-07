#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < zig_zag_scan.py 2016-05-07 09:03:07 >
"""
Z字形的扫描,zig-zag scan
""" 

import numpy as np

# Z字形排列的量化DCT系数之序号
order_of_dct_table = np.array([
	[0, 1, 5, 6, 14, 15, 27, 28],
	[2, 4, 7, 13, 16, 26, 29, 42],
	[3, 8, 12, 17, 25, 30, 41, 43],
	[9, 11, 18, 24, 31, 40, 44, 53],
	[10, 19, 23, 32, 39, 45, 52, 54],
	[20, 22, 33, 38, 46, 51, 55, 60],
	[21, 34, 37, 47, 50, 56, 59, 61],
	[35, 36, 48, 49, 57, 58, 62, 63],
],dtype=np.uint8)


# 整理成一个1x64的映射序列
def generate_seq():
	global order_of_dct_table
	seq_dict = {}
	for i,j in [(i,j) for i in xrange(8) for j in xrange(8)]:
		seq_dict[order_of_dct_table[i, j]] = (i * 8 + j)
	return seq_dict

def get_seq_1x64(input_matrix):
	pass

def test():
	t = generate_seq()
	for i in t:
		print "%d->%d" % (i, t[i])

if __name__ == '__main__':
	test()

