#!/usr/bin/env python
import http.client
import json
import base64
import random

c = http.client.HTTPSConnection("mlb.praetorian.com")
c.request("GET", "/challenge")
response = c.getresponse()
print(response.status,response.reason)
data = response.read()
jsondata = json.loads(data)
print(jsondata)
cookie = response.getheader("Set-Cookie")[:44]
print(cookie)
print(jsondata["binary"])
binary = jsondata["binary"]
print(jsondata["target"])
target = jsondata["target"]
print(base64.b64decode(jsondata["binary"]))
#print(random.choice(target))

target = random.choice(target)
jsontarget = {"target":target}
data = json.dumps(jsontarget)
print(data)
headers = {"Content-type": "application/json","Accept": "text/plain","Cookie": cookie}
c.request("POST","/solve", data, headers)
print(headers)

response = c.getresponse()
print(response.status,response.reason)
data = response.read()
jsondata = json.loads(data)
print(jsondata)
#{'accuracy': 1.0, 'correct': 1, 'target': 'arm'}
print(jsondata["accuracy"])
if(jsondata["accuracy"] == 1.0):
    print("correct guess")
    print({'target':target,'base64':binary})
    f= open("ML_Data.txt","a+")
    f.write(json.dumps({'target':target,'base64':binary}) + "\n")
    f.close()
else:
    print("wrong guess")
print(jsondata["correct"])
print(jsondata["target"])
