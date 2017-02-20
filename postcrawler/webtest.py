import re
import urllib.request

import pymysql

#打开数据库连接
import sys

import time




if __name__ == "__main__":
    pageurl = ''
    pageurl = input("是否开始爬取数据（y/n）")
    if(pageurl=='n'):
        sys.exit(0)
    pagenum = 0

    initial_page = "http://lsuplus.top/"
    webheader = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
           }
    while pagenum<=92700:
        req = urllib.request.Request(url=initial_page, headers=webheader)
        webPage = urllib.request.urlopen(req)
        contentBytes = webPage.read()
        contentBytes = contentBytes.decode('UTF-8')
        pagenum = pagenum + 1
        print(pagenum)



