#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql

connection = pymysql.connect(host="localhost",port=3306,user="root",db="indexes")

c = connection.cursor()

file = open("save.txt",'r',encoding = "utf-8")


for index,line in enumerate(file):
    if index % 1000 == 0:
        print(index)
        connection.commit()
    word,total,freqs = line.split()
    try:
        c.execute(f"INSERT INTO token (word, total, freqs) VALUES ('{word}','{total}','{freqs}')")
    except Exception as e:
        print(e)
        continue


file.close()
