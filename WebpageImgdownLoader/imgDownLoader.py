#import Queue
import urllib.request
import socket
import re
import sys
import os

saveDir = r"D:\网页图片下载" #文件保存路径
def destFile(path):
    if not os.path.isdir(saveDir):
        os.mkdir(saveDir)
    pos = path.rindex('/')
    t = os.path.join(saveDir,path[pos+1:])
    return t

if __name__ == "__main__":
    pageurl = ''
    pageurl = input("输入要下载图片的网址")


    initial_page = pageurl
    #webheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    webheader = {
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '                            'Chrome/51.0.2704.63 Safari/537.36'
           }
    req = urllib.request.Request(url=initial_page, headers=webheader)
    webPage = urllib.request.urlopen(req)
    contentBytes = webPage.read()
    contentBytes = contentBytes.decode('UTF-8')
    # print(contentBytes)
    #for link, t in set(re.findall(r'(http:[^\s]*?(jpg|png|gif))', str(contentBytes))):
    for link,t, in set(re.findall(r'(http[^\s]*?(jpg|png|gif))',str(contentBytes))): #正则表达式找图
        print(link)
        try:
            urllib.request.urlretrieve(link, destFile(link))
        except:
            print("错误")