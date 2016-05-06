#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dct.py 2016-05-06 19:39:56 >
"""
离散余弦变换
""" 

import numpy as np
from numpy import pi
import math

w_equal_zero=1.0/math.sqrt(2.0)
w_equal_one=1.0
# 重复使用的余弦函数表,8x8
cosine_table=np.zeros(64,dtype=np.float64).reshape(8,8)

def generate_tables():
	global cosine_table
	for i in xrange(8):
		cosine_table[i,0]=1.0;
		for j in xrange(1,8):
			cosine_table[i,j]=math.cos(((2*j+1)*i)*pi/16)

def C(w):
	return w_equal_one if w!=0 else w_equal_zero
	
def forward_dct(input_matrix):
	global cosine_table
	
	
def test():
	print C(1)
	print C(0)
	generate_tables()
	print cosine_table
	

if __name__ == '__main__':
	test()
	
