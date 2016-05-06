#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < block_split.py 2016-05-07 00:20:35 >
"""
块分割
""" 

import numpy as np
import math

# 最终的方块边长
blk_width=8

# 测试矩阵，课本P129，已删除部份，留下6x7矩阵
test_table=np.array([
	[139,144,149,153,155,155,155],
	[144,151,153,156,159,156,156],
	[150,155,160,163,158,156,156],
	[159,161,162,160,160,159,159],
	[159,160,161,162,162,155,155],
	[161,161,161,161,160,157,157]
])

def padding_dummy_edge(input_matrix,blk_width_):
	height=input_matrix.shape[0]
	width=input_matrix.shape[1]
	if height%blk_width_==0 and width%blk_width_==0:
		return input_matrix
	height_new=height+(blk_width_-height%blk_width_)
	width_new=width+(blk_width_-width%blk_width_)
	new_table=np.zeros(height_new*width_new,
					   dtype=np.float64).reshape(height_new,width_new)
	for x,y in [(x,y) for x in xrange(height) for y in xrange(width)]:
		new_table[x,y]=input_matrix[x,y]
	# 先横向填充，再纵向填充
	for y in xrange(width,width_new):
		for x in xrange(height_new):
			new_table[x,y]=new_table[x,width-1]
	for x in xrange(height,height_new):
		for y in xrange(width_new):
			new_table[x,y]=new_table[height-1,y]
	return new_table
	
def split_to_blocks(input_matrix,blk_width_):
	height=input_matrix.shape[0]
	width=input_matrix.shape[1]
	horizontal_blocks_num=height/blk_width_
	vertical_blocks_num=width/blk_width_
	# 先横向分割，再纵向分割
	vertical_blocks=np.vsplit(input_matrix,vertical_blocks_num)
	for block_vert in vertical_blocks:
		horizontal_blocks=np.hsplit(block_vert,horizontal_blocks_num)
		for block in horizontal_blocks:
			print block
			print '-'*10

def test():
	padded_table=padding_dummy_edge(test_table,8)
	print "Original blocks:"
	print padded_table
	print '*'*10
	print "cutted blocks:"
	split_to_blocks(padded_table,4)

if __name__ == '__main__':
	test()
