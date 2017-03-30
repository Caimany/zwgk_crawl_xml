# -*- coding:utf-8 -*-
import datetime,commands
from setting import BASE_DIR
from core_crawl import gen_date,_single_xml_crawl

def _xml_crawl(city_num,start_date='',end_date=''):
    p_end_date = (datetime.datetime.strptime(end_date, "%Y%m%d").date() +datetime.timedelta(hours=24)).strftime('%Y%m%d')
    for subdate in gen_date(start_date,p_end_date):
        _single_xml_crawl(date=subdate,city_num=city_num)

#凌晨4点运行 即将爬取的最新的xml
newest_date = (datetime.datetime.now()-datetime.timedelta(hours=0)).strftime('%Y%m%d')
older_date =  (datetime.datetime.now()-datetime.timedelta(hours=72)).strftime('%Y%m%d')

for citynum in range(0,22):
    # out = commands.getoutput('python %s/start.py %s %s'%(BASE_DIR,newest_date,citynum))
    # print "########################"
    # print out
    # print "########################"
    _xml_crawl(citynum,start_date=older_date,end_date=newest_date)