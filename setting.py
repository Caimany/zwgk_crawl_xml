# -*- coding:utf-8 -*-
import logging
import MySQLdb

city_url_dic={
    0: "http://zwgk.gd.gov.cn/xml/%year%/shengzhi%date%.xml",
    1: "http://zwgk.gz.gov.cn/xml/%year%/guangzhou%date%.xml",
    2: "http://zwgk.sz.gov.cn/xml/%year%/shenzhen%date%.xml",
    3: "http://zwgk.zhuhai.gov.cn/xml/%year%/zhuhai%date%.xml",
    4: "http://zwgk.st.gov.cn/xml/%year%/shantou%date%.xml",
    5: "http://zwgk.foshan.gov.cn/xml/%year%/foshan%date%.xml",

}

table_name = 'zwgkapp_data'
# db = MySQLdb.connect("localhost","root","southcn","ZWGK" )
mysql_conf = {
    'host':'localhost',
    'user':'root',
    'passwd':'southcn',
    'db':'ZWGK',
}
# db.set_character_set('utf8')



logging.basicConfig(
level=logging.DEBUG,
format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
datefmt='%a, %d %b %Y %H:%M:%S',
filename='/var/log/zwgk_crawl_xml/main.log',
filemode='a'
)


