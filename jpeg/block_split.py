#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < block_split.py 2016-05-16 17:16:32 >
"""
块分割
"""

import numpy as np

# 计算新的矩阵尺寸
def calc_new_size(width, height, blk_width = 8):
	if height % blk_width != 0:
		height_new = height + (blk_width - (height % blk_width))
	else:
		height_new = height
	if width % blk_width != 0:
		width_new = width + (blk_width - (width % blk_width))
	else:
		width_new = width
	return width_new, height_new

# 往图像边缘填充像素至长度为8的倍数
def padding_dummy_edge(input_matrix, blk_width = 8):
	# 输入图像的长度宽度
	height = input_matrix.shape[0]
	width = input_matrix.shape[1]

	# 不需要做padding，直接返回
	if height % blk_width == 0 and width % blk_width == 0:
		return input_matrix

	# 计算新的矩阵尺寸
	width_new, height_new = calc_new_size(width, height)

	# 创建一个新的图像矩阵为8的整数倍
	new_table = np.zeros(height_new * width_new,
					   dtype = np.float64).reshape(height_new, width_new)
	# 复制原有图像的信息到新图像
	new_table[:height, :width] = input_matrix[:height, :width]

	# 先横向填充，再纵向填充
	for x in xrange(width, width_new):
		new_table[:height, x] = new_table[:height, width - 1]
	for y in xrange(height, height_new):
		new_table[y, :width_new] = new_table[height - 1, :width_new]
	return new_table

# 将图像打碎成8x8块，参数blk_width表示新的边长
def split_to_blocks(input_matrix, blk_width = 8):
	height = input_matrix.shape[0]
	width = input_matrix.shape[1]
	print "in function spilt(): "
	print "new matrix created: width:%d height:%d" % (width, height)

	# 图像块的数目
	# 水平
	horizontal_blocks_num = width / blk_width
	# 垂直
	vertical_blocks_num = height / blk_width

	print "split to: rows:%d columns:%d" % (horizontal_blocks_num, vertical_blocks_num)

	all_small_blocks = []
	# 先横向分割成很多行，再纵向分割成很多列
	vertical_blocks = np.vsplit(input_matrix, vertical_blocks_num)#hsplit是水平切刀方向

	for block_ver in vertical_blocks:
		hor_blocks = np.hsplit(block_ver,horizontal_blocks_num)
		for block in hor_blocks:
			all_small_blocks.append(block)

	return all_small_blocks, horizontal_blocks_num, vertical_blocks_num

# 拼合成一个原图，并且去掉padding块（row：block的竖直方向个数(行数)，column：block水平方向个数(列数)）
def merge_blocks(input_list, rows, columns):
	all_rows_concatenated = []
	# 先拼合水平方向，成为一行一行的
	for row in xrange(rows):
		this_row_items = input_list[(columns * row):(columns * (row + 1))]
		all_rows_concatenated.append(np.concatenate(this_row_items, axis = 1))

	output_matrix = np.concatenate(all_rows_concatenated, axis = 0)
	return output_matrix

# 移除边界补全的多余像素
def remove_dummy_edge(input_matrix, width_new, height_new):
	# 输入图像的长度宽度
	height = input_matrix.shape[0]
	width = input_matrix.shape[1]

	# 不需要做padding，直接返回
	if height == height_new and width == width_new:
		return input_matrix

	# 复制原有图像的信息到新图像
	new_table = input_matrix[:height_new, :width_new]

	return new_table

# 测试打散矩阵
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
		[161, 164, 161, 161, 160, 157, 157],
		[164, 161, 161, 161, 160, 157, 157]
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

# 测试合并矩阵
def test1():
	test_table1 = np.array([
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255], 
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255]
	])
	test_table2 = np.array([
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255], 
		[0, 255, 255, 255, 255, 255, 255, 255],
		[0, 255, 255, 255, 255, 255, 255, 255]
	])
	test_list = [test_table1, test_table2]
	# 合并矩阵
	print "merge to 2x1"
	print merge_blocks(test_list, 1, 2)
	print "##" * 46
	print "merge to 1x2"
	merged = merge_blocks(test_list, 2, 1)
	print merged
	# 移除dummpy块
	print "remove dummy to 7x6"
	print remove_dummy_edge(merged, 7, 6)

if __name__ == '__main__':
	# test()
	test1()
