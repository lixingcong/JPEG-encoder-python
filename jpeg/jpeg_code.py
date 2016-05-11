#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < jpeg_code.py 2016-05-11 19:05:01 >
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


# z字形扫描的固定字典
zigzig_dict_forward = zig_zag_scan.generate_dict('forward')
zigzig_dict_backward = zig_zag_scan.generate_dict('backward')

def jpeg_encode(input_matrix):
	temp_matrix = block_split.padding_dummy_edge(input_matrix)
	blocks_spilted = block_split.split_to_blocks(temp_matrix)[0]
	del temp_matrix
	last_DC_value = 0

	for block in blocks_spilted:
		DCT_table = dct.forward_dct(block - 128)
		table_quantized = quantize.get_quantisation(DCT_table, 'chrominance', 'forward')
		result_zig_zag = zig_zag_scan.get_seq_1x64(table_quantized, zigzig_dict_forward)
		encoded_1 = dc_ac_encode.DC_AC_encode(result_zig_zag, last_DC_value)
		encoded_2 = entropy_encode.get_entropy_encode(encoded_1)
		last_DC_value = result_zig_zag[0]

	print encoded_1
	print encoded_2

def jpeg_decode(input_list):
	pass

def test():
	test_table = np.array([
		[139, 144, 149, 153, 155, 155, 155, 155],
		[144, 151, 153, 156, 159, 156, 156, 156],
		[150, 155, 160, 163, 158, 156, 156, 156],
		[159, 161, 162, 160, 160, 159, 159, 159],
		[159, 160, 161, 162, 162, 155, 155, 155],
		[161, 161, 161, 161, 160, 157, 157, 157],
		[162, 162, 161, 163, 162, 157, 157, 157],
		[162, 162, 161, 161, 163, 158, 158, 158]
	])
	jpeg_encode(test_table)


if __name__ == "__main__":
	test()
