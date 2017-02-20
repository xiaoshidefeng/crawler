import re
import urllib.request

import pymysql

#打开数据库连接
import sys

import time

print("连接数据库...")
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='crawler', charset='utf8mb4')
print("数据库连接成功")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#存在就删表重建
cursor.execute("DROP TABLE IF EXISTS POSTINFOS")

# 创建表
sql = """CREATE TABLE POSTINFOS (
         ID INT NOT NULL AUTO_INCREMENT,
         POST_REPLY_NUM TEXT,
         POST_TITLE TEXT,
         POST_AUTHOR TEXT,
         POST_CREAT_TIME TEXT,
         PRIMARY KEY (ID))"""

cursor.execute(sql)

def insert(replynum,posttitle,postauthor,creattime):
    sqlorder = """INSERT INTO POSTINFO(POST_REPLY_NUM,POST_TITLE,POST_AUTHOR,POST_CREAT_TIME) VALUES ('"""+replynum+"'"+","+"'"+posttitle+"'"+","+"'"+postauthor+"'"+","+"'"+creattime+"')"
    try:
        # 执行sql语句
        cursor.execute(sqlorder)
        # 提交到数据库执行
        db.commit()
        print("数据库写入成功")
    except:
        # 如果发生错误
        print("数据库写入失败")

if __name__ == "__main__":
    pageurl = ''
    pageurl = input("是否开始爬取数据（y/n）")
    if(pageurl=='n'):
        sys.exit(0)
    pagenum = 0

    initial_page = "http://tieba.baidu.com/f?kw=%E4%B8%BD%E6%B0%B4%E5%AD%A6%E9%99%A2&ie=utf-8&pn="
    webheader = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
           }
    while pagenum<=92700:
        newpage = initial_page + str(pagenum)
        req = urllib.request.Request(url=newpage, headers=webheader)
        webPage = urllib.request.urlopen(req)
        contentBytes = webPage.read()
        contentBytes = contentBytes.decode('UTF-8')

        for onepost in set(re.findall( r'<div class="col2_left j_threadlist_li_left">(.*?)<div class="threadlist_detail clearfix">', str(contentBytes), re.S)):  # 正则表达式找图
            replyNumber = re.findall( r'title="回复">(.*?)</span>', onepost , re.S)
            postTitle = re.findall( r'<a href=".*?" title="(.*?)" target="_blank"', onepost , re.S)
            postAuthor = re.findall( r'title="主题作者:(.*?)"', onepost , re.S)
            postCreatTime = re.findall( r'title="创建时间">(.*?)</span>', onepost , re.S)

            print("回复时间："+replyNumber[0])
            print("帖子标题：" + postTitle[0])
            print("帖子作者：" + postAuthor[0])
            print("创建时间：" + postCreatTime[0])
            insert(replyNumber[0],postTitle[0],postAuthor[0],postCreatTime[0])
            print("---------------------------------")
        print("开始休眠")
        time.sleep(3)
        print("休眠结束")
        print("---------------------------------")
        pagenum=pagenum+50

    print("数据抓取完毕 程序运行结束")
# 关闭数据库连接
db.close()
