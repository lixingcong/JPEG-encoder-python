#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dc_ac_encode.py 2016-05-07 12:35:23 >
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


# DC直流分量编码
def dc_encode(this_DC_value, previous_DC_value):
	theta_DC = this_DC_value - previous_DC_value
	need_bit = calc_need_bits(theta_DC)
	return (need_bit, theta_DC)

def ac_encode(input_list):
	lite_list = input_list[:]
	output_list = []
	# 移除末位0
	while(lite_list[-1] == 0):
		lite_list.pop()
	index = 0
	length = len(lite_list)
	# 开始进行RLE编码
	while(index < length):
		zero_counter = 0
		# 找出连续0个数
		while(lite_list[index] == 0):
			zero_counter += 1
			index += 1
		current_num = lite_list[index]
		# 本次REL码字
		this_round = [zero_counter, calc_need_bits(current_num), current_num]
		output_list.append(tuple(this_round))
		index += 1
	return output_list
	
def DC_AC_encode(input_list,previous_DC_value):
	pass

def test():
	print test_list
	# print "after pop"
	s = ac_encode(test_list[1:])
	for i in s:print i
	

if __name__ == '__main__':
	test()
