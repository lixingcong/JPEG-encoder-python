#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < entropy_encode.py 2016-05-16 17:11:14 >
"""
熵编码
"""
AC_MODE = True
FORWARD = True

# 色度交流系数，从itu-t81.pdf中复制过来的。
huffman_AC_luminance_table_forward = (
	"1010",
	"00",
	"01",
	"100",
	"1011",
	"11010",
	"1111000",
	"11111000",
	"1111110110",
	"1111111110000010",
	"1111111110000011",
	"1100",
	"11011",
	"1111001",
	"111110110",
	"11111110110",
	"1111111110000100",
	"1111111110000101",
	"1111111110000110",
	"1111111110000111",
	"1111111110001000",
	"11100",
	"11111001",
	"1111110111",
	"111111110100",
	"1111111110001001",
	"1111111110001010",
	"1111111110001011",
	"1111111110001100",
	"1111111110001101",
	"1111111110001110",
	"111010",
	"111110111",
	"111111110101",
	"1111111110001111",
	"1111111110010000",
	"1111111110010001",
	"1111111110010010",
	"1111111110010011",
	"1111111110010100",
	"1111111110010101",
	"111011",
	"1111111000",
	"1111111110010110",
	"1111111110010111",
	"1111111110011000",
	"1111111110011001",
	"1111111110011010",
	"1111111110011011",
	"1111111110011100",
	"1111111110011101",
	"1111010",
	"11111110111",
	"1111111110011110",
	"1111111110011111",
	"1111111110100000",
	"1111111110100001",
	"1111111110100010",
	"1111111110100011",
	"1111111110100100",
	"1111111110100101",
	"1111011",
	"111111110110",
	"1111111110100110",
	"1111111110100111",
	"1111111110101000",
	"1111111110101001",
	"1111111110101010",
	"1111111110101011",
	"1111111110101100",
	"1111111110101101",
	"11111010",
	"111111110111",
	"1111111110101110",
	"1111111110101111",
	"1111111110110000",
	"1111111110110001",
	"1111111110110010",
	"1111111110110011",
	"1111111110110100",
	"1111111110110101",
	"111111000",
	"111111111000000",
	"1111111110110110",
	"1111111110110111",
	"1111111110111000",
	"1111111110111001",
	"1111111110111010",
	"1111111110111011",
	"1111111110111100",
	"1111111110111101",
	"111111001",
	"1111111110111110",
	"1111111110111111",
	"1111111111000000",
	"1111111111000001",
	"1111111111000010",
	"1111111111000011",
	"1111111111000100",
	"1111111111000101",
	"1111111111000110",
	"111111010",
	"1111111111000111",
	"1111111111001000",
	"1111111111001001",
	"1111111111001010",
	"1111111111001011",
	"1111111111001100",
	"1111111111001101",
	"1111111111001110",
	"1111111111001111",
	"1111111001",
	"1111111111010000",
	"1111111111010001",
	"1111111111010010",
	"1111111111010011",
	"1111111111010100",
	"1111111111010101",
	"1111111111010110",
	"1111111111010111",
	"1111111111011000",
	"1111111010",
	"1111111111011001",
	"1111111111011010",
	"1111111111011011",
	"1111111111011100",
	"1111111111011101",
	"1111111111011110",
	"1111111111011111",
	"1111111111100000",
	"1111111111100001",
	"11111111000",
	"1111111111100010",
	"1111111111100011",
	"1111111111100100",
	"1111111111100101",
	"1111111111100110",
	"1111111111100111",
	"1111111111101000",
	"1111111111101001",
	"1111111111101010",
	"1111111111101011",
	"1111111111101100",
	"1111111111101101",
	"1111111111101110",
	"1111111111101111",
	"1111111111110000",
	"1111111111110001",
	"1111111111110010",
	"1111111111110011",
	"1111111111110100",
	# 特殊位置，ZRL，对应'F/0'
	"11111111001",
	"1111111111110101",
	"1111111111110110",
	"1111111111110111",
	"1111111111111000",
	"1111111111111001",
	"1111111111111010",
	"1111111111111011",
	"1111111111111100",
	"1111111111111101",
	"1111111111111110"
)

