#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,urllib
import simplejson
#q：搜索内容
#rsz：每页显示条数
#start：第几页

seachstr = 'china'
psize = 8
for x in range(15):
   # print "page:%s"%(x+1)
    if(x==0):
        page = 1
    else:
        page = x * psize

    url =('https://ajax.googleapis.com/ajax/services/search/web'
                  '?v=1.0&q=%s&rsz=%s&start=%s') %(urllib.quote(seachstr),psize,page)
    try:
        request = urllib2.Request(
        url, None, {'Referer': 'http://www.sina.com'})

        response = urllib2.urlopen(request)
        # Process the JSON string.
        #得到json的数据格式，利用json在线校验器可以得到清晰的样式。
        results = simplejson.load(response)
        #从results中取出results
        infoaaa = results['responseData']['results']
    except Exception,e:
        print e
        pass
    else:
        #定义Google Rank
        n = psize*x
        for minfo in infoaaa:
            n += 1
            #从infoaaa中取出url链接
            print n
            print minfo['url']
            