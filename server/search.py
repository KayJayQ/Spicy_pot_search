#!/usr/bin/python
# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import lxml.html

stop = set(stopwords.words('english'))
page_dir = "E:/WEBPAGES_RAW"

def start_search(query:str,cursor):
    
    lemmatizer = WordNetLemmatizer()
    query_words = word_tokenize(query)
    query_words = [lemmatizer.lemmatize(word.lower()) for word in query_words]
    query_words = list(filter(lambda x:(x.isalnum() and x not in stop),query_words))
    
    length = len(query_words)
    
    if length == 1:
        res = one_word_query(query_words[0],cursor)
        return res
    
    if length == 2:
        res = two_words_query(query_words[0] + " " + query_words[1],cursor)
        return res
    
    if length > 2:
        res = multi_words_query(query_words, cursor)
        return res

def decorate(docs:list)->list:
    res = []
    for i in docs:
        url = i[2]
        index = int(i[0])
        file = open(page_dir+f"/{index//500}/{index%500}",'r',encoding="utf-8")
        text = ""
        for line in file:
            text += line.rstrip('\n')
        file.close()
        text = lxml.html.fromstring(text.encode(encoding="utf-8"))
        title = ""
        temp = text.xpath("//title")
        if len(temp) > 0:
            title = temp[0].text
        else:
            title = text.text_content()[:50] + "..."
        des = text.text_content()[:400]
        res.append((url,title,des,index))
    return res

def one_word_query(word:str,c):
    c.execute(f"SELECT * FROM token WHERE word = '{word}';")
    res = c.fetchone()
    if res == None:
        return []
    _,postings = res
    postings = postings.split(';')[:-1]
    #ranking classes: T,A T A Normal
    rc1 = []
    rc2 = []
    rc3 = []
    rc4 = []
    for item in postings:
        doc,tfidf,tag = item.split(',')
        doc = int(doc)
        tfidf = float(tfidf)
        c.execute(f"SELECT * FROM docs WHERE position = {int(doc)};")
        doc,url,doc_length = c.fetchone()
        c.execute(f"SELECT * FROM anchor WHERE url = '{url}';")
        anchors = c.fetchall()
        tag = True if int(tag) == 1 else False
        if(len(anchors) > 0):
            anchors = anchors[0][1]
        else:
            anchors = None
        if anchors == None:
            anchor = False
        elif word in anchors:
            anchor = True
        else:
            anchor = False
        data = (doc,tfidf,url,doc_length)
        if tag and anchor:
            rc1.append(data)
        if tag and not anchor:
            rc2.append(data)
        if not tag and anchor:
            rc3.append(data)
        if not tag and not anchor:
            rc4.append(data)
#     print("rc1",len(rc1))
#     print(rc1)
#     print("rc2",len(rc2))
#     print(rc2)
#     print("rc3",len(rc3))
#     print(rc3)
#     print("rc4",len(rc4))
#     print(rc4)
    for i in range(len(rc1)):
        rc1[i] = rc1[i] + (rc1[i][1]/rc1[i][3],)
    for i in range(len(rc2)):
        rc2[i] = rc2[i] + (rc2[i][1]/rc2[i][3],)
    for i in range(len(rc3)):
        rc3[i] = rc3[i] + (rc3[i][1]/rc3[i][3],)
    for i in range(len(rc4)):
        rc4[i] = rc4[i] + (rc4[i][1]/rc4[i][3],)
    res = []
    rc1 = sorted(rc1,key=lambda x:-x[4])
    rc2 = sorted(rc2,key=lambda x:-x[4])
    rc3 = sorted(rc3,key=lambda x:-x[4])
    rc4 = sorted(rc4,key=lambda x:-x[4])
    
    rc1 += [0,0,0,0]
    rc2 += [0,0,0]
    rc3 += [0,0]
    rc4 += [0]
    
    res += rc1[:4]+rc2[:3]+rc3[:2]+rc4[:1]
    res += rc1[4:]+rc2[3:]+rc3[2:]+rc4[1:]
    res = list(filter(lambda x:x!=0,res))
    return res

def two_words_query(word:str,c):
    print(word)
    c.execute(f"SELECT * FROM token2 WHERE word = '{word}';")
    res = c.fetchone()
    if res == None:
        return multi_words_query(word.split(), c)
    _,postings = res
    postings = postings.split(';')[:-1]
    #ranking classes: T,A T A Normal
    rc1 = []
    rc2 = []
    rc3 = []
    rc4 = []
    for item in postings:
        doc,tfidf,tag = item.split(',')
        doc = int(doc)
        tfidf = float(tfidf)
        c.execute(f"SELECT * FROM docs WHERE position = {int(doc)};")
        doc,url,doc_length = c.fetchone()
        c.execute(f"SELECT * FROM anchor WHERE url = '{url}';")
        anchors = c.fetchall()
        tag = True if int(tag) == 1 else False
        if(len(anchors) > 0):
            anchors = anchors[0][1]
        else:
            anchors = None
        if anchors == None:
            anchor = False
        elif word.split()[0] in anchors or word.split()[1] in anchors:
            anchor = True
        else:
            anchor = False
        data = (doc,tfidf,url,doc_length)
        if tag and anchor:
            rc1.append(data)
        if tag and not anchor:
            rc2.append(data)
        if not tag and anchor:
            rc3.append(data)
        if not tag and not anchor:
            rc4.append(data)
    for i in range(len(rc1)):
        rc1[i] = rc1[i] + (rc1[i][1]/rc1[i][3],)
    for i in range(len(rc2)):
        rc2[i] = rc2[i] + (rc2[i][1]/rc2[i][3],)
    for i in range(len(rc3)):
        rc3[i] = rc3[i] + (rc3[i][1]/rc3[i][3],)
    for i in range(len(rc4)):
        rc4[i] = rc4[i] + (rc4[i][1]/rc4[i][3],)
    res = []
    rc1 = sorted(rc1,key=lambda x:-x[4])
    rc2 = sorted(rc2,key=lambda x:-x[4])
    rc3 = sorted(rc3,key=lambda x:-x[4])
    rc4 = sorted(rc4,key=lambda x:-x[4])
    
    rc1 += [0,0,0,0]
    rc2 += [0,0,0]
    rc3 += [0,0]
    rc4 += [0]
    
    res += rc1[:4]+rc2[:3]+rc3[:2]+rc4[:1]
    res += rc1[4:]+rc2[3:]+rc3[2:]+rc4[1:]
    res = list(filter(lambda x:x!=0,res))
    return res