huffman_AC_luminance_table_backward = {
	"1010" : 0,
	"00" : 1,
	"01" : 2,
	"100" : 3,
	"1011" : 4,
	"11010" : 5,
	"1111000" : 6,
	"11111000" : 7,
	"1111110110" : 8,
	"1111111110000010" : 9,
	"1111111110000011" : 10,
	"1100" : 11,
	"11011" : 12,
	"1111001" : 13,
	"111110110" : 14,
	"11111110110" : 15,
	"1111111110000100" : 16,
	"1111111110000101" : 17,
	"1111111110000110" : 18,
	"1111111110000111" : 19,
	"1111111110001000" : 20,
	"11100" : 21,
	"11111001" : 22,
	"1111110111" : 23,
	"111111110100" : 24,
	"1111111110001001" : 25,
	"1111111110001010" : 26,
	"1111111110001011" : 27,
	"1111111110001100" : 28,
	"1111111110001101" : 29,
	"1111111110001110" : 30,
	"111010" : 31,
	"111110111" : 32,
	"111111110101" : 33,
	"1111111110001111" : 34,
	"1111111110010000" : 35,
	"1111111110010001" : 36,
	"1111111110010010" : 37,
	"1111111110010011" : 38,
	"1111111110010100" : 39,
	"1111111110010101" : 40,
	"111011" : 41,
	"1111111000" : 42,
	"1111111110010110" : 43,
	"1111111110010111" : 44,
	"1111111110011000" : 45,
	"1111111110011001" : 46,
	"1111111110011010" : 47,
	"1111111110011011" : 48,
	"1111111110011100" : 49,
	"1111111110011101" : 50,
	"1111010" : 51,
	"11111110111" : 52,
	"1111111110011110" : 53,
	"1111111110011111" : 54,
	"1111111110100000" : 55,
	"1111111110100001" : 56,
	"1111111110100010" : 57,
	"1111111110100011" : 58,
	"1111111110100100" : 59,
	"1111111110100101" : 60,
	"1111011" : 61,
	"111111110110" : 62,
	"1111111110100110" : 63,
	"1111111110100111" : 64,
	"1111111110101000" : 65,
	"1111111110101001" : 66,
	"1111111110101010" : 67,
	"1111111110101011" : 68,
	"1111111110101100" : 69,
	"1111111110101101" : 70,
	"11111010" : 71,
	"111111110111" : 72,
	"1111111110101110" : 73,
	"1111111110101111" : 74,
	"1111111110110000" : 75,
	"1111111110110001" : 76,
	"1111111110110010" : 77,
	"1111111110110011" : 78,
	"1111111110110100" : 79,
	"1111111110110101" : 80,
	"111111000" : 81,
	"111111111000000" : 82,
	"1111111110110110" : 83,
	"1111111110110111" : 84,
	"1111111110111000" : 85,
	"1111111110111001" : 86,
	"1111111110111010" : 87,
	"1111111110111011" : 88,
	"1111111110111100" : 89,
	"1111111110111101" : 90,
	"111111001" : 91,
	"1111111110111110" : 92,
	"1111111110111111" : 93,
	"1111111111000000" : 94,
	"1111111111000001" : 95,
	"1111111111000010" : 96,
	"1111111111000011" : 97,
	"1111111111000100" : 98,
	"1111111111000101" : 99,
	"1111111111000110" : 100,
	"111111010" : 101,
	"1111111111000111" : 102,
	"1111111111001000" : 103,
	"1111111111001001" : 104,
	"1111111111001010" : 105,
	"1111111111001011" : 106,
	"1111111111001100" : 107,
	"1111111111001101" : 108,
	"1111111111001110" : 109,
	"1111111111001111" : 110,
	"1111111001" : 111,
	"1111111111010000" : 112,
	"1111111111010001" : 113,
	"1111111111010010" : 114,
	"1111111111010011" : 115,
	"1111111111010100" : 116,
	"1111111111010101" : 117,
	"1111111111010110" : 118,
	"1111111111010111" : 119,
	"1111111111011000" : 120,
	"1111111010" : 121,
	"1111111111011001" : 122,
	"1111111111011010" : 123,
	"1111111111011011" : 124,
	"1111111111011100" : 125,
	"1111111111011101" : 126,
	"1111111111011110" : 127,
	"1111111111011111" : 128,
	"1111111111100000" : 129,
	"1111111111100001" : 130,
	"11111111000" : 131,
	"1111111111100010" : 132,
	"1111111111100011" : 133,
	"1111111111100100" : 134,
	"1111111111100101" : 135,
	"1111111111100110" : 136,
	"1111111111100111" : 137,
	"1111111111101000" : 138,
	"1111111111101001" : 139,
	"1111111111101010" : 140,
	"1111111111101011" : 141,
	"1111111111101100" : 142,
	"1111111111101101" : 143,
	"1111111111101110" : 144,
	"1111111111101111" : 145,
	"1111111111110000" : 146,
	"1111111111110001" : 147,
	"1111111111110010" : 148,
	"1111111111110011" : 149,
	"1111111111110100" : 150,
	# ZRL (F/0) 注意另外编码规则与上面不一致
	"11111111001" : 151,
	"1111111111110101" : 152,
	"1111111111110110" : 153,
	"1111111111110111" : 154,
	"1111111111111000" : 155,
	"1111111111111001" : 156,
	"1111111111111010" : 157,
	"1111111111111011" : 158,
	"1111111111111100" : 159,
	"1111111111111101" : 160,
	"1111111111111110" : 161
}
huffman_DC_luminance_table_forward = (
	"00",
	"010",
	"011",
	"100",
	"101",
	"110",
	"1110",
	"11110",
	"111110",
	"1111110",
	"11111110",
	"111111110"
)

