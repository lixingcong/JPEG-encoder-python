#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < dc_ac_encode.py 2016-05-07 11:52:52 >
"""
DC AC系数的编码
""" 

import numpy as np

# 测试矩阵，课本P129 "量化矩阵"转化为1x64列表
test_list = [15, 0, -2, -1, -1, -1, 0, 0, -1]
for i in xrange(55):test_list.append(0)

def dc_encode():
	pass

def ac_encode():
	pass

def DC_AC_encode(input_list,last_DC_value):
	pass

def test():
	global test_list
	print test_list
	print len(test_list)

if __name__ == '__main__':
	test()
