#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < quantize.py 2016-05-16 15:55:06 >
"""
量化
"""

import numpy as np

FORWARD = True
LUMINANCE = True

# 重复使用的矩阵，返回结果
output_table = np.zeros(64, dtype = np.int16).reshape(8, 8)

# 色差量化矩阵，课本P125
chrominance_table = np.array([
	[16, 11, 10, 16, 24, 40, 51, 61],
	[12, 12, 14, 19, 26, 58, 60, 55],
	[14, 13, 16, 24, 40, 57, 69, 56],
	[14, 17, 22, 29, 51, 87, 80, 62],
	[18, 22, 37, 56, 68, 109, 103, 77],
	[24, 36, 55, 64, 81, 104, 113, 92],
	[49, 64, 78, 87, 103, 121, 120, 101],
	[72, 92, 95, 98, 112, 100, 103, 99]
])
# 亮度量化矩阵，灰度使用全1的矩阵
luminance_table = np.ones(64).reshape(8,8)
# 亮度量化矩阵，课本P125
# luminance_table = np.array([
# 	[17, 18, 24, 47, 99, 99, 99, 99],
# 	[18, 21, 26, 66, 99, 99, 99, 99],
# 	[24, 26, 56, 99, 99, 99, 99, 99],
# 	[47, 66, 99, 99, 99, 99, 99, 99],
# 	[99, 99, 99, 99, 99, 99, 99, 99],
# 	[99, 99, 99, 99, 99, 99, 99, 99],
# 	[99, 99, 99, 99, 99, 99, 99, 99],
# 	[99, 99, 99, 99, 99, 99, 99, 99],
# ])

def get_quantisation(input_matrix, table_name = LUMINANCE, direction = FORWARD):
	global chrominance_table, luminance_table, output_table
	# 选择量化表
	if table_name is LUMINANCE:
		table = luminance_table
	elif table_name is False:
		table = chrominance_table
	else:
		table = table_name
	# 选择正向量化或反量化
	if direction is FORWARD:
		for u, v in [(u, v) for u in xrange(8) for v in xrange(8)]:
			output_table[u, v] = round(input_matrix[u, v] / table[u, v])
	else:
		for u, v in [(u, v) for u in xrange(8) for v in xrange(8)]:
			output_table[u, v] = input_matrix[u, v] * table[u, v]

	return output_table

def test():
	# 测试矩阵
	test_table = np.array([
		[235.6, -1, -12.1, -5.2, 2.1, -1.7, -2.7, 1.3],
		[-22.6, -17.5, -6.2, -3.2, -2.9, -0.1, -0.4, -1.2],
		[-10.9, -9.3, -1.6, 1.5, 0.2, 0.9, -0.6, -0.1],
		[-7.1, -1.9, 0.2, 1.5, -0.9, -0.1, 0, 0.3],
		[-0.6, -0.8, 1.5, 1.6, -0.1, -0.7, 0.6, 1.3],
		[1.8, -0.2, 1.6, -0.3, -0.8, 1.5, 1.0, -1.0],
		[-1.3, -0.4, -0.3, -1.5, -0.5, 1.7, 1.1, -0.8],
		[-2.6, 1.6, -3.8, -1.8, 1.9, 1.2, -0.6, -0.4]
	])
	print "课本P129 色差量化后结果："
	table_forward = get_quantisation(test_table, table_name = False, direction = FORWARD)
	print table_forward
	print '-' * 10
	print "色差反量化后结果："
	table_backward = get_quantisation(table_forward, table_name = False, direction = False)
	print table_backward

if __name__ == '__main__':
	test()