huffman_DC_luminance_table_backward = {
	"00":0,
	"010":1,
	"011":2,
	"100":3,
	"101":4,
	"110":5,
	"1110":6,
	"11110":7,
	"111110":8,
	"1111110":9,
	"11111110":10,
	"111111110":11
}

# 计算幅值，课本P133
def calc_amplitude(input_num, need_bit, mode = AC_MODE, direction = FORWARD):
	# 直流，且幅值0
	if mode is not AC_MODE and input_num == 0:
		return "0"
	elif mode is not AC_MODE and input_num == '0':
		return 0
	# 反向
	if direction is not FORWARD:
		num = int('0b' + input_num, 2)
		middle = 1 << (need_bit - 1)
		if num >= middle:
			return num
		else:
			sum = 0
			for i in xrange(need_bit):
				this_bit = num >> i & 0x1
				if this_bit == 0:
					sum += (1 << i)
			return -sum
	# 正向
	else:
		num = abs(input_num) & 0xffff
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

# 熵编码
# 输入一组包含多个Block的RLE码流，例如[[(2,3),(3,4)...],[(00,),(2,3)...]]输出[('100','00')...]
def get_entropy_encode(input_list, is_debug=False):
	output_list = []
	# 对每个block进行编码
	block_num = 1
	for each_block in input_list:
		if is_debug:
			print "get entropy encode: block #%d" % block_num
			block_num += 1
		# DC 编码，每个block的第一个元素是DC
		dc_bit = each_block[0][0]
		# 长度为1，即为dc00
		if len(each_block[0]) != 1:
			dc_amp = each_block[0][1]
			# 查DC表
			(dc_bit, dc_amp) = (huffman_DC_luminance_table_forward[dc_bit], calc_amplitude(dc_amp, dc_bit, "DC"))
			insert_item = (dc_bit, dc_amp)
		else:
			dc_bit = huffman_DC_luminance_table_forward[dc_bit]
			insert_item = (dc_bit,)
		if is_debug:print "DC:", insert_item
		output_list.append(insert_item)

		# AC 编码
		for ac_item in each_block[1:]:
			if len(ac_item) == 2:
				# RLZ编码
				if ac_item[0] == 15 and ac_item[1] == 0:
					insert_item = ('11111111001',)
					output_list.append(insert_item)
				# EOB编码
				elif ac_item[0] == 0 and ac_item[1] == 0:
					insert_item = ("1010",)
					output_list.append(insert_item)
			# 普通的AC系数编码
			else:
				ac_zero_counter = ac_item[0]
				ac_bit = ac_item[1]
				# 由(跨越/位长)得出查表位置=跨越*10+位长，除了RLZ以后的位置有偏移

				position_in_huffman_table = ac_zero_counter * 10 + ac_bit
				ac_amp = ac_item[2]
				ac_amp = calc_amplitude(ac_amp, ac_bit)
				
				# RLZ后的有偏移1
				if ac_zero_counter == 15:
					position_in_huffman_table += 1
				
				# 通过(跨越/位长)来查表
				coefficient = huffman_AC_luminance_table_forward[position_in_huffman_table]
				insert_item = (coefficient, ac_amp)
				output_list.append(insert_item)
			if is_debug:print "AC:", insert_item

	return output_list

