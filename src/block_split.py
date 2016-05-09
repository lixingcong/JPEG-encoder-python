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
def padding_dummy_edge(input_matrix,blk_width=8):
	# 输入图像的长度宽度
	height=input_matrix.shape[0]
	width=input_matrix.shape[1]
	
	# 不需要做padding，直接返回
	if height%blk_width==0 and width%blk_width==0:
		return input_matrix

	# 计算新的矩阵尺寸
	height_new=height+(blk_width-height%blk_width)
	width_new=width+(blk_width-width%blk_width)
	
	# 创建一个新的图像矩阵为8的整数倍
	new_table=np.zeros(height_new*width_new,
					   dtype=np.float64).reshape(height_new,width_new)
	# 复制原有图像的信息到新图像
	for y,x in [(y,x) for x in xrange(width) for y in xrange(height)]:
		new_table[y,x]=input_matrix[y, x]
		
	# 先横向填充，再纵向填充
	for x in xrange(width,width_new):
		for y in xrange(height_new):
			new_table[y,x]=new_table[y,width-1]
	for y in xrange(height,height_new):
		for x in xrange(width_new):
			new_table[y,x]=new_table[height-1,x]
	return new_table

# 将图像打碎成8x8块，参数blk_width表示新的边长
def split_to_blocks(input_matrix,blk_width=8):
	height=input_matrix.shape[0]
	width=input_matrix.shape[1]	

	# 图像块的数目
	horizontal_blocks_num=height/blk_width
	vertical_blocks_num=width/blk_width
	
	all_small_blocks=[]
	# 先横向分割，再纵向分割
	vertical_blocks=np.vsplit(input_matrix,vertical_blocks_num)
	for block_vert in vertical_blocks:
		horizontal_blocks=np.hsplit(block_vert,horizontal_blocks_num)
		for block in horizontal_blocks:
			all_small_blocks.append(block)
			
	return all_small_blocks,horizontal_blocks,vertical_blocks_num

def test():
	# 测试矩阵，课本P129，已删除部份，留下6x7矩阵
	test_table=np.array([
		[139,144,149,153,155,155,155],
		[144,151,153,156,159,156,156],
		[150,155,160,163,158,156,156],
		[159,161,162,160,160,159,159],
		[159,160,161,162,162,155,155],
		[161,161,161,161,160,157,157]
	])
	
	print "Original blocks:(7x6)"
	print test_table

	print "padded table:(8x8)"
	# 第二个参数4表示定义打碎后的块边长4
	padded_table=padding_dummy_edge(test_table,8)
	print padded_table
	print '*'*10
	
	print "cutted blocks:(4x4)"
	blocks,hor_num,ver_num=split_to_blocks(padded_table,4)
	for i in blocks:
		print i
		print ""

if __name__ == '__main__':
	test()
