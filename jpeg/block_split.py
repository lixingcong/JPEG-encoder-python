#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < block_split.py 2016-05-09 22:27:43 >
"""
块分割
"""

import numpy as np
import math

# 最终的方块边长，调试用。
# blk_width=8

# 往图像边缘填充像素至长度为8的倍数
def padding_dummy_edge(input_matrix, blk_width = 8):
	# 输入图像的长度宽度
	height = input_matrix.shape[0]
	width = input_matrix.shape[1]

	# 不需要做padding，直接返回
	if height % blk_width == 0 and width % blk_width == 0:
		return input_matrix

	# 计算新的矩阵尺寸
	if height % blk_width != 0:
		height_new = height + (blk_width - (height % blk_width))
	else:
		height_new = height
	if width % blk_width != 0:
		width_new = width + (blk_width - (width % blk_width))
	else:
		width_new = width


	# 创建一个新的图像矩阵为8的整数倍
	new_table = np.zeros(height_new * width_new,
					   dtype = np.float64).reshape(height_new, width_new)
	# 复制原有图像的信息到新图像
	for y, x in [(y, x) for x in xrange(width) for y in xrange(height)]:
		new_table[y, x] = input_matrix[y, x]

	# 先横向填充，再纵向填充
	for x in xrange(width, width_new):
		for y in xrange(height_new):
			new_table[y, x] = new_table[y, width - 1]
	for y in xrange(height, height_new):
		for x in xrange(width_new):
			new_table[y, x] = new_table[height - 1, x]
	return new_table

# 将图像打碎成8x8块，参数blk_width表示新的边长
def split_to_blocks(input_matrix, blk_width = 8):
	height = input_matrix.shape[0]
	width = input_matrix.shape[1]
	print "in spilt:%d %d" % (height, width)
	# 图像块的数目
	horizontal_blocks_num = height / blk_width
	vertical_blocks_num = width / blk_width

	print horizontal_blocks_num, vertical_blocks_num

	all_small_blocks = []
	# 先横向分割，再纵向分割
	vertical_blocks = np.hsplit(input_matrix, vertical_blocks_num)
	for block_vert in vertical_blocks:
		horizontal_blocks = np.vsplit(block_vert, horizontal_blocks_num)
		for block in horizontal_blocks:
			all_small_blocks.append(block)

	return all_small_blocks, horizontal_blocks_num, vertical_blocks_num

def test():
	# 测试矩阵，课本P129，已删除部份，留下7x9矩阵
	test_table1 = np.array([
		[139, 144, 149, 153, 155, 155, 155],
		[144, 151, 153, 156, 159, 156, 156],
		[150, 155, 160, 163, 158, 156, 156],
		[159, 161, 162, 160, 160, 159, 159],
		[159, 160, 161, 162, 162, 155, 155],
		[161, 161, 161, 161, 160, 157, 157],
		[161, 161, 161, 161, 160, 157, 157],
		[161, 161, 161, 161, 160, 157, 157],
		[161, 161, 161, 161, 160, 157, 157]
	])


	print "Original blocks:(7x9)"
	print test_table1

	# 第二个参数4表示定义打碎后的块边长4
	padded_table = padding_dummy_edge(test_table1)
	print "padded table:(%d x %d)" % (padded_table.shape[1], padded_table.shape[0])
	print padded_table
	print '*' * 10

	print "cutted blocks:"
	blocks, hor_num, ver_num = split_to_blocks(padded_table)
	for i in blocks:
		print i
		print ""

	# 留下9x7矩阵
	test_table2 = np.array([
		[139, 144, 149, 153, 155, 155, 155, 155, 155],
		[144, 151, 153, 156, 159, 156, 156, 156, 155],
		[150, 155, 160, 163, 158, 156, 156, 156, 155],
		[159, 161, 162, 160, 160, 159, 159, 159, 155],
		[159, 160, 161, 162, 162, 155, 155, 155, 155],
		[161, 161, 161, 161, 160, 157, 157, 157, 155],
		[162, 162, 161, 163, 162, 157, 157, 157, 155]
	])

	print "#"*20
	print "Original blocks:(9x7)"
	print test_table2

	# 第二个参数4表示定义打碎后的块边长4
# 	padded_table=padding_dummy_edge(test_table,8)
	padded_table = padding_dummy_edge(test_table2)
	print "padded table:(%d x %d)" % (padded_table.shape[1], padded_table.shape[0])
	print padded_table
	print '*' * 10

	print "cutted blocks:"
	blocks, hor_num, ver_num = split_to_blocks(padded_table)
	for i in blocks:
		print i
		print ""

if __name__ == '__main__':
	test()
