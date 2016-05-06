#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < block_split.py 2016-05-06 23:36:17 >
"""
块分割
""" 

import numpy as np
import math

# 测试矩阵，课本P129，已删除部份，留下6x7矩阵
test_table=np.array([
	[139,144,149,153,155,155,155],
	[144,151,153,156,159,156,156],
	[150,155,160,163,158,156,156],
	[159,161,162,160,160,159,159],
	[159,160,161,162,162,155,155],
	[161,161,161,161,160,157,157]
])

def padding_dummy_edge(input_matrix):
	height=input_matrix.shape[0]
	width=input_matrix.shape[1]
	if height%8==0 and width%8==0:
		return input_matrix
	height_new=height+(8-height%8)
	width_new=width+(8-width%8)
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

	print input_matrix
	print '-'*10
	print new_table
	
def split_to_blocks(input_matrix):
	pass

def test():
	padding_dummy_edge(test_table)

if __name__ == '__main__':
	test()