def multi_words_query(words:list, c):
    found = False
    for word in words:
        c.execute(f"SELECT * FROM token WHERE word = '{word}';")
        if c.fetchone() != None:
            found = True
    if not found:
        return []
    
    rc1 = []
    rc2 = []
    rc3 = []
    rc4 = []
    
    for term in words:
        c.execute(f"SELECT * FROM token WHERE word = '{term}';")
        res = c.fetchone()
        if res == None:
            continue
        _,postings = res
        postings = postings.split(';')[:-1]
        
        for item in postings:
            doc,tfidf,tag = item.split(',')
            doc = int(doc)
            tfidf = float(tfidf)
            c.execute(f"SELECT * FROM docs WHERE position = {int(doc)};")
            doc,url,doc_length = c.fetchone()
            c.execute(f"SELECT * FROM anchor WHERE url = '{url}';")
            anchors = c.fetchall()
            tag = True if int(tag) == 1 else False
            if(len(anchors) > 0):
                anchors = anchors[0][1]
            else:
                anchors = None
            if anchors == None:
                anchor = False
            elif word in anchors:
                anchor = True
            else:
                anchor = False
            data = (term,doc,tfidf,url,doc_length)
            if tag and anchor:
                rc1.append(data)
            if tag and not anchor:
                rc2.append(data)
            if not tag and anchor:
                rc3.append(data)
            if not tag and not anchor:
                rc4.append(data)
    
    #CUT
    rc4 = rc4[:300]
    
    #Calculate Cosine Similarity
    score_1 = [0 for i in range(len(rc1))]
    for term in words:
        for i in range(len(rc1)):
            if rc1[i][0] == term:
                score_1[i] += rc1[i][2]
    for i in range(len(rc1)):
        score_1[i] = score_1[i]/rc1[i][4]
        rc1[i] += (score_1[i],)
    
    score_2 = [0 for i in range(len(rc2))]
    for term in words:
        for i in range(len(rc2)):
            if rc2[i][0] == term:
                score_2[i] += rc2[i][2]
    for i in range(len(rc2)):
        score_2[i] = score_2[i]/rc2[i][4]
        rc2[i] += (score_2[i],)
    
    score_3 = [0 for i in range(len(rc3))]
    for term in words:
        for i in range(len(rc3)):
            if rc3[i][0] == term:
                score_3[i] += rc3[i][2]
    for i in range(len(rc3)):
        score_3[i] = score_3[i]/rc3[i][4]
        rc3[i] += (score_3[i],)
    
    score_4 = [0 for i in range(len(rc4))]
    for term in words:
        for i in range(len(rc4)):
            if rc4[i][0] == term:
                score_4[i] += rc4[i][2]
    for i in range(len(rc4)):
        score_4[i] = score_4[i]/rc4[i][4]
        rc4[i] += (score_4[i],)
    
    res = []
    rc1 = sorted(rc1,key=lambda x:-x[5])
    rc2 = sorted(rc2,key=lambda x:-x[5])
    rc3 = sorted(rc3,key=lambda x:-x[5])
    rc4 = sorted(rc4,key=lambda x:-x[5])
    
    rc1 += [0,0,0,0]
    rc2 += [0,0,0]
    rc3 += [0,0]
    rc4 += [0]
    
    res += rc1[:4]+rc2[:3]+rc3[:2]+rc4[:1]
    res += rc1[4:]+rc2[3:]+rc3[2:]+rc4[1:]
    res = list(filter(lambda x:x!=0,res))
    p_w = dict()
    for item in res[:10]:
        p_w[item[1]] = position_weight(f"{page_dir}/{item[1]//500}/{item[1]%500}", words)
    new_res = sorted(res[:10],key=lambda x:p_w[x[1]])
    
    if len(res) <= 10:
        to_return = new_res
        res = []
        for item in to_return:
            res.append(item[1:])
        return res
    else:
        to_return = new_res + res[10:]
        res = []
        for item in to_return:
            res.append(item[1:])
        return res
    
def position_weight(doc,query):
    file = open(doc,'r',encoding="utf-8")
    txt = ""
    for line in file:
        txt += line
    length = len(txt)
    file.close()
    means = []
    for term in query:
        count = 0
        pos = []
        for index,word in enumerate(txt.split()):
            if term == word:
                pos.append(index/length)
                count += 1
        if count == 0:
            continue
        means.append(sum(pos)/count)
    if len(means) == 0:
        return 0
    mbar = sum(means)/len(means)
    s = 0
    for i in means:
        s += (i-mbar)**2
    s = s/len(means)
    return s
    
if __name__ == '__main__':
    import pymysql
    query = "178 random forest"
    connection = pymysql.connect(host="192.168.1.62",port=3306,user="root",db="spicy_pot")
    cursor = connection.cursor()
    res = start_search(query,cursor)
    print(res)
    connection.close()