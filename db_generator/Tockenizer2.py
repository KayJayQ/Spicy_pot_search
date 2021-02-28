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


def tockenize_page(page):
    file = open(page,'r',encoding="utf-8")
    text = ""
    for line in file:
        text += line.rstrip("\n")
    file.close()
    text = lxml.html.fromstring(text).text_content()
    text = text.replace("\n","")

    to_remove = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    raw_words = word_tokenize(text)
    words = [str(lemmatizer.lemmatize(word.lower())) for word in raw_words]
    words = filter(lambda x:x not in to_remove, words)
    words = list(filter(lambda x:x.isalnum(), words))

    two_gram = []
    for i in range(len(words)-1):
        two_gram.append(f"{words[i]} {words[i+1]}")

    res = dict()
    for word in two_gram:
        if word in res.keys():
            res[word] += 1
        else:
            res[word] = 1
    return res

if __name__ == "__main__":

    base_dir = "../WEBPAGES_CLEAN"
    dir_range = range(75)

    big_table = dict()

    for p in dir_range:
        print("page",p)
        for chap in range(500):
            if p == 74 and chap == 497:
                save = open("save2.txt",'w',encoding = "utf-8")
                for k,v in big_table.items():
                    save.write(f"{k} {v[0]} {v[1]}\n")
                save.close()
            if p % 10 == 0:
                save = open(f"t{p//10}.txt",'w',encoding = "utf-8")
                for k,v in big_table.items():
                    save.write(f"{k} {v[0]} {v[1]}\n")
                save.close()
            try:
                words = tockenize_page(f"{base_dir}/{p}/{chap}")
            except Exception as e:
                print(e)
                continue

            try:
                for k,v in words.items():
                    k = str(k)
                    v = int(v)
                    if k not in big_table.keys():
                        big_table[k] = [v,f"{p}:{chap},{v};"]
                    else:
                        big_table[k][0] += v
                        big_table[k][1] += f"{p}:{chap},{v};"
            except Exception as e:
                print(p,chap,e)
                continue

                    
            
    print("done")

    
    
    
