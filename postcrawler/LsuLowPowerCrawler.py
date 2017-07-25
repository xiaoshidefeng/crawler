# encoding: utf-8
import re
import urllib.request
# from urllib2 import urlopen
import pymysql

#打开数据库连接
import sys

import time


print("连接数据库...")
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='cw1330661071', db='lslowpowerdb', charset='utf8mb4')
print("数据库连接成功")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

#存在就删表重建
cursor.execute("DROP TABLE IF EXISTS lowpower")

# 创建表
sql = """CREATE TABLE lowpower (
         POWER_ID INT NOT NULL AUTO_INCREMENT,
         BUILDING_NAME TEXT,
         DORM_NUM TEXT,
         RESIDUAL_ELECTRICITY TEXT,
         DATE_NUM TEXT,
         PRIMARY KEY (POWER_ID))"""

cursor.execute(sql)

def insert(buildingname, dormnum, reselectricity, datenum):
    sqlorder = """INSERT INTO lowpower(BUILDING_NAME,DORM_NUM,RESIDUAL_ELECTRICITY,DATE_NUM) VALUES ('"""+buildingname+"'"+","+"'"+dormnum+"'"+","+"'"+reselectricity+"'"+","+"'"+datenum+"')"
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
    count = 1

    initial_page = "http://www.houqinbao.com/index.php?s=/addon/CustomReply/CustomReply/detail/token/gh_b46e816c9261/openid/oJZkxt7LGlxClxlqmxJ-cL60RMkU/id/906.html"


    webheader = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
           }

    while count < 100000:
        # 存在就删表重建
        cursor.execute("DROP TABLE IF EXISTS lowpower")
        cursor.execute(sql)

        req = urllib.request.Request(url=initial_page, headers=webheader)
        webPage = urllib.request.urlopen(req)
        contentBytes = webPage.read()
        contentBytes = contentBytes.decode('UTF-8')

        daytime = re.findall( r'<p>以下内容更新时间：(.*?)</p>', str(contentBytes), re.S)

        for onelowpower in set(re.findall( r'<tr height="18" style="height:18px">(.*?)</tr>', str(contentBytes), re.S)):

            # print(onelowpower)
            buildingname = re.findall(r'<td height="18" style="border-top: none;">(.*?)</td>', onelowpower, re.S)
            # replyNumber = re.findall( r'title="回复">(.*?)</span>', onepost , re.S)
            dormInfo = re.findall(r'<td style="border-top:none;border-left:none">(.*?)</td>', onelowpower, re.S)
            # postTitle = re.findall( r'<a href=".*?" title="(.*?)" target="_blank"', onepost , re.S)
            # postAuthor = re.findall( r'title="主题作者:(.*?)"', onepost , re.S)
            # postCreatTime = re.findall( r'title="创建时间">(.*?)</span>', onepost , re.S)
            #
            #
            print("幢：" + buildingname[0])
            print("寝室号：" + dormInfo[0])
            print("剩余电量：" + dormInfo[1])
            print("更新时间：" + daytime[0])
            insert(buildingname[0], dormInfo[0],dormInfo[1], daytime[0])
            print("---------------------------------")

        print("今日数据抓取完毕" + time.ctime())
        print("共抓取" + str(count) + "次")
        time.sleep(7200)
        count = count + 1
# 关闭数据库连接
db.close()