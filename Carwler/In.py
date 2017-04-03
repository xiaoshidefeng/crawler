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
cursor.execute("DROP TABLE IF EXISTS INFASHION")

# 创建表
sql = """CREATE TABLE INFASHION (
         ID INT NOT NULL AUTO_INCREMENT,
         COMMENT_TIME TEXT,
         COMMENT_AUTHOR TEXT,
         COMMENT_CONTENT TEXT,
         PRIMARY KEY (ID))"""

cursor.execute(sql)

def insert(commentTime,commentAuthor,commentContent):
    sqlorder = """INSERT INTO INFASHION(COMMENT_TIME,COMMENT_AUTHOR,COMMENT_CONTENT) VALUES ('"""+commentTime+"'"+","+"'"+commentAuthor+"'"+","+"'"+commentContent+"')"
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
    pagenum = 1

    initial_page = "http://www.wandoujia.com/apps/com.jiuyan.infashion/comment"
    webheader = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
           }
    while pagenum<=51:
        newpage = initial_page + str(pagenum)
        req = urllib.request.Request(url=newpage, headers=webheader)
        webPage = urllib.request.urlopen(req)
        contentBytes = webPage.read()
        contentBytes = contentBytes.decode('UTF-8')

        for onepost in set(re.findall( r'<li class="normal-li">(.*?)</p></li>', str(contentBytes), re.S)):  # 正则表达式找图

            print(onepost)

            # postCreatTime = re.findall( r'title="创建时间">(.*?)</span>', onepost , re.S)
            commenttime = re.findall(r'</span><span>(.*?)</span></p><p class="cmt-content">', onepost, re.S)
            print("回复时间："+commenttime[0])

            commentcontent = re.findall(r'<p class="cmt-content"><span>(.*?)</span>', onepost, re.S)
            print("帖子标题：" + commentcontent[0])
            commentauthor = re.findall(r'<span class="name">(.*?)</span><span>', onepost, re.S)
            print("帖子作者：" + commentauthor[0])
            # //print("创建时间：" + postCreatTime[0])
            insert(commenttime[0],commentauthor[0],commentcontent[0])
            print("---------------------------------")
        # print("开始休眠")
        # time.sleep(3)
        # print("休眠结束")
        # print("---------------------------------")
        pagenum=pagenum+1

    print("数据抓取完毕 程序运行结束")
# 关闭数据库连接
db.close()