# 二进制编码
# 输入一个列表[('100','00')...],该列表是所有block的组合，不分block，输出码流类似'ffab3324'，
def get_encoded_to_hex(input_list, is_debug=False):
	output_bin = ''
	buffer = ''
	# 逐位拼接
	for i in input_list:
		# 直流(00)、EOB(0/0)、或者ZRL(F/0)
		if len(i) == 1:
			buffer += i[0]
		# 普通码字长度为2个元素
		else:
			buffer += (i[0] + i[1])
		# 字节的倍数可以暂时转换一下成为hex
		if (len(buffer) % 8) == 0:
			# 注意保留前导的0，使用0b1作为前导再去掉
			this_hex = (hex(int('0b1' + buffer, 2)))[3:]
			output_bin += (this_hex[:-1] if this_hex[-1] == 'L' else this_hex)
			if is_debug:print buffer
			buffer = ''

	# 剩余位的处理方法
	l = len(buffer)
	if (l % 8) != 0 and l != 0:
		buffer += ('1' * (8 - (l % 8)))
		if is_debug:print buffer
		this_hex = (hex(int('0b1' + buffer, 2)))[3:]
		output_bin += (this_hex[:-1] if this_hex[-1] == "L" else this_hex)
	# print final_result
	# print bin(int('1' + final_result, 16))[3:]
	return output_bin

# 熵解码
# 输入一个[('100','00')...]，输出RLE例如[(2,3),(3,4)...]
def get_entropy_decode(input_list, is_debug=False):
	output_list = []
	each_block = []
	counter_less_than_64 = 0
	is_found_EOB = False
	is_coded_DC = False
	block_num = 1
	for i in input_list:
		if counter_less_than_64 == 64 or is_found_EOB:
			# 将当前block加入到列表中
			output_list.append(each_block)
			each_block = []
			# 复位状态
			counter_less_than_64 = 0
			is_found_EOB = False
			is_coded_DC = False
			print  "[NUM] End of block #%d" % block_num
			block_num += 1
		elif counter_less_than_64 > 64:
			print "MCU elements out of range 64!"
			exit(1)

		counter_less_than_64 += 1

		# 如果tuple元素只有一个'1010'，即EOB
		if len(i) == 1:
			if is_debug:print i
			
			if i[0] == '1010':
				if is_debug:print "EOB"
				EOB = (0, 0)
				each_block.append(EOB)
				is_found_EOB = True
				continue
			elif i[0] == '11111111001':
				if is_debug:print "    RLZ"
				RLZ = (15, 0)
				each_block.append(RLZ)
				# 跨越
				counter_less_than_64 += 15
				continue
			elif not is_coded_DC and i[0] == '00':
				if is_debug:print "---\nDC00"
				# DC解码
				insert_item = (0,)
				each_block.append(insert_item)
				is_coded_DC = True
				continue

		if not is_coded_DC:
			if is_debug:print "---\nDC: ", i
			# DC解码
			dc_bit = i[0]
			dc_amp = i[1]
			# DC位长
			dc_bit = huffman_DC_luminance_table_backward[dc_bit]
			dc_amp = calc_amplitude(dc_amp, dc_bit, mode = False, direction = False)
			insert_item = (dc_bit, dc_amp)
			each_block.append(insert_item)
			is_coded_DC = True
			continue


		# AC解码
		# 查表看到对应的十进制数
		if is_debug:print "AC:", i
		coefficient = i[0]
		ac_zero_counter_and_bit = huffman_AC_luminance_table_backward[coefficient]

		# RLZ 后面的，减去RLZ一个
		if ac_zero_counter_and_bit > 150:
			ac_zero_counter_and_bit -= 1
			
		# 由(跨越/位长)得出查表位置=跨越*10+位长
		ac_zero_counter = (ac_zero_counter_and_bit - 1) / 10
		ac_bit = ac_zero_counter_and_bit % 10
		
		# 余数0表示位长A
		if ac_bit == 0:
			ac_bit = 10
		# 跨越像素
		counter_less_than_64 += ac_zero_counter

		# 计算幅值
		ac_amp = i[1]
		ac_amp = calc_amplitude(ac_amp, ac_bit, mode = AC_MODE, direction = False)

		insert_item = (ac_zero_counter, ac_bit, ac_amp)
		each_block.append(insert_item)

	# 最后一个列表要加进去
	print  "[NUM] End of block #%d" % block_num
	output_list.append(each_block)
	return output_list

