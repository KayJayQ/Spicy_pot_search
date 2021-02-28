#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql

connection = pymysql.connect(host="localhost",port=3306,user="root",db="indexes")

c = connection.cursor()

file = open("doc1.txt",'r',encoding = "utf-8")


for index,line in enumerate(file):
    if index % 1000 == 0:
        print(index)
        connection.commit()
    doc,length = line.split()
    try:
        c.execute(f"INSERT INTO doc (position, length) VALUES ('{doc}','{length}')")
    except Exception as e:
        print(e)
        continue

connection.commit()
file.close()
