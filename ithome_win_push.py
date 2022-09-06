#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author    : feller


import requests, json, sys, re
import time
from datetime import datetime, timedelta
import os
from winotify import Notification

def sleeptime(hour, min, sec):
    return hour * 3600 + min * 60 + sec


def push(title, msg, app_id, urlurl):
    title = title
    msg = msg
    app_id = app_id
    urlurl = urlurl

    # r"D:\Python\demo\wechat.png"
    toast = Notification(app_id=app_id, title=title, msg=msg, icon=r"D:\Python\demo\wechat.png")
    toast.add_actions(label="查看详情",
                      launch=f"{urlurl}")
    toast.show()
    
class bzMonitor():
    
    def echoMsg(self, level, msg):
        if level == 'Info':
            print('[Info] %s' % msg)

        elif level == 'Error':
            print('[Error] %s' % msg)
            
    def __init__(self, ):
        self.reqHeaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'Content-Type': 'application/x-www-form-urlencoded',

            'Connection': 'close',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
        }

        

    

    # 获取各用户当前新闻数目
    def getBZQueue(self):
        try:
            url = 'https://api.ithome.com/json/newslist/news?r=0'

            res = requests.get(url=url)

            res = res.text
            jsonobj = json.loads(res)
            toCntPercent = jsonobj['newslist']
            with open("D:\\Python\\newsid.txt", 'a', encoding='utf-8') as f:
                for i in toCntPercent:
                    # print(i['newsid'])
                    jk = i['newsid']
                    f.write(str(jk) + '\n')
            self.echoMsg('Info', '新闻数目获取成功')
        except Exception as e:
            self.echoMsg('Error', e)
            sys.exit()

    # 监控函数
    def startbzmonitor(self, ):

        returnDict = {}  # 获取新闻相关内容
        try:
            bilibili = []
            with open("D:\\Python\\newsid.txt", 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip('\n')
                    bilibili.append(line)
            url = 'https://api.ithome.com/json/newslist/news?r=0'

            res = requests.get(url=url)

            res = res.text
            jsonobj = json.loads(res)
            toCntPercent = jsonobj['newslist']
            for dynamic_idd in toCntPercent:
                jk = dynamic_idd['newsid']
                if str(jk) not in bilibili:
                    with open("D:\\Python\\newsid.txt", 'a', encoding='utf-8') as f:
                        f.write(str(jk) + '\n')
                        self.echoMsg('Info', 'IT之家新闻更新啦!!!')
                        title = dynamic_idd['title']
                        description = dynamic_idd['description']
                        app_id = dynamic_idd['postdate'] + "[" + str(dynamic_idd['commentcount']) + "评]"
                        urlurl = "https://www.ithome.com/" + dynamic_idd['url']

                        print(title)
                        push(title, description, app_id, urlurl)







        except Exception as e:
            self.echoMsg('Error', e)
            sys.exit()





if __name__ == '__main__':
    b = bzMonitor()
    # b.getbzurl()
    with open("D:\\Python\\newsid.txt", 'r', encoding='utf-8') as f2:
        text = f2.read()
        if text == '':
            b.getBZQueue()

        second = sleeptime(0, 0, 120)
        while 1 == 1:
            time.sleep(second)

            b.startbzmonitor()
