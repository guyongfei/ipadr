#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import struct
from ipq import IPQ
import sys
import torndb
import json
from tornado.options import define, options
import xlrd

define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="mad", help="blog database name")
define("mysql_user", default="mobilead", help="blog database user")
define("mysql_password", default="Mobad2016!", help="blog database password")

# script, ip = sys.argv

# f = 'ipadr.dat'
# IPQ.load(f)
# ipaddr = IPQ.find(ip)
# print ipaddr
db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

city_dict = {}

def read_xlsx():
    workbook = xlrd.open_workbook('ip_code.xlsx')
    booksheet = workbook.sheet_by_name('Sheet1')
    for row in range(1,booksheet.nrows):
        value0 = booksheet.cell(row, 0).value.strip()
        value1 = booksheet.cell(row, 1).value.strip()
        # print value0, value1, value1[len(value1)-1], value1[len(value1)-1]==u'市'
        if value1[len(value1)-1]==u'市':
            value1 = value1[:-1]

        city_dict[value1] = int(booksheet.cell(row, 2).value)

def read_db_city():
    sql = 'select city_code, city_name from mad_rs_china_city'
    citylist = db.query(sql)
    print len(citylist)
    for city in citylist:
        city_name = city['city_name'].strip()
        print city_name
        sql_update = 'update mad_rs_china_city set city_MVGeoID="%s" where city_code = %s' % (str(city_dict[city_name]), city['city_code'])

        print sql_update
        city_dict.pop(city_name)
        db.execute(sql_update)

read_xlsx()
read_db_city()
print len(city_dict)
i = 47
for keyitem in  city_dict.keys():
    sql_insert = 'insert into mad_rs_china_city(id, city_name, city_code, city_name_en, city_MVGeoID) \
        values(%s, "%s", %s, "", "%s")' % (i,keyitem,i,str(city_dict[keyitem]))
    i = i+1
    db.execute(sql_insert)
    print sql_insert

