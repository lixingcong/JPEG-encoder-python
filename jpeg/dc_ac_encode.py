#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dc_ac_encode.py 2016-05-16 17:14:36 >
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


# DC直流分量编码，从
def dc_encode(this_DC_value, previous_DC_value):
	theta_DC = this_DC_value - previous_DC_value
	if theta_DC != 0:
		need_bit = calc_need_bits(theta_DC)
		return (need_bit, theta_DC)
	else:
		return (0,)

def ac_encode(input_list):
	length = len(input_list)
	if length == 0:
		yield (0, 0)
	else:
		lite_list = input_list[:]
		output_list = []
		# 移除末位0

		while(length > 0 and lite_list[-1] == 0):
			lite_list.pop()
			length = len(lite_list)
		length = len(lite_list)

		index = 0
		# 开始进行RLE编码
		while(index < length):
			zero_counter = 0
			# 找出连续0个数,no larger than 15
			while(lite_list[index] == 0 and zero_counter < 15):
				zero_counter += 1
				index += 1
			current_num = lite_list[index]
			# 本次RLE码字
			if current_num != 0:
				this_round = [zero_counter, calc_need_bits(current_num), current_num]
			else:
				# RZL
				this_round = [15, 0]
			# 生成器yeild
			yield tuple(this_round)
			index += 1


def DC_AC_encode(input_list, previous_DC_value):
	output_list = []
	# 直流编码
	dc = dc_encode(input_list[0], previous_DC_value)
	if len(dc) == 2:
		dc_value = (dc[0], dc[1])
	else:
		dc_value = (dc[0],)
	output_list.append(dc_value)
	# 交流编码
	ac_values = ac_encode(input_list[1:])
	# zig应少于64，算上DC为1
	zig_zag_counter = 1
	for ac_value in ac_values:
		zig_zag_counter += (ac_value[0] + 1)
		output_list.append(ac_value)
	if zig_zag_counter < 64:
		# 无振幅
		EOC = (0, 0)
		output_list.append(EOC)
	elif zig_zag_counter > 64:
		print "DC AC coding ERROR! out of range 64!"
	return output_list

def DC_AC_decode(input_list, previous_DC_value):
	output_list = []
	# 直流解码
	if input_list[0][0] == 0:
		output_list.append(0 + previous_DC_value)
	else:
		output_list.append(input_list[0][1] + previous_DC_value)
	# 交流解码
	for ac_encoded in input_list[1:]:
		# EOB或者RLZ
		if len(ac_encoded) == 2:
			if ac_encoded[0] == 0 and ac_encoded[1] == 0:
				break
			elif ac_encoded[0] == 15:
				for i in xrange(16):
					output_list.append(0)
				continue

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

# 课本P129 "量化矩阵"转化为1x64列表
def test():
	test_list = [15, 0, -2, -1, -1, -1, 0, 0, -1]
	# 补零至长度64
	for i in xrange(55):test_list.append(0)
	print "encode:"
	encoded = DC_AC_encode(test_list, 0)
	for i in encoded:print i

	print "#" * 20
	print "decode:"
	test_list_backward = [
		(4, 15),
		(1, 2, -2),
		(0, 1, -1),
		(0, 1, -1),
		(0, 1, -1),
		(2, 1, -1),
		(0, 0)
	]
	res = DC_AC_decode(test_list_backward, 0)
	print res
	print "len:", len(res)

# 测试带有连续16个零的，还有DC差值0的特殊情况
def test1():
	test_list = [
		[0, 0, -2, -1, -1, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
		[10, 0, -2, -1, -1, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[4, 0, -2, -1, -1, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 88]
	]
	l = len(test_list)
	print "original:"
	for i in test_list:
		print i

	last_dc = 0
	encoded = []
	for i in xrange(l):
		encoded.append(DC_AC_encode(test_list[i], last_dc))
		last_dc =  test_list[i][0]
	print "\nencoded:"
	for i in encoded:print i

	decoded = []
	last_dc = 0
	print '\ndecoded:'
	for i in encoded:
		j = DC_AC_decode(i, last_dc)
		decoded.append(j)
		last_dc = j[0]
		print j
if __name__ == '__main__':
	# test()
	test1()
