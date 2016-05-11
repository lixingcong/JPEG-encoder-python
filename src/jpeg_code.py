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
import entropy_encode
import dc_ac_encode
import numpy as np

def jpeg_encode(input_matrix):
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
	pass

if __name__ == "__main__":
	test()
