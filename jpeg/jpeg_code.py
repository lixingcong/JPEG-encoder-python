#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < jpeg_code.py 2016-05-12 13:33:00 >
"""
JPEG编码
"""

import block_split
import dct
import quantize
import zig_zag_scan
import dc_ac_encode
import entropy_encode
import numpy as np
import struct

from quantize import FORWARD
from quantize import LUMINANCE


def jpeg_encode(input_matrix):
	output_stream = []
	# 填充block长宽为8的整数
	temp_matrix = block_split.padding_dummy_edge(input_matrix)
	# 分割MCU
	blocks_spilted = block_split.split_to_blocks(temp_matrix)[0]
	del temp_matrix
	last_DC_value = 0
	block_num = 1
	# 对每一个block处理
	for block in blocks_spilted:
		print "----------------\nBLOCK #%d encoding:" % block_num
		block_num += 1
		# 计算DCT变换
		DCT_table = dct.forward_dct(block - 128)
		# 量化
		table_quantized = quantize.get_quantisation(DCT_table)
		# zig-zag顺序读取数据
		result_zig_zag = zig_zag_scan.get_seq_1x64(table_quantized)
		# 直流、交流编码
		encoded_1 = dc_ac_encode.DC_AC_encode(result_zig_zag, last_DC_value)
		print encoded_1
		# 熵编码（哈夫曼）
		encoded_2 = entropy_encode.get_entropy_encode(encoded_1)
		# print encoded_2
		output_stream.append(encoded_2)
		# 记下当前块的DC值供下一个编号
		last_DC_value = table_quantized[0, 0]

	return output_stream
	# TODO
	# 二进制编码

def jpeg_decode(input_list, width, height):
	block_num = 1
	last_DC_value = 0
	restored_MCU_blocks = []
	for MCU in input_list:
		print "----------------\nBLOCK #%d decoding:" % block_num
		block_num += 1
		# 熵解码
		decode_1 = entropy_encode.get_entropy_decode(MCU)
		# DC AC解码
		decode_2 = dc_ac_encode.DC_AC_decode(decode_1, last_DC_value)
		print decode_2
		# zig-zag还原成8x8矩阵
		result_zig_zag = zig_zag_scan.restore_matrix_from_1x64(decode_2)
		print result_zig_zag
		# 反量化
		table_unquantized = quantize.get_quantisation(result_zig_zag, LUMINANCE, False)
		# 逆DCT变换
		IDCT_table = dct.inverse_dct(table_unquantized)
		restored_MCU_blocks.append(IDCT_table + 128)
		# 更新DC值
		last_DC_value = result_zig_zag[0, 0]
	# 合并前计算padded尺寸
	width_padded, height_padded = block_split.calc_new_size(width, height)
	# 计算MCU的行列数
	columns, rows = width_padded / 8, height_padded / 8
	# 合并
	merged_matrix = block_split.merge_blocks(restored_MCU_blocks, rows, columns)
	# 移除多余的边缘像素
	final_matrix = block_split.remove_dummy_edge(merged_matrix, width, height)
	return final_matrix

def test():
	# 测试矩阵，在课本P129
	test_table = np.array([
		[139, 144, 149, 153, 155, 155, 155, 155],
		[144, 151, 153, 156, 159, 156, 156, 156],
		[150, 155, 160, 163, 158, 156, 156, 156],
		[159, 161, 162, 160, 160, 159, 159, 159],
		[159, 160, 161, 162, 162, 155, 155, 155],
		[161, 161, 161, 161, 160, 157, 157, 157],
		[162, 162, 161, 163, 162, 157, 157, 157],
		[162, 162, 161, 163, 162, 157, 157, 157],
		[162, 162, 161, 161, 163, 158, 158, 158]
	])
	print "original:"
	print test_table
	# 编码
	encoded = jpeg_encode(test_table)
	print  '#' * 10 + "\nencoded:"
	print encoded

	# 解码
	decoded = jpeg_decode(encoded, 8, 9)
	print '#' * 10 + "\ndecoded:"
	print decoded


if __name__ == "__main__":
	test()
