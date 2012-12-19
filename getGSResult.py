#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,urllib
import simplejson
import xlrd,xlwt
import os,re,time

#获取excel数据
def open_excel(file= 'key.xlsx'):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)



#q：搜索内容
#rsz：每页显示条数
#start：第几页

def searchstr(strlist):
    psize = 8
    searchlist = []
    searchlist.append('KeyWord')
    grlist = []
    grlist.append('Google Rank')
    urllist = []
    urllist.append('KeyWord Url')
    weblist = []
    weblist.append('Website')
    for str in strlist:
        seachstr = str
        print seachstr
        for x in range(8):
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
                #print results['responseData']['cursor']
            except Exception,e:
                print e
            else:
                #定义Google Rank
                n = psize*x
                for minfo in infoaaa:
                    n += 1
                    #从infoaaa中取出url链接
                    
                    pattern = re.compile(r'dhgate|lightinthebox|madeinchina|aliexpress') 
                    result = re.compile(r'https?://[^/]+?\.([^\.]+)\.[^\.]+(/|$)')
                    website = minfo['url'];
                    print '%d'%n + "\t" + result.findall(website)[0] + "\t" + minfo['url']
                    match = pattern.search(minfo['url']) 
                    if match: 
                        searchlist.append(seachstr)
                        grlist.append(n)
                        urllist.append(minfo['url'])
                        weblist.append(minfo['url'])
            time.sleep(10)
    createNewData(searchlist,grlist,urllist,weblist)


#从excel的index标签获取值
def excel_data_byindex(file='key.xlsx',colindex=0,by_index=0):
    #打开excel表单
    excel = open_excel()
    #检查表单名字
    excel.sheet_names()
    #得到第一张表单：
    sheet =excel.sheet_by_index(by_index)
    #获取第二列信息
    first_columu = sheet.col_values(colindex)
    strlist = []
    #获取第二列每行的值，并进行搜索
    #for num in range (1,len(first_columu)):
    for num in range (1,len(first_columu)):
        str = first_columu[num].encode("utf-8")
        strlist.append(str)
    return strlist

def createNewData(searchlist,grlist,urllist,weblist):
    #创建工作簿
    file = xlwt.Workbook()
    #创建工作表(sheet),命名为:统计结果
    table = file.add_sheet('Search Result')
    
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() #为样式创建字体
    font.name = 'Times New Roman'
    font.bold = True
    style.font = font #为样式设置字体

    #为excel赋值，共四列
    for index,strnum in enumerate(searchlist):
        table.write(index,0,strnum,style)

    for index2,website in enumerate(weblist):
        table.write(index2,1,website,style)

    for index3,gr in enumerate(grlist):
        table.write(index3,2,gr,style)

    for index4,url in enumerate(urllist):
        table.write(index4,3,url,style)

    #开启重复写   
    table = file.add_sheet('sheet name',cell_overwrite_ok=True )

    #保存文件
    fname = "data" + time.strftime('%Y-%m-%d',time.localtime(time.time())) + ".xls";
    print "FileName is:"+fname
    file.save(fname) 

def main():
    #名为key.xlsx的excel文件的第一个tab下的第二列
    strlist = excel_data_byindex("key.xlsx",1,0)
    print len(strlist)
    searchstr(strlist)
    #createNewData()

if __name__ == "__main__":
    main()

