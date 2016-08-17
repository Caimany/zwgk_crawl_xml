# -*- coding:utf-8 -*-

# 约定时间格式为 20140101

from setting import logging,table_name,mysql_conf
import xml.etree.cElementTree as ET
import re,datetime,requests
from base import base_isourl
from setting import city_url_dic
import pickle,os,datetime
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial

# {'0':20160101,'1':20160302}

lastest_dic = {}

pool = ThreadPool(8)

haystack_path = "/home/ubuntu/work/zwgk_search"


# print gen_xml_url('20140103', 1, city_url_dic)
def _gen_xml_url(date, city_num, city_url_dic ):
    xml_url_template = city_url_dic[city_num]
    target_url_1 = re.sub('%date%', date, xml_url_template)
    target_url = re.sub('%year%',date[0:4],target_url_1)
    return target_url

# 日期生成器
def gen_date(start_date, end_date):
    try:
        d_start_date = datetime.datetime.strptime(start_date,'%Y%m%d')
        d_end_date = datetime.datetime.strptime(end_date,'%Y%m%d')
        if d_start_date == d_end_date:
            yield d_start_date.strftime('%Y%m%d')
        while d_start_date < d_end_date:
            #sub_date = '20160101'
            yield d_start_date.strftime('%Y%m%d')
            d_start_date=d_start_date+datetime.timedelta(days=1)
        pass
    except Exception as e:
         print 'EXCEPTION : in gen_date seg awrgs are %s %s , detail fellow  %s'%(start_date,end_date,str(e))

# # 连续处理url
# def process_xml(start_date,end_date,city_num,city_url_dic):
#     for _date in gen_date(start_date,end_date):
#         xml_url = _gen_xml_url(_date,city_num,city_url_dic)
#         try:
#             # extract xml
#             pass
#         except:
#             # xml push in redis
#             # retry_xml:list     city_num +:+ url
#             pass
import MySQLdb
class DB():
    connect = None
    def init_db(self):
        self.db  = MySQLdb.connect(mysql_conf['host'],mysql_conf['user'],mysql_conf['passwd'],mysql_conf['db'],charset="utf8" )

    def return_db(self):
        try:
            self.db.ping()
            return self.db
        except:
            self.init_db()
            return self.db

# 从redis处理
def pocess_xml_redis(list_name):
    # list_name = retry_xml:list
    # pop redis list retry_xml:list
    try:
        # extract xml
        pass
    except:
        # set in fails:url hash
        # city_num:xxxxxx,xxxxxx
        pass

# 传入xml字典,insert到数据库
def _sql_insert(data,table_name):
    try:

        # cur = db.cursor()
        cur_class = DB()
        db = cur_class.return_db()
        cur = db.cursor()
        placeholders = ', '.join(['%s'] * len(data))
        placeholders = placeholders.replace('%s','"%s"')
        columns = ', '.join(data.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)

        cur.execute(sql%tuple(data.values()))
        db.commit()
    except Exception as e :
        # print e.args[0],"!!", e.args[1]
        # duplicate autolink

        if e.args[0] == 1062:
            try:

                cur = db.cursor()
                autolink = data['autolink']
                del data['autolink']

                update_sql = 'UPDATE '+table_name+' SET {}'.format(', '.join('{}=%s'.format(k) for k in data) + ' WHERE autolink ="%s"'%(autolink) )
                # update_sql = update_sql.replace('%s','"%s"')
                # print update_sql
                cur.execute(update_sql,data.values())
                db.commit()

            except Exception as e:
                print "update fail! %s"%(str(e))
        else:
            print str(e)
    pass

def _clear_publisher(publisher_name,url):
    # 规则化发布机构名称
    return publisher_name

# xml外额外的数据加入到字典数据
def _extend_xml_dic(data):
    #setting 处理规则字典
    #visible
    data.update({'visible':'1'})

    #autolink
    # data['URL']
    autolink_obj = base_isourl()
    autolink = autolink_obj.isouri(data['URL']).replace('/','')
    data.update({'autolink':autolink})

    #clear_indexnum
    if data['INDEXNUM']:
        clear_indexnum = re.sub('/|-','',data['INDEXNUM'])
        data.update({'clear_indexnum':clear_indexnum})
    else:
        data.update({'clear_indexnum':''})

    #clear_publisher
    if data['PUBLISHER']:
        clear_publisher = _clear_publisher(data['PUBLISHER'],data['URL'])
        data.update({'clear_publisher':clear_publisher})
    else:
        data.update({'clear_publisher':''})

    # issued
    if data['city_num'] == 0:
        data.update({'issued':(data['URL'].split('/')[-1]).split('_')[0][1:9]})

    return data

# 传入xml地址,insert到数据库
def crawl_xml(xmlurl,city_num,xml_date):
    try:
        # exml = ET.fromstring(urllib2.urlopen(xmlurl).read())
        response = requests.get(xmlurl,timeout=1000)
        # if response == 200:
            #
        lastest_dic.update({city_num:xml_date})
        exml = ET.fromstring(response.text.encode('utf-8'))

        for subxml in exml:
            subxml_dic = {'city_num':city_num,'xml_date':xml_date}
            for i in subxml:
                # print i.tag,":",i.text
                # APPENDIXS 暂不处理
                if i.tag != 'APPENDIXS':
                    text = i.text
                    if text:
                        text = text.replace('"',"'")
                        # text = text.replace("'",'"')

                    subxml_dic.update({i.tag:text})
                else:
                    pass

            subxml_dic = _extend_xml_dic(subxml_dic)
            # 额外添加xml外的插入的数据
            _sql_insert(subxml_dic,table_name)
    except Exception as e:
        print str(e)
        pass

def _single_xml_crawl(date,city_num):
    print "crawl %s xml ... "%(date)
    try:
        xmlurl = _gen_xml_url(date, city_num, city_url_dic )

        crawl_xml(xmlurl=xmlurl,city_num=city_num,xml_date=date)
        f = open('lastest_dic.pickle', 'wb')
        # lastest_dic.update({city_num:date})
        pickle.dump(lastest_dic, f)
        f.close()

    except Exception as e:
        print "Fail ! crawl %s xml : %s"%(date,str(e))

def xml_crawl(start_date,end_date,city_num):

    partial_single_xml_crawl = partial(_single_xml_crawl,city_num=city_num)

    pool.map(partial_single_xml_crawl,gen_date(start_date,end_date))


    # for _date in gen_date(start_date,end_date):
    #     print "crawl %s xml ... "%(_date)
    #     # try:
    #     #     # print _date
    #     #     xmlurl = _gen_xml_url(_date, city_num, city_url_dic )
    #     #     # print xmlurl,city_num,_date
    #     #     crawl_xml(xmlurl,city_num,_date)
    #     # except Exception as e:
    #     #     print "Fail ! crawl %s xml :%s "%(_date,str(e))
    #     _single_xml_crawl(_date,city_num)

    # _single_xml_crawl(end_date,city_num)

    f = open('lastest_dic.pickle', 'wb')
    pickle.dump(lastest_dic, f)
    f.close()


    #读 pickle
    # game_state = pickle.load(open('gamestate.pickle', 'rb'))



def update_index(update_age):
    os.chdir(haystack_path)
    os.system('pwd')
    os.system('python ./manage.py update_index --age=%s'%(update_age))

# update_index()