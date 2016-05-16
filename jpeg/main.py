#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < main.py 2016-05-16 17:41:41 >
"""
主演示程序
""" 

import io_jpg
import io_bmp
import numpy as np
import argparse


def demo(src):
	if src[-3:] == 'jpg':
		my_pic = io_jpg.JPG(src)
		dst = raw_input("输入保存bmp路经:")
		my_pic.read_data()
		matrix = my_pic.get_data()[0]
		my_pic1 = io_bmp.BMP(dst, matrix)
		try:
			my_pic1.write_data()
			print "写入%s成功！" % dst
		except:
			print "写入错误！"
			exit(1)
	elif src[-3:] == 'bmp':
		my_pic = io_bmp.BMP(src)
		dst = raw_input("输入保存jpg路经:")
		my_pic.read_data()
		matrix = my_pic.get_data()[0]
		my_pic1 = io_jpg.JPG(dst, matrix)
		try:
			my_pic1.write_data()
			print "写入%s成功！" % dst
		except:
			print "写入错误！"
			exit(1)
	else:
		print "不是jpg或者bmp！"
		exit(1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "简易灰度BMP和JPG互转程序 By 黎醒聪 @2015.5.16")
	parser.add_argument('--src', action = "store", dest = "src", help='源文件，可以是bmp或jpg',required = True)
	given_args = parser.parse_args()
	src = given_args.src
	demo(src)



