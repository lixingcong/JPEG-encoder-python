#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < zig_zag_scan.py 2016-05-11 23:38:07 >
"""
Z字形的扫描,zig-zag scan
"""

import numpy as np
FORWARD = True

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
])

# 整理成一个8x8到1x64的映射序列，高效，可以映射正向或逆向，已经生成，无需重新生成。
def generate_dict(direction):
	global order_of_dct_table
	seq_dict = {}
	if direction is FORWARD:
		for i, j in [(i, j) for i in xrange(8) for j in xrange(8)]:
			seq_dict[int(order_of_dct_table[i, j])] = int(i * 8 + j)
	else:
		for i, j in [(i, j) for i in xrange(8) for j in xrange(8)]:
			seq_dict[int(i * 8 + j)] = int(order_of_dct_table[i, j])
	print seq_dict

# 上面的generate函数生成的字典
scan_dict_forward = {0: 0, 1: 1, 2: 8, 3: 16, 4: 9, 5: 2, 6: 3, 7: 10, 8: 17, 9: 24, 10: 32, 11: 25, 12: 18, 13: 11, 14: 4, 15: 5, 16: 12, 17: 19, 18: 26, 19: 33, 20: 40, 21: 48, 22: 41, 23: 34, 24: 27, 25: 20, 26: 13, 27: 6, 28: 7, 29: 14, 30: 21, 31: 28, 32: 35, 33: 42, 34: 49, 35: 56, 36: 57, 37: 50, 38: 43, 39: 36, 40: 29, 41: 22, 42: 15, 43: 23, 44: 30, 45: 37, 46: 44, 47: 51, 48: 58, 49: 59, 50: 52, 51: 45, 52: 38, 53: 31, 54: 39, 55: 46, 56: 53, 57: 60, 58: 61, 59: 54, 60: 47, 61: 55, 62: 62, 63: 63}
scan_dict_backward = {0: 0, 1: 1, 2: 5, 3: 6, 4: 14, 5: 15, 6: 27, 7: 28, 8: 2, 9: 4, 10: 7, 11: 13, 12: 16, 13: 26, 14: 29, 15: 42, 16: 3, 17: 8, 18: 12, 19: 17, 20: 25, 21: 30, 22: 41, 23: 43, 24: 9, 25: 11, 26: 18, 27: 24, 28: 31, 29: 40, 30: 44, 31: 53, 32: 10, 33: 19, 34: 23, 35: 32, 36: 39, 37: 45, 38: 52, 39: 54, 40: 20, 41: 22, 42: 33, 43: 38, 44: 46, 45: 51, 46: 55, 47: 60, 48: 21, 49: 34, 50: 37, 51: 47, 52: 50, 53: 56, 54: 59, 55: 61, 56: 35, 57: 36, 58: 48, 59: 49, 60: 57, 61: 58, 62: 62, 63: 63}



# 把8x8的矩阵按照z字形顺序转成1x64的列表
def get_seq_1x64(input_matrix):
	list_DCT = []
	for i in xrange(64):
		order = scan_dict_forward[i]
		list_DCT.append(int(input_matrix[order / 8, order % 8]))
	return list_DCT

# 把1x64的列表转成8x8矩阵
def restore_matrix_from_1x64(input_list):
	output_matrix = np.zeros(64, dtype = np.int16).reshape(8, 8)
	for i, j in [(i, j) for i in xrange(8) for j in xrange(8)]:
		order = scan_dict_backward[8 * i + j]
		output_matrix[i, j] = input_list[order]
	return output_matrix

def test():
	# 测试矩阵，课本P129，附有正确答案
	test_table = np.array([
		[139, 144, 149, 153, 155, 155, 155, 155],
		[144, 151, 153, 156, 159, 156, 156, 156],
		[150, 155, 160, 163, 158, 156, 156, 156],
		[159, 161, 162, 160, 160, 159, 159, 159],
		[159, 160, 161, 162, 162, 155, 155, 155],
		[161, 161, 161, 161, 160, 157, 157, 157],
		[162, 162, 161, 163, 162, 157, 157, 157],
		[162, 162, 161, 161, 163, 158, 158, 158]
	])

	print "original table: 8x8"
	print test_table

	# 转成1x64
	list_DCT_forward = get_seq_1x64(test_table)
	print "forward: TO 64x1"
	print list_DCT_forward

	# 转成8x8
	print "backward: TO 8x8"
	np_DCT_backward = restore_matrix_from_1x64(list_DCT_forward)
	print np_DCT_backward

if __name__ == '__main__':
	test()
