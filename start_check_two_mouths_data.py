# -*- coding:utf-8 -*-

import datetime,multiprocessing,time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ProcessPool

from core_crawl import gen_date,_single_xml_crawl
k = 0


def c_xml_crawl(city_num):
    today = datetime.datetime.now()
    today2mouth = datetime.datetime.now() -  datetime.timedelta(days=60)
    end_date=today.strftime("%Y%m%d")
    start_date= today2mouth.strftime("%Y%m%d")


    p_end_date = (datetime.datetime.strptime(end_date, "%Y%m%d").date() +datetime.timedelta(hours=24)).strftime('%Y%m%d')
    for subdate in gen_date(start_date,p_end_date):
        _single_xml_crawl(date=subdate,city_num=city_num)


def thread_pool_crawl(a,b):
    # partial_xml_crawl = pyth(xml_crawl,start_date=20000101,end_date=20160901)
    # p_end_date = (datetime.datetime.strptime(end_date, "%Y%m%d").date() +datetime.timedelta(hours=24)).strftime('%Y%m%d')
    pool = ThreadPool(8)

    pool.map(c_xml_crawl,range(a,b))

def Process_pool_crawl(a,b):
    pool = ProcessPool(8)
    pool.map(c_xml_crawl,range(a,b))
    pool.close()
    pool.join()


# for i in range(3,22,4):
#     thread_pool_crawl(i,i+4)
# def C_Process_pool_crawl():
#     pool = ProcessPool(6)
#     pool.map(c_xml_crawl,[1,2,4,7,8,9,13,14,15,21])
#     pool.close()
#     pool.join()


if __name__ == '__main__':
    for i in range(0,22):

        c_xml_crawl(i)