# 从二进制流中读取出范式编码
# 输入一个字符串"ff329900"，输出列表[('1001',''0030')...]
def get_decoded_from_hex(input_string, is_debug = False):
	# 替换FF00为FF的步骤不应该在本函数内实现，应交给IO读写实现
	# input_string_new = input_string.replace('FF00', 'FF')
	print input_string[:16]
	buffer = bin(int('1' + input_string, 16))[3:]
	output_list = []
	len_buffer = len(buffer)
	current_pos = 0
	block_num = 1

	# 遍历所有位
	while(current_pos < len_buffer):
		print "-----------\n[HEX] decode block #%d" % block_num
		block_num += 1
		# DC
		bit_index = 1
		dc_bit, dc_amp = '', 0
		bits_to_read = 0
		# 读取位长，最大扫描16位
		if is_debug:
			# print "DC blocks to find:",
			# print "\n " + buffer[:32]
			pass
		while bit_index < 16:
			these_bits_value = buffer[:bit_index]
			# 使用forward表查
			if these_bits_value in huffman_DC_luminance_table_backward:
				dc_bit = these_bits_value
				# 查backward表得到位长
				bits_to_read = huffman_DC_luminance_table_backward[dc_bit]
				# 截断
				buffer = buffer[bit_index:]
				# 更新current指针
				current_pos += bit_index
				break
			bit_index += 1

		if dc_bit == '':
			print "DC value is not in huffman table!!!!\nMaybe DHT was not normalized or this jpg has been optimized."
			exit(1)

		# 直流分量位长为非0才进行读取
		if bits_to_read != 0:
			# DC解码 读取振幅，向前读取位长
			dc_amp = buffer[:bits_to_read]
			buffer = buffer[bits_to_read:]
			insert_item = (dc_bit, dc_amp)
			# 更新current指针
			current_pos += bits_to_read
		else:
			insert_item = (dc_bit,)

		# 直流写入到output
		output_list.append(insert_item)
		if is_debug:
			if bits_to_read != 0:
				print dc_bit, dc_amp
			else:
				print dc_bit

		# AC
		# 读取（跨越、位长、幅值）
		zero_counter = 0
		ac_bit = 0
		ac_amp = 0
		# 循环中止的变量
		zig_zag_counter = 1
		is_found_EOB = False
		is_this_block_ended = False
		while True:
			# 复位bit指针
			bit_index = 1
			bits_to_read = 0
			# 临时调试用，
			temp = 0
			if is_debug:
				# print "AC blocks to find: (32b))",
				# print "\n " + buffer[:32]
				pass
			# 逐位读取，最大读取16bit
			while bit_index <= 16:
				these_bits_value = buffer[:bit_index]
				if these_bits_value in huffman_AC_luminance_table_backward:
					# 如果是EOB或者ZRL（F/0）即16个零
					if these_bits_value == '1010':
						is_this_block_ended = True
						# 截断buffer
						buffer = buffer[bit_index:]
						# 插入EOB进结果
						ac_bit = these_bits_value
						# 结束本次16位搜寻之旅
						break
					elif these_bits_value == '11111111001':
						# 截断buffer
						buffer = buffer[bit_index:]
						ac_bit = these_bits_value
						# 跨越15个零，zig+=15
						zig_zag_counter += 15
						# 结束本次16位搜寻之旅
						break
					# 如果是其它跨越/位长
					ac_bit = these_bits_value
					# 截断
					buffer = buffer[bit_index:]

					# 求位长和跨越，很多坑，最坑就是RLZ
					temp = huffman_AC_luminance_table_backward[ac_bit]
					# 排在RLZ后面的数字
					if temp > 150:
						temp -= 1
					# 位长
					bits_to_read = temp % 10
					# 位长余数0，即为10对应A
					if bits_to_read == 0:
						bits_to_read = 10
					# 跨越了多少个像素
					zig_zag_counter += (temp - 1) / 10
					
					# 读取幅值
					ac_amp = buffer[:bits_to_read]
					# 截断
					buffer = buffer[bits_to_read:]
					break

				bit_index += 1

			if is_debug:print "pixel #" + str(zig_zag_counter),
			# 更新current指针
			current_pos += (bit_index + bits_to_read)
			# 插入除了长度为1的码字
			if bits_to_read != 0:
				insert_item = (ac_bit, ac_amp)
			else:
				insert_item = (ac_bit,)
			# 输出调试结果
			if is_debug:
				if bits_to_read != 0:
					print ac_bit, ac_amp
				else:
					print ac_bit
			output_list.append(insert_item)
			# 异常解码，数组溢出
			if zig_zag_counter == 63 or is_this_block_ended:
				break
			elif zig_zag_counter >= 64:
				print "ERROR when coding AC, out of range 64"
				print "buffer:", buffer[:16]
				exit(1)				
			# 下一个zig
			zig_zag_counter += 1

		# 遍历完所有MCU停止的条件之一是padding位不超过8
		if len_buffer - current_pos < 8:
			break
	if is_debug:print "-------\ndecode from hex finished, remain bits:", buffer, '\n-------'
	return output_list

