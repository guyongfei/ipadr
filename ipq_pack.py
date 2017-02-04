#!/usr/bin/python
# -*- coding: utf-8 -*-
from socket import inet_aton
import struct
import binascii
import csv

fdat = open('ipadr.dat', 'wb')
excelfile = 'IP(20160905).csv'

len_ip = []
array_ip = []

# len_ip = [1,3,4]
# array_0 = [{'0.255.255.255':1000000000}]
# array_1 = [{'1.0.0.255':1000000000},{'1.0.3.255':1156350100},{'1.255.255.255':1410000000}]
# array_2 = [{'2.16.0.255':1250000000},{'2.103.255.255':1826000000},{'2.199.255.255':1380000000},{'2.255.255.255':1752000000}]

def read_excel(fexcel):
    prev_ip_1 = '0' #记录上一次ip的第一个字段，0~255。
    ip_1_arr = [] #记录prev_ip_1开头的ip地址段和编码的映射关系，截止IP作为key，
                  #如，对于1.x.x.x类型的ip而言，格式：[{"1.0.255.255":11560000},{"1.255.255.255":11430000}]
    prev_ip = '' #记录上次处理的IP
    for line in open(fexcel):
        if len(line) > 15:
            print line
            items = line.split(',')
            ip = items[1]
            loc = int(items[2])
            ip_1 = ip.split('.')[0]

            #ip地址的第一个字段，如果跟上次的不一样，逐渐递增prev_ip_1
            if ip_1 != prev_ip_1:
                while ip_1 != prev_ip_1:
                    cur_ip = '%s.255.255.255' % prev_ip_1
                    if cur_ip != prev_ip:
                        ip_loc_item = {cur_ip:loc}
                        ip_1_arr.append(ip_loc_item)
                        prev_ip = cur_ip

                    #将上一次ip段录入到全局变量
                    len_ip.append(len(ip_1_arr))
                    array_ip.append(ip_1_arr)

                    ip_1_arr = []

                    int_prev_ip_1 = int(prev_ip_1)
                    prev_ip_1 = str(int_prev_ip_1+1)

                    if(prev_ip_1 == ip_1):
                        cur_ip = ip
                        ip_loc_item = {cur_ip:loc}
                        ip_1_arr.append(ip_loc_item)
                        prev_ip = cur_ip
            else:
                cur_ip = ip
                ip_loc_item = {cur_ip:loc}
                ip_1_arr.append(ip_loc_item)
                prev_ip = cur_ip
    len_ip.append(len(ip_1_arr))
    array_ip.append(ip_1_arr)

def pack_len_ip():
    print len_ip
    packformat = '%sI' % len(len_ip)
    s = struct.Struct(packformat)
    packed_data = s.pack(*len_ip)
    # unpacked_data = s.unpack(packed_data)
    fdat.write(packed_data)
    print 'Packed value:', binascii.hexlify(packed_data)
    # print 'Unpacked value:', type(unpacked_data), unpacked_data

def pack_ip_array(array_x):
    for ip_item in array_x:
        for k,v in ip_item.items():
            tmp = inet_aton(k)
            end_ip_addr = struct.pack('4c', *tmp)
            end_ip_loc =  struct.pack('I', v)
            fdat.write(end_ip_addr)
            fdat.write(end_ip_loc)
            # print binascii.hexlify(end_ip_addr), binascii.hexlify(end_ip_loc)

read_excel(excelfile)
pack_len_ip()
print array_ip
for array_item in array_ip:
    pack_ip_array(array_item)

fdat.close()