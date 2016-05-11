#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dct.py 2016-05-11 23:29:56 >
"""
离散余弦变换
"""

import numpy as np
from numpy import pi
import math

w_equal_zero = 1.0 / math.sqrt(2.0)

# 重复使用的余弦函数表,8x8
cosine_table = np.zeros(64, dtype = np.float32).reshape(8, 8)
# 临时变量表,8x8
G_table = np.zeros(64, dtype = np.float32).reshape(8, 8)
F_table = np.zeros(64, dtype = np.float32).reshape(8, 8)

# 常量表，cos((2j+1)vπ/16)，是关于j和v的函数，作成Look-Up table提高效率
def generate_tables():
	global cosine_table
	for i, j in [(i, j) for i in xrange(8) for j in xrange(8)]:
		cosine_table[i, j] = math.cos(((2 * j + 1) * i) * pi / 16.0)

# 生成常量表cos
generate_tables()

def C(w):
	return 1.0 if w > 0 else w_equal_zero

def forward_dct(input_matrix):
	global cosine_table, G_table, F_table
	# 第一轮循环，在课本P124下方的 G(i,v)
	for i, v in [(i, v) for i in xrange(8) for v in xrange(8)]:
		sum = 0.0
		for j in xrange(8):
			sum = sum + (input_matrix[i, j] * cosine_table[v, j])
		G_table[i, v] = 0.5 * C(v) * sum

	# 第二轮循环，在课本P124下方的 F(u,v)
	for u, v in [(u, v) for u in xrange(8) for v in xrange(8)]:
		sum = 0.0
		for i in xrange(8):
			sum = sum + (G_table[i, v] * cosine_table[u, i])
		F_table[u, v] = 0.5 * C(u) * sum
	return F_table

def inverse_dct(input_matrix):
	global cosine_table, G_table, F_table
	# 第一轮循环，在课本P124下方的 G(i,v)逆运算
	for u, j in [(u, j) for u in xrange(8) for j in xrange(8)]:
		sum = 0.0
		for v in xrange(8):
			sum = sum + C(v) * (input_matrix[u, v] * cosine_table[v, j])
		G_table[u, j] = 0.5 * sum

	# 第二轮循环，在课本P124下方的 F(u,v)逆运算
	for i, j in [(i, j) for i in xrange(8) for j in xrange(8)]:
		sum = 0.0
		for u in xrange(8):
			sum = sum + C(u) * (G_table[u, j] * cosine_table[u, i])
		F_table[i, j] = 0.5 * sum
	F_table_int = np.zeros(64, dtype = np.int16).reshape(8, 8)
	F_table_int[:, :] = F_table[:, :]
	return F_table_int


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
	], dtype = np.int16)

	# 余弦变换
	DCT_table = forward_dct(test_table - 128)
	print "Forward-DCT"
	for x in xrange(8):
		for y in xrange(8):
			print "(%d,%d) %.2f" % (x, y, DCT_table[x, y])

	print '-' * 10
	# 余弦逆变换
	print "Inverse-DCT"
	IDCT_table = inverse_dct(DCT_table)
	print IDCT_table + 128

if __name__ == '__main__':
	test()

