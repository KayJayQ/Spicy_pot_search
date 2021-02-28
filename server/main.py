#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, abort, render_template
from datetime import timedelta
import pymysql
from search import start_search, decorate

page_dir = "E:/WEBPAGES_RAW"

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

connection = pymysql.connect(host="localhost",port=3306,user="root",db="spicy_pot")
cursor = connection.cursor()

@app.route('/')
def homepage():
    return render_template("root.html")

@app.route('/search')
def search():
    word = request.args.get('s')
    page = int(request.args.get('p'))
    all_res = start_search(word,cursor)
    if len(all_res) == 0:
        return render_template("result.html",result={"word":word,"pages":-1,"currentPage":1,"res":[]})
    
    pages = ((len(all_res)-1)//10) + 1
    res = decorate(all_res[(page-1)*10:page*10])
    content = {"word":word,"pages":pages,"currentPage":page,"res":res}
    return render_template("result.html",result=content)

@app.route('/cache')
def cache():
    p = request.args.get('p')
    c = request.args.get('c')
    read = open(page_dir+"/"+p+"/"+c,'r',encoding="utf-8")
    save = open("templates/temp.html",'w',encoding="utf-8")
    for line in read:
        save.write(line)
    read.close()
    save.close()
    return render_template("temp.html")


app.run(host='0.0.0.0',port=80,debug=True)
