#!/usr/bin/env python
import http.client
import json
import base64
import random
import binascii
import numpy
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

f=open("ML_Data.txt", "r")
if f.mode == 'r':
    lines = f.readlines()
    vec_opts = {
        "ngram_range": (1, 4),  # allow n-grams of 1-4 words in length (32-bits)
        "analyzer": "word",     # analyze hex words
        "token_pattern": "..",  # treat two characters as a word (e.g. 4b)
        "min_df": 0,          # for demo purposes, be very selective about features
    }
    v = CountVectorizer(**vec_opts)
    idf_opts = {"use_idf": True}
    idf = TfidfTransformer(**idf_opts)
    data_stack = []
    target_stack = []
    for x in lines:
        data = ""
        jsondata = json.loads(x)
        data_train = (base64.b64decode(jsondata['base64']))
        target_train = jsondata['target']
        hex_train = binascii.hexlify(data_train)
        data_stack.append(str(hex_train))
        target_stack.append(target_train)

from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('vec',   CountVectorizer(**vec_opts)),
    ('idf',  TfidfTransformer(**idf_opts)),
    ('clf', LinearSVC())
])

Z = pipeline.fit(data_stack, target_stack)

cookie = ""

def initialize():
    global cookie
    c = http.client.HTTPSConnection("mlb.praetorian.com")
    c.request("GET", "/challenge")
    response = c.getresponse()
    print(response.status,response.reason)
    data = response.read()
    jsondata = json.loads(data)
    print(jsondata)
    cookie = response.getheader("Set-Cookie")[:44]
    binary = jsondata["binary"]
    target = jsondata["target"]
    test = str(binascii.hexlify(base64.b64decode(jsondata["binary"])))
    target = str(pipeline.predict([test])[0])
    jsontarget = {"target":target}
    data = json.dumps(jsontarget)
    print(data)
    headers = {"Content-type": "application/json","Accept": "text/plain","Cookie": cookie}
    c.request("POST","/solve", data, headers)
    response = c.getresponse()
    print(response.status,response.reason)
    data = response.read()
    jsondata = json.loads(data)
    print(jsondata)
    #{'accuracy': 1.0, 'correct': 1, 'target': 'arm'}
    print(jsondata["target"])
    if(jsondata["accuracy"] == 1.0):
        print("correct guess")
        print({'target':target,'base64':binary})
        f= open("ML_Data.txt","a+")
        f.write(json.dumps({'target':target,'base64':binary}) + "\n")
        f.close()
    else:
        print("wrong guess")
    print("correct:")
    print(jsondata["correct"])
    return

def getChallenge():
    c = http.client.HTTPSConnection("mlb.praetorian.com")
    headers = {"Content-type": "application/json","Accept": "text/plain","Cookie": cookie}
    data = ""
    c.request("GET", "/challenge", data, headers)
    response = c.getresponse()
    print(response.status,response.reason)
    data = response.read()
    jsondata = json.loads(data)
    print(jsondata)
    binary = jsondata["binary"]
    target = jsondata["target"]
    test = str(binascii.hexlify(base64.b64decode(jsondata["binary"])))
    target = str(pipeline.predict([test])[0])
    jsontarget = {"target":target}
    data = json.dumps(jsontarget)
    print(data)
    headers = {"Content-type": "application/json","Accept": "text/plain","Cookie": cookie}
    c.request("POST","/solve", data, headers)
    response = c.getresponse()
    print(response.status,response.reason)
    data = response.read()
    jsondata = json.loads(data)
    print(jsondata)
    #{'accuracy': 1.0, 'correct': 1, 'target': 'arm'}
    if(jsondata["accuracy"] == 1.0):
        print("correct guess")
        print({'target':target,'base64':binary})
        f= open("ML_Data.txt","a+")
        f.write(json.dumps({'target':target,'base64':binary}) + "\n")
        f.close()
    else:
        print("wrong guess")
        initialize()
        return
    print("correct:")
    print(jsondata["correct"])
    if(jsondata["correct"] > 499):
        print(cookie)
        f= open("hash.txt","a+")
        f.write(data)
        f.close()
    print()
    return


initialize()
while True:
    getChallenge()
