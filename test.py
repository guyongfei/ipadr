#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import struct
from ipq import IPQ
import sys

script, ip = sys.argv

f = 'ipadr.dat'
IPQ.load(f)
ipaddr = IPQ.find(ip)
print ipaddr

# a = 'abcd'
# b = 'abcd'

# print '1.2.0.1'>'1.2.253.1'