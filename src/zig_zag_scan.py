#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < zig_zag_scan.py 2016-05-07 09:48:52 >
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

# 测试矩阵，课本P129，附有正确答案
test_table=np.array([
	[139,144,149,153,155,155,155,155],
	[144,151,153,156,159,156,156,156],
	[150,155,160,163,158,156,156,156],
	[159,161,162,160,160,159,159,159],
	[159,160,161,162,162,155,155,155],
	[161,161,161,161,160,157,157,157],
	[162,162,161,163,162,157,157,157],
	[162,162,161,161,163,158,158,158]
])

# 整理成一个8x8到1x64的映射序列，可以映射正向或逆向
def generate_dict(direction):
	global order_of_dct_table
	seq_dict = {}
	if direction == 'forward':
		for i,j in [(i,j) for i in xrange(8) for j in xrange(8)]:
			seq_dict[order_of_dct_table[i, j]] = (i * 8 + j)
	elif direction == 'backward':	
		for i,j in [(i,j) for i in xrange(8) for j in xrange(8)]:
			seq_dict[i * 8 + j] = order_of_dct_table[i, j]
	else:
		return
	return seq_dict

def get_seq_1x64(input_matrix, seq_dict):
	list_DCT = []
	for i in xrange(64):
		order = seq_dict[i]
		list_DCT.append(input_matrix[order / 8, order % 8])
	return list_DCT

def restore_matrix_from_1x64(input_list, seq_dict):
	output_matrix = np.zeros(64,dtype=np.uint8).reshape(8,8)
	for i in xrange(64):
		order = seq_dict[i]
		output_matrix[order / 8, order % 8] = input_list[i]
	return output_matrix

def test():
	dict_forward = generate_dict('forward')
	list_DCT_forward = get_seq_1x64(test_table, dict_forward)
	dict_backward = generate_dict('backward')
	for i in xrange(64):
		print "forward: %d->%d backward: %d->%d" % (i, dict_forward[i], i, dict_backward[i]) 
	# np_DCT_backward = restore_matrix_from_1x64(list_DCT_forward, dict_backward)
	# print np_DCT_backward
	
if __name__ == '__main__':
	test()

