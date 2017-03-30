# -*- coding:utf-8 -*-

# 约定时间格式为 20140101

from setting import logging,table_name,mysql_conf
import xml.etree.cElementTree as ET
import re,datetime,requests
from base import base_isourl
from setting import city_url_dic,rconn
import os,datetime,time
# from multiprocessing.dummy import Pool as ThreadPool
# from functools import partial
# from xml.etree.cElementTree import ParseError
import MySQLdb,random
from redis_queue import RedisQueue

print "采集xml前,会查询redis集合中的是否的采集过,如需手动重新采集,请删除redis数据中的历史采集记录..."
# time.sleep(10)


# pool = ThreadPool(8)

haystack_path = "/home/ubuntu/work/zwgk_search"


# print gen_xml_url('20140103', 1, city_url_dic)
def _gen_xml_url(date, city_num, city_url_dic ):
    xml_url_template = city_url_dic[city_num]
    target_url_1 = re.sub('%date%', date, xml_url_template)
    target_url = re.sub('%year%',date[0:4],target_url_1)
    return target_url

# 日期生成器 生成%Y%m%d 格式的字符串
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

# db = DB().return_db()
# k = 0
def _InsertSQLbyDic(data, table_name):
    db = DB().return_db()
    try:
        cur = db.cursor()
        placeholders = ", ".join(['%s'] * len(data))
        placeholders = placeholders.replace('%s', "%s")
        columns = ', '.join(data.keys())

        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table_name, columns, placeholders)
        cur.execute(sql, tuple(data.values()))
    except Exception as e:
        raise e
    finally:
        db.commit()


# 删除数据 传入autolink
def _DeleteSQLbyAutolink(autolink, table_name):
    db = DB().return_db()
    cur = db.cursor()
    sql = '''DELETE FROM %s where autolink = "%s";''' % (table_name, autolink)
    cur.execute(sql)
    db.commit()
    # db.close()
    print "删除成功"


# 查询该信息是否已经插入了sql中,如果是 返回xmldate
def _QueryIsSQLbyautolink(autolink,city_num, table_name):
    db = DB().return_db()
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute('''SELECT xml_date,autolink,id FROM %s  where autolink="%s" and city_num = %s LIMIT 1;''' % (table_name, autolink,city_num))
    return cur.fetchone()

# 更新autolink
def _ReplaceSQLbyAutolink(data, table_name):

    db =  DB().return_db()
    cautolink = data['autolink']
    ccitynum = data['city_num']
    # data.pop('autolink')
    placeholders = ', '.join(['%s'] * len(data))
    # placeholders = placeholders.replace('%s', "%s")
    columns = ', '.join(data.keys())
    sql = '''REPLACE INTO  %s(%s) VALUES(%s);''' % (table_name, columns, placeholders)
    # print tuple(data.values())
    # time.sleep(100)
    db.commit()
    cur = db.cursor()
    cur.execute(sql, tuple(data.values()))
    db.commit()

    # db.close()


# 更新
def _UpdateTable(data,table_name):
    db =  DB().return_db()
    sql = '''UPDATE '''+table_name+''' SET {}'''.format(', '.join('{}=%s'.format(k) for k in data))
    print sql
    cur = db.cursor()
    cur.execute(sql, tuple(data.values()))
    db.commit()

#判断该信息是否是最新的 strdate='20120303' comdatetime 为datetimetype


def _sql_insert(data, table_name):
    try:
        _InsertSQLbyDic(data, table_name)
    except Exception as e:


        if e.args[0] == 1062:

            print "%s autolink: %s 已存在"%(data['xml_date'],data['autolink']),
            # 判断信息是否已经更新
            if  _QueryIsSQLbyautolink(autolink=data["autolink"],city_num=data["city_num"],table_name=table_name):
                if datetime.datetime.strptime(str(data['xml_date']), '%Y%m%d') > \
                        _QueryIsSQLbyautolink(autolink=data["autolink"], city_num=data['city_num'],table_name=table_name)['xml_date']:
                    print "需要更新"

                    # _UpdateTable(data,table_name)
                    q=RedisQueue('removed pk')
                    q.put(_QueryIsSQLbyautolink(autolink=data["autolink"], city_num=data['city_num'],table_name=table_name)['id'])

                    _ReplaceSQLbyAutolink(data, table_name)

                else:
                    pass
            else:
                print "可能错误 %s:%s "%(data['city_num'],data['xml_date'])

            print ''

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

    # issued,provincial_office
    if data['city_num'] == 0:
        data.update({'issued':(data['URL'].split('/')[-1]).split('_')[0][1:9]})
        if re.search('http://zwgk.gd.gov.cn/006939748/',data['URL']):
            # 办公厅
            data.update({'provincial_office':50})
        else:
            # 省直
            data.update({'provincial_office':30})


    return data

# 传入xml地址,insert到数据库
def crawl_xml(xmlurl,city_num,xml_date):
    try:
        response = requests.get(xmlurl,timeout=1000)
        # exml = ET.fromstring(response.text.encode('utf-8'))
        exml = ET.fromstring(response.content)

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

            # for i in  subxml_dic.values():
            #     print i
            subxml_dic = _extend_xml_dic(subxml_dic)
            # 额外添加xml外的插入的数据
            _sql_insert(subxml_dic,table_name)

    except Exception as e:
        print str(e)
        pass
    finally:
        redis_set_name = 'city_num_' + str(city_num)

        #记录已采集的xml 无论成功还是失败
        # rconn.zincrby(redis_set_name, str(xml_date), str(xml_date))

def _single_xml_crawl(date,city_num):
    str_date = date
    redis_set_name ='city_num_'+str(city_num)
    # if not rconn.zscore(name=redis_set_name,value = str_date):
    if 1:
        print str(os.getpid()),"-- %s  crawl %s:%s xml ... "%(time.strftime('%m-%d %H:%M',time.localtime()),city_num,date)
        xmlurl = _gen_xml_url(date, city_num, city_url_dic )
        crawl_xml(xmlurl=xmlurl,city_num=city_num,xml_date=date)


def xml_crawl(start_date,end_date,city_num):
    p_end_date = (datetime.datetime.strptime(end_date, "%Y%m%d").date() +datetime.timedelta(hours=24)).strftime('%Y%m%d')
    for subdate in gen_date(start_date,p_end_date):
        _single_xml_crawl(date=subdate,city_num=city_num)

def update_index(update_age):
    os.chdir(haystack_path)
    os.system('pwd')
    print "执行 命令 python ./manage.py update_index --age=%s"%(update_age)
    os.system('python ./manage.py update_index --age=%s'%(update_age))
