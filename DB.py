#! /usr/bin/python3
# Author:Zzf
# -*- coding = utf-8 -*-
# @Time :2021/4/4 20:55
# @File :DB.py
# @Software :PyCharm
import sqlite3


#初始化数据库
def init_db(dbpath):
    sql = '''
        create table job
        (
        id integer primary key autoincrement,
        link text,
        keyword text,
        jobname text,
        companyname text,
        salary text,
        place text,
        experience text,
        educate text,
        info text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


#保存数据(sqlite)
def saveData(jobList,dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    for data in jobList: #data即每条字典

        data = list(data.values())  #把data字典转成列表
        for index in range(len(data)):
            data[index] = "'"+str(data[index])+"'" #转成引号格式
        sql = '''
            insert into job (
                link,keyword,jobname,companyname,salary,place,experience,educate,info
            )values(%s)'''%",".join(data)   #将data列表以逗号分隔
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()




