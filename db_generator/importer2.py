#!/usr/bin/python
# -*- coding: utf-8 -*-
import pymysql

connection = pymysql.connect(host="localhost",port=3306,user="root",db="indexes")

c = connection.cursor()

file = open("save2.txt",'r',encoding = "utf-8")


for index,line in enumerate(file):
    if index % 1000 == 0:
        print(index)
        connection.commit()
    word1,word2,total,freqs = line.split()
    word = word1+" "+word2
    try:
        c.execute(f"INSERT INTO token2 (word, total, freqs) VALUES ('{word}','{total}','{freqs}')")
    except Exception as e:
        print(e)
        continue


file.close()
