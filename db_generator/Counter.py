#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb 14, 2020

@author: qiangkejia
'''

import lxml.html
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pymysql


def count(page):
    file = open(page,'r',encoding="utf-8")
    text = ""
    for line in file:
        text += line.rstrip("\n")
    file.close()
    text = lxml.html.fromstring(text).text_content()
    text = text.replace("\n","")

    to_remove = set(stopwords.words('english'))
    raw_words = word_tokenize(text)
    return len(raw_words)

if __name__ == "__main__":
    connection = pymysql.connect(host="localhost",port=3306,user="root",db="indexes",cursorclass=pymysql.cursors.DictCursor)
    c = connection.cursor()
    c.execute("select * from token")

    base_dir = "../WEBPAGES_CLEAN"
    dir_range = range(72,75)

    big_table = dict()

    for p in dir_range:
        print("page",p)
        for chap in range(500):
            if p == 74 and chap == 497:
                save = open("doc1.txt",'w',encoding = "utf-8")
                for k,v in big_table.items():
                    save.write(f"{k} {v}\n")
                save.close()
            try:
                length = count(f"{base_dir}/{p}/{chap}")
            except Exception as e:
                print(e)
                continue

            try:
                big_table[f"{p}:{chap}"] = length
            except Exception as e:
                print(p,chap,e)
                continue

                    
            
    print("done")

    '''
            for k,v in words.items():
                try:
                    if c.execute(f"select * from token where word = '{k}'") == 0:
                        c.execute(f"insert into token (word,total,freqs) values ('{k}','{v}','{p}:{chap},{v};')")
                        connection.commit()
                    else:
                        c.execute(f"select * from token where word = '{k}'")
                        temp = c.fetchone()
                        total = temp['total']
                        total += v
                        freqs = temp['freqs']
                        freqs += f"{p}:{chap},{v};"
                        c.execute(f"update token set total = '{total}', freqs = '{freqs}' where word = '{k}'")
                        connection.commit()
                except Exception as e:
                    print(e)
                    continue
    '''

    
    
    
