#! /usr/bin/python3
# Author:Zzf
# -*- coding = utf-8 -*-
# @Time :2021/4/4 20:40
# @File :spider.py
# @Software :PyCharm
import re
from bs4 import BeautifulSoup
import urllib.request,urllib.error
from urllib import parse
import json
from tkinter import *
from tkinter import scrolledtext
from DB import init_db,saveData
import os


#定义一个全局变量jobList,用来存放爬取到的所有职位信息
jobList = [] #存储所有职位信息 格式[{},{},{}...]
#数据库路径
dbpath = "./51job.db"


def main():
    num = inputnum.get()
    if os.path.exists(dbpath):
        pass
    else:
        init_db(dbpath)
    for i in range(1,int(num)+1):  #爬取该职位前n页信息
        kw = inputkw.get()
        keyword = parse.quote(parse.quote(kw))
        url = "https://search.51job.com/list/000000,000000,0000,00,9,99," + keyword + ",2," + str(i) + ".html"
        pageLink = getLink(url,keyword)
        if len(pageLink) == 0:
            break
        for jobPage in pageLink:
            getData(jobPage)
    txt.insert(END,"正在保存数据...\n")
    saveData(jobList,dbpath)
    txt.insert(END,"数据已保存\n")
    txt.insert(END,"爬取完成！\n")

#得到指定一个URL的网页内容
def askURL(url):
    head = {      #模拟浏览器访问该服务器
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 "
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
        # print(html)
    except urllib.error.URLError as e:      #捕获异常
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


# 通过岗位详情页获得职位的具体信息
def getData(jobPage):
    jobHtml = askURL(jobPage)  #获取详情页
    bs = BeautifulSoup(jobHtml, "html.parser")
    for job in jobList:
        if jobPage == job["link"]:
            #职位名称：
            jobname = bs.select(".cn>h1")
            if jobname[0]["title"] :
                job["jobname"] = jobname[0]["title"]
            else:
                job["jobname"] = " "
            txt.insert(END,jobname[0]["title"]+"----"+job["link"]+"\n"+"\n")
            txt.see(END)
            txt.update()
            #公司名称：
            companyname = bs.select(".cn>.cname>.catn")
            job["companyname"] = companyname[0]["title"]
            #工资(保存最低工资)：
            salary = bs.select(".cn>strong")
            findLSalary = re.compile(r'(\d+\.?\d*?)-', re.S)
            if salary[0].string:
                L = re.findall(findLSalary, salary[0].string)
                if L:
                    job["salary"] = L[0]
                else:
                    job["salary"] = 0
            else:
                job["salary"] = 0

            #msg包括工作地点、经验要求、学历要求、招聘人数、发布时间：
            msg = bs.select(".ltype")
            msg = msg[0]["title"].split("|")  #msg形成列表形式
            #工作地点
            job["place"] = ''.join(msg[0].split("-")[0].strip())
            #工作经验
            ex = ''.join(msg[1].split())
            findExp = re.compile(r'(\d+)', re.S)
            exp = re.findall(findExp,ex)
            if len(exp) == 0:
                job["experience"] = 0
            else :
                job["experience"] = exp[0]
            #学历要求
            job["edu"] = ''.join(msg[2].split())
            #工作描述
            jobMsgList = bs.select(".job_msg")  # 工作描述
            jobMsgStr = ""
            for str in jobMsgList:
                jobMsgStr = jobMsgStr + str.text
            jobMsgStr = jobMsgStr.replace(';','\;')  #过滤特殊符号
            jobMsgStr = jobMsgStr.replace('\\', ' ')
            jobMsgStr = jobMsgStr.replace('\'', ' ')
            jobMsgStr = jobMsgStr.replace(':', ' ')
            jobMsgStr = jobMsgStr.replace(',', '\,')
            job["info"] = ''.join(jobMsgStr.split())



#获取每个岗位的详情页面链接
def getLink(url,keyword):
    jobLink = []  #存放每个职位的链接，格式[{"link":"...."},{},{}...]
    html = askURL(url)
    bs = BeautifulSoup(html, "html.parser")
    data = bs.select("script[type='text/javascript']")[2]
    a1 = data.string.split(" = ")[1]
    res = json.loads(a1) #获取到动态数据
    link = res["engine_search_result"]  #获取到岗位信息(列表-字典)
    for i in link:  #i即每个岗位
        for key,value in i.items():
            if key == "job_href" and re.match(r'https://jobs.51job.com/(.*)',value) != None:
                jobLink.append(value)
                # print(value)
                jobList.append({"link":value,"keyword":keyword})
    return jobLink


#GUI界面
root = Tk()
root.title('51job爬虫')
root.geometry("550x750")
root.resizable(0, 0)
#输入爬取岗位
tip = Label(root, text='请输入您要爬取的岗位：')
inputkw = Entry(root)
inputkw.place(relx=0.5, y=1, relheight=0.04)
#指定爬取的数量
tip2 = Label(root, text='请输入您要爬取的总页数：')
inputnum = Entry(root)
#开始按钮
btn = Button(root, text='开始爬取', command=main)
#爬取过程显示框
txt = scrolledtext.ScrolledText(root)
#布局
txt.place(relx=0.05, y=120, relheight=0.8, relwidth=0.9)
tip.place(relx=0.1, y=1, relheight=0.05)
tip2.place(relx=0.1, y=40, relheight=0.05)
inputnum.place(relx=0.5, y=40, relheight=0.04)
btn.place(relx=0.4, y=80, relheight=0.04)
root.mainloop()


