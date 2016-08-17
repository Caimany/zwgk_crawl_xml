# -*- coding:utf-8 -*-
import re

class base_isourl(object):
    def __init__(self):
        self.compile_pattern=re.compile(r'\w+/$')

    def _pre_one(self,uri):
        # print re.sub(r'\w+/$','',uri)
        # compile_pattern=re.compile(r'\w+/$')
        return self.compile_pattern.sub('',uri)

    def isouri(self,uri):
        list_uri=uri.split('../',1)

        if len(list_uri) == 1:
            return list_uri[0]
        else:
            uri_pre=self._pre_one(list_uri[0])
            uri_next=list_uri[1]
            return self.isouri(uri_pre+uri_next)
