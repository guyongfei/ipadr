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

script, ip = sys.argv

f = 'ipadr.dat'
IPQ.load(f)

db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password)

country_dict = {}
prov_dict = {}
city_dict = {}
intgeoid = 0

def read_db():
    sql = "select country_id, country_code from mad_rs_country"
    country_list = db.query(sql)
    for country in country_list:
        country_dict[country['country_code']] = country['country_id']

    sql = "select city_code, city_MVGeoID from mad_rs_china_city"
    city_list = db.query(sql)
    for city in city_list:
        city_dict[city['city_MVGeoID']] = city['city_code']

def get_location(ip):
    country_id = 0
    prov_code = '00'
    city_id = 0
    global intgeoid
    intgeoid = IPQ.find(ip)
    geoid = str(intgeoid)
    country_code = geoid[:4]
    if country_dict.has_key(country_code):
        country_id = country_dict[country_code]
    if country_code == '1156': #China
        prov_code = geoid[4:6]
    if city_dict.has_key(geoid):
        city_id = city_dict[geoid]
    return country_id,prov_code,city_id


read_db()
countryid, provcode, cityid =  get_location(ip)
print countryid, provcode, cityid

countryname='unknown'
provname='unknown'
cityname='unknown'
sql = "select country_name from mad_rs_country where country_id=%s" % countryid
res = db.query(sql)
if len(res) > 0:
    countryname = res[0]['country_name']
sql = "select prov_name from mad_rs_china_prov where prov_code='%s'" % provcode
res = db.query(sql)
if len(res) > 0:
    provname = res[0]['prov_name']
sql = "select city_name from mad_rs_china_city where city_code=%s" % cityid
res = db.query(sql)
if len(res) > 0:
    cityname = res[0]['city_name']
print countryname,provname,cityname

print intgeoid
workbook = xlrd.open_workbook('ip_code.xlsx')
booksheet = workbook.sheet_by_name('Sheet1')
for row in range(1,booksheet.nrows):
    value0 = booksheet.cell(row, 0).value.strip()
    value1 = booksheet.cell(row, 1).value.strip()
    value2 = int(booksheet.cell(row, 2).value)
    if value2 == intgeoid:
        print value0, value1