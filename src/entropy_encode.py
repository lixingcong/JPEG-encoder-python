#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < entropy_encode.py 2016-05-07 15:57:40 >
"""
熵编码
""" 

import numpy as np

# 色差交流系数，课本P132
# luminance_table={
# }

# 亮度交流系数，课本P132
huffman_AC_chrominance_table={
	"0/1":"00",
	"0/2":"01",
	"0/3":"100",
	"0/4":"1011",
	"0/5":"11010",
	"0/6":"1111000",
	"0/7":"11111000",
	"0/8":"1111110110",
	"0/9":"1111111110000010",
	"0/10":"1111111110000011",
	
	"1/1":"1100",
	"1/2":"11011",
	"1/3":"1111001",
	"1/4":"111110110",
	"1/5":"11111110110",
	"1/6":"1111111110000100",
	"1/7":"1111111110000101",
	"1/8":"1111111110000110",
	"1/9":"1111111110000111",
	"1/10":"1111111110001000",
	
	"2/1":"11100",
	"2/2":"11111001",
	"2/3":"1111110111",
	"2/4":"111111110100",
	"2/5":"1111111110001001",
	"2/6":"1111111110001010",
	"2/7":"1111111110001011",
	"2/8":"1111111110001100",
	"2/9":"1111111110001101",
	"2/10":"1111111110001110",
	
	"3/1":"111010",
	"3/2":"111110111",
	"3/3":"111111110101",
	"3/4":"1111111110001111",
	"3/5":"1111111110010000",
	"3/6":"1111111110010001",
	"3/7":"1111111110010010",
	"3/8":"1111111110010011",
	"3/9":"1111111110010100",
	"3/10":"1111111110010101",
	
	"4/1":"111011"
}

huffman_DC_chrominance_table = {
	0: "00",
	1: "010",
	2: "011",
	3: "100",
	4: "101",
	5: "110",
	6: "1100",
	7: "11110",
	8: "111110",
	9: "1111110",
	10: "11111110",
	11: "111111110"
}

# 计算幅值，课本P133
def calc_amplitude(input_num, need_bit, mode="AC"):
	num = abs(input_num) & 0xffff
	if mode == 'DC' and input_num == 0:
		return "0"
	index = 0
	output_string = ""
	# 正数
	if  input_num >= 0:
		while index < need_bit:
			this_bit = "1" if ((num >> index) & 0x1) else "0"
			output_string = this_bit + output_string
			index += 1
	# 负数
	else:
		while index < need_bit:
			this_bit = "0" if ((num >> index) & 0x1) else "1"
			output_string = this_bit + output_string
			index += 1

	return output_string
		
def get_entropy_encode(input_list):
	output_list = []
	# DC 编码
	dc_bit = input_list[0][0]
	dc_amp = input_list[0][1]
	(dc_bit, dc_amp) = (huffman_DC_chrominance_table[dc_bit], calc_amplitude(dc_amp, dc_bit, "DC"))
	insert_item = (dc_bit, dc_amp)
	output_list.append(insert_item)

	return output_list

def test():
	# 测试数据，来自P130上方
	test_list = [(2, 3), (1, 2, -2), (0, 1, -1), (0, 1, -1), (0, 1, -1), (2, 1, -1), (0, 0)]
	ll = get_entropy_encode(test_list)
	for i in ll:print i

if __name__ == '__main__':
	test()