def test1():
	# 测试数据，来自P130上方
	test_list = [(2, 3), (1, 2, -2), (0, 1, -1), (0, 1, -1), (0, 1, -1), (2, 1, -1), (0, 0)]
	print "original:"
	print test_list
	print "-" * 10
	# 编码
	encoded = get_entropy_encode(test_list)
	print "encoded:"
	print encoded
	# 解码
	print "-" * 10
	print "decoded:"
	print get_entropy_decode(encoded)

def test2():
	# 测试对十六进制的读写，囊括所有的转码
	# test_hex = "FD53F885FB4EDDFC28F8A1A47ED7DF1A3F69FF001A4DFB29FC03FD983F67A8BE21785BC617FADF88BC3B67E35B192CBC11F153C0BE30F859ACD9F8987C40F897E32F1AF897C32F7DF173C19E0AF107C43D06F7C69E15BCD47C63A07C33D39E5F15FF00"
	# 包含两个block的数据
	test_hex = "FE8D7E1A7C00B1F08F87F4CF0D6950DE49A6E9AD78D6DF6E9DAEAE337D7F77A8CFBE6645DC05CDE4C22508AB1C4238D46D415F23FF00C161FF00E0A59F02BF663FD907C73E18F827F147C3FE2FF8F7F16DAFFE19F82D7C1C1FC45A6F87B4C17B0E9DF13BC4D75E23B30BA0C573A36832DF785F458F4CD5AF75EB7F1BEBBA36A10E95268DE1FF00156A5A17"
	# 把0xff00替换为ff
	test_hex = test_hex.replace("FF00", "FF")
	# test_hex = ''
	# with open('/tmp/2.bin', 'rb') as f:
		# test_hex = f.read().encode('hex')

	print "-" * 10
	print "original:"
	print test_hex

	print "-" * 10
	decoded_hex = get_decoded_from_hex(test_hex, is_debug = False)
	print "decoded to bin:"
	print decoded_hex

	print "-" * 10
	print "decode to RLE:(maybe has multi blocks!)"
	decoded_hex_RLE = get_entropy_decode(decoded_hex)
	for i in decoded_hex_RLE:
		print i


	print "-" * 10
	print "encoded to bin:"
	encoded_hex = get_entropy_encode(decoded_hex_RLE)
	print encoded_hex


	print "-" * 10
	print "encode to hex stream:"
	final = get_encoded_to_hex(encoded_hex)
	print final

	print "len of original:", len(test_hex), "\nlen of final:", len(final)



if __name__ == '__main__':
	# test1()
	test2()
