#!/usr/bin/python
# -*- coding: utf-8 -*-
from socket import inet_aton
import struct
import binascii
import os

class IPQ:
    binary = ""
    count_ip = []
    total_len = 0

    @staticmethod
    def load(file):
        try:
            path = os.path.abspath(file)
            with open(path, "rb") as f:
                IPQ.binary = f.read()
                IPQ.total_len = len(IPQ.binary)
                len_ip = struct.unpack('256I', IPQ.binary[:1024])
                IPQ.count_ip.append(0)
                index = 0
                for item in len_ip:
                    # print index, ':', item
                    IPQ.count_ip.append(IPQ.count_ip[index]+item)
                    index = index +1
        except Exception as ex:
            print "cannot open file %s" % file
            print ex.message
            exit(0)

    @staticmethod
    def find(ip):
        binary = IPQ.binary
        total_len = IPQ.total_len
        count_ip = IPQ.count_ip
        # print count_ip
        nip = inet_aton(ip)
        ipdot = ip.split('.')
        firstip = int(ipdot[0])
        if firstip < 0 or firstip > 255 or len(ipdot) != 4:
            return None
        count_ip_first = count_ip[firstip]
        count_ip_next = count_ip[firstip + 1]
        start_index = count_ip_first*8 + 1024
        end_index = count_ip_next*8 + 1024
        while start_index < end_index:
            if(binary[start_index:start_index+4] >= nip):
                return struct.unpack('I', binary[start_index+4:start_index+8])[0]
            start_index = start_index + 8

        return None

