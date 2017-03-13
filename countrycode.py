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

country_dict = {}

def read_xlsx():
    workbook = xlrd.open_workbook('ip_code.xlsx')
    booksheet = workbook.sheet_by_name('Sheet1')
    for row in range(1,booksheet.nrows):
        value0 = booksheet.cell(row, 0).value.strip()
        value1 = booksheet.cell(row, 1).value.strip()
        # print value0, value1, value0==u'全球'
        if value0 == u'全球':
            countrycode = int(booksheet.cell(row, 2).value)
            country_dict[value1] = countrycode
    print len(country_dict)

def read_db_country():
    sql = 'select country_id, country_name from mad_rs_country'
    countrylist = db.query(sql)
    for country in countrylist:
        country_name = country['country_name'].strip()
        if country_name == u'中国台湾':
            country_name = u'台湾'
        if country_name == u'泽西岛(英吉利海峡的岛屿)':
            country_name = u'泽西岛'
        if country_name == u'波斯尼亚和黑塞哥维那':
            country_name = u'波黑'
        if country_name == u'科索沃共和国':
            continue
        if country_name == u'苏图语':
            continue
        if country_name == u'博内尔岛':
            continue   
        if country_name == u'科威特-重复':
            continue 
        sql_update = 'update mad_rs_country set country_code="%s" where country_id = %s' % (str(country_dict[country_name]/1000000), country['country_id'])

        print sql_update
        country_dict.pop(country_name)
        # db.execute(sql_update)

read_xlsx()
read_db_country()
i = 248
for keyitem in  country_dict.keys():
    sql_insert = 'insert into mad_rs_country(country_id, country_name, country_name_en, iso_code, country_code) \
    values(%s, "%s", "", "", "%s")' % (i,keyitem,str(country_dict[keyitem]/1000000))
    i = i+1
    db.execute(sql_insert)
    print sql_insert

