#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dc_ac_encode.py 2016-05-07 12:14:25 >
"""
DC AC系数的编码
""" 

import numpy as np

# 测试矩阵，课本P129 "量化矩阵"转化为1x64列表
test_list = [15, 0, -2, -1, -1, -1, 0, 0, -1]
# 补零至长度64
for i in xrange(55):test_list.append(0)

# 位长的计算
def calc_need_bits(input_num):
	num = abs(input_num)
	if num == 0:
		return 0
	returnValue = 1
	num += 1
	while True:
		if (1 << returnValue) >= num:
			break
		returnValue += 1
	return returnValue


# DC直流分量编码，输入上一个
def dc_encode(this_DC_value, previous_DC_value):
	pass

def ac_encode():
	pass

def DC_AC_encode(input_list,previous_DC_value):
	pass

def test():
	while True:
		n = input("input a num:")
		print calc_need_bits(n)

if __name__ == '__main__':
	test()
