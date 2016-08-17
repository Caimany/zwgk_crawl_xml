# -*- coding:utf-8 -*-
from core_crawl import xml_crawl,_single_xml_crawl,update_index
import sys,datetime

syslen = len(sys.argv)
starttime = datetime.datetime.now()
#long running

if syslen == 3:
    city_num = int(sys.argv[2])
    xml_date = sys.argv[1]
    print "正在爬取id为%s  %s xml的数据"%(city_num,xml_date)

    try:
        # lastest_dic = pickle.load(open('lastest_dic.pickle','rb'))
        # print "正在尝试继续爬之前未完成的xml数据...."
        # lastest_xml_date = lastest_dic[city_num]
        # xml_crawl(start_date=lastest_xml_date,end_date=xml_date,city_num=city_num)

        _single_xml_crawl(date=xml_date,city_num=city_num)
        f = open('lastest_dic.pickle', 'wb')
        #写lastest_dic.pickle to disk
        # pickle.dump(lastest_dic, f)
        f.close()


    except Exception as e:
        print "错误!:%s"%(str(e))
        print "..."
        print "尝试爬指定的xml数据"
        _single_xml_crawl(date=xml_date,city_num=city_num)
        pass


elif syslen == 4:
    xml_date1 = sys.argv[1]
    xml_date2 = sys.argv[2]
    city_num = int(sys.argv[3])
    print "正在爬取id为%s   %s ~ %s xml 的数据"%(city_num,xml_date1,xml_date2)

    xml_crawl(start_date=xml_date1,end_date=xml_date2,city_num=city_num)

else:
    print "请输入正确的命令格式:"
    print "%s 20150101 20151231 3  或者 %s 20150301 3"%(sys.argv[0],sys.argv[0])



endtime = datetime.datetime.now()
update_age = (endtime-starttime).seconds/3600+1
update_index(update_age=update_age)