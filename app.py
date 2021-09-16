import jieba
from flask import Flask,render_template
import sqlite3
app = Flask(__name__)

@app.route('/')
def index():
    datalist = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql1 = '''select count(*) from job'''
    num = cur.execute(sql1)
    for item in num:
        datalist.append(item)
    sql2 = '''select keyword from job where id = 1'''
    keyword = cur.execute(sql2)
    for item2 in keyword:
        datalist.append(item2)
    cur.close()
    conn.close()
    return render_template("/index.html", data=datalist)

@app.route('/index.html')
def home():
    datalist = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql1 = '''select count(*) from job'''
    num = cur.execute(sql1)
    for item in num:
        datalist.append(item)
    sql2 = '''select keyword from job where id = 1'''
    keyword = cur.execute(sql2)
    for item2 in keyword:
        datalist.append(item2)
    # sql3 = 'select info from job'
    # data = cur.execute(sql3)
    # text = ""
    # for item in data:
    #     text = text + item[0]
    # cut = jieba.cut(text)
    # string = ' '.join(cut)
    cur.close()
    conn.close()
    return render_template("/index.html", data=datalist)


@app.route('/charts_edu.html')
def charts_salary():
    benke = []
    shuoshi = []
    dazhuan = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql1 = '''select count(*) from job where educate = "本科"'''
    ben = cur.execute(sql1)
    for i in ben:
        benke.append(i)
    sql2 = '''select count(*) from job where educate = "大专"'''
    da = cur.execute(sql2)
    for i in da:
        dazhuan.append(i)
    sql3 = '''select count(*) from job where educate = "硕士"'''
    shuo = cur.execute(sql3)
    for i in shuo:
        shuoshi.append(i)
    cur.close()
    conn.close()
    return render_template("/charts_edu.html",benke = benke,dazhuan = dazhuan,shuoshi=shuoshi)



@app.route('/charts_exper.html')
def charts_exper():
    salary = []
    exper = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql1 = '''select salary,experience from job where salary != '0' order by salary asc,experience asc'''
    # sql2 = '''select place,count(place) from job group by place order by count(place) desc'''
    res = cur.execute(sql1)
    for i in res:
        salary.append(float(i[0])*10000)
        exper.append(i[1])
    cur.close()
    conn.close()
    return render_template("/charts_exper.html",salary=salary,exper=exper)



@app.route('/charts_city.html')
def charts_city():
    keyword = []
    city = []
    num = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql1 = '''select keyword from job where id = 1'''
    sql2 = '''select place,count(place) from job group by place order by count(place) desc'''
    kw = cur.execute(sql1)
    for i in kw:
        keyword.append(i)
    ci = cur.execute(sql2)
    for j in ci:
        city.append(j[0])
        num.append(j[1])
    cur.close()
    conn.close()
    return render_template("/charts_city.html", keyword=keyword, city=city, num=num)



@app.route('/charts_comp.html')
def charts_comp():
    keyword = []
    company = []
    num = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql1 = '''select keyword from job where id = 1'''
    sql2 = '''select companyname,count(companyname) from job group by companyname order by count(companyname) desc'''
    kw = cur.execute(sql1)
    for i in kw:
        keyword.append(i)
    cn = cur.execute(sql2)
    for j in cn:
        company.append(j[0])
        num.append(j[1])
    cur.close()
    conn.close()
    return render_template("/charts_comp.html", keyword=keyword,company = company,num = num)



@app.route('/charts_aver.html')
def charts_aver():
    city = []
    salary = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql = '''select place,AVG(salary) from job where place in ('北京','上海','广州','深圳','杭州','武汉','成都','南京','苏州','东莞','西安','佛山','长沙','汕头') group by place order by AVG(salary) desc'''
    res = cur.execute(sql)
    for item in res:
        city.append(item[0])
        salary.append(float(item[1])*10000)
    return render_template("/charts_aver.html",city = city,salary = salary)



@app.route('/tables.html')
def tables():
    datalist = []
    conn = sqlite3.connect("51job.db")
    cur = conn.cursor()
    sql = '''select * from job'''
    list = cur.execute(sql)
    for item in list:
        datalist.append(item)
    cur.close()
    conn.close()
    return render_template("/tables.html",datalist=datalist)



@app.route('/wordcloud.html')
def wordcloud():
    return render_template("/wordcloud.html")



if __name__ == '__main__':
    app.run()
