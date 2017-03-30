# -*- coding:utf-8 -*-
import logging,redis
import MySQLdb

city_url_dic={
    0: "http://zwgk.gd.gov.cn/xml/%year%/shengzhi%date%.xml",
    1: "http://zwgk.gz.gov.cn/xml/%year%/guangzhou%date%.xml",
    2: "http://zwgk.sz.gov.cn/xml/%year%/shenzhen%date%.xml",
    3: "http://zwgk.zhuhai.gov.cn/xml/%year%/zhuhai%date%.xml",
    4: "http://zwgk.st.gov.cn/xml/%year%/shantou%date%.xml",
    5: "http://zwgk.foshan.gov.cn/xml/%year%/foshan%date%.xml",
    6: "http://zwgk.sg.gov.cn/xml/%year%/shaoguan%date%.xml",
    7: "http://zwgk.heyuan.gov.cn/xml/%year%/heyuan%date%.xml",
    8: "http://zwgk.meizhou.gov.cn/xml/%year%/meizhou%date%.xml",
    9: "http://zwgk.huizhou.gov.cn/xml/%year%/huizhou%date%.xml",
    10: "http://zwgk.shanwei.gov.cn/xml/%year%/shanwei%date%.xml",
    11: "http://zwgk.dg.gov.cn/xml/%year%/dongguan%date%.xml",
    12: "http://www.zs.gov.cn/xml/%year%/zhongshan%date%.xml",
    13: "http://zwgk.jiangmen.gov.cn/xml/%year%/jiangmen%date%.xml",
    14: "http://zwgk.yangjiang.gov.cn/xml/%year%/yangjiang%date%.xml",
    15: "http://zwgk.zhanjiang.gov.cn/xml/%year%/zhanjiang%date%.xml",
    16: "http://zwgk.maoming.gov.cn/xml/%year%/maoming%date%.xml",
    17: "http://zwgk.zhaoqing.gov.cn/xml/%year%/zhaoqing%date%.xml",
    18: "http://zwgk.gdqy.gov.cn/xml/%year%/qingyuan%date%.xml",
    19: "http://zwgk.chaozhou.gov.cn/xml/%year%/chaozhou%date%.xml",
    20: "http://zwgk.jieyang.gov.cn/xml/%year%/jieyang%date%.xml",
    21: "http://zwgk.yunfu.gov.cn/xml/%year%/yunfu%date%.xml",
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


import os,sys
BASE_DIR =  os.path.split(os.path.abspath(sys.argv[0]))[0]
rconn = redis.StrictRedis(host='localhost', port=6379, db=1, charset='utf-8', errors='strict', unix_socket_path=None)
