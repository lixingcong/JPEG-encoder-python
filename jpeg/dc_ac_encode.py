#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dc_ac_encode.py 2016-05-11 23:58:14 >
"""
DC AC系数的编码
""" 

import numpy as np

# 位长的计算
def calc_need_bits(input_num):
	num = abs(input_num)
	# 注意：DC才允许input_num=0，AC系数中不存在0
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
		# 找出连续0个数,no larger than 15
		while(lite_list[index] == 0 and zero_counter < 15):
			zero_counter += 1
			index += 1
		current_num = lite_list[index]
		# 本次RLE码字
		this_round = [zero_counter, calc_need_bits(current_num), current_num]
		# 生成器yeild
		yield tuple(this_round)
		index += 1

	
def DC_AC_encode(input_list,previous_DC_value):
	output_list = []
	# 直流编码
	(dc_bit, dc) = dc_encode(input_list[0], previous_DC_value)
	dc_value = (dc_bit, dc)
	output_list.append(dc_value)
	# 交流编码
	ac_values = ac_encode(input_list[1:])
	for ac_value in ac_values:
		output_list.append(ac_value)
	# 无振幅
	EOC = (0, 0)
	output_list.append(EOC)
	return output_list

def DC_AC_decode(input_list, previous_DC_value):
	output_list = []
	# 直流解码
	output_list.append(input_list[0][1] + previous_DC_value)
	# 交流解码
	for ac_encoded in input_list[1:-1]:
		zero_counter = ac_encoded[0]
		current_num = ac_encoded[2]
		for i in xrange(zero_counter):
			output_list.append(0)
		output_list.append(current_num)
	# 补全0
	zero_in_the_end_count = 64 - len(output_list)
	for i in xrange(zero_in_the_end_count):
		output_list.append(0)
	return output_list
	
			
def test():
	# 测试矩阵，课本P129 "量化矩阵"转化为1x64列表
	test_list = [15, 0, -2, -1, -1, -1, 0, 0, -1]
	# 补零至长度64
	for i in xrange(55):test_list.append(0)
	print "encode:"
	encoded = DC_AC_encode(test_list, 0)
	for i in encoded:print i

	print "#" * 20
	print "decode:"
	test_list_backward=[
		(4, 15),
		(1, 2, -2),
		(0, 1, -1),
		(0, 1, -1),
		(0, 1, -1),
		(2, 1, -1),
		(0, 0)
	]
	res =  DC_AC_decode(test_list_backward, 0)
	print res
	print "len:", len(res)

if __name__ == '__main__':
	test()
