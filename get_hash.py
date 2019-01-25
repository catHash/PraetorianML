#!/usr/bin/env python
import http.client
import json
import base64
import random

#{'hash': ''}

cookie = "session="
headers = {"Content-type": "application/json","Accept": "text/plain","Cookie": cookie}
email = ""
json_email = {"email":email}
data = json.dumps(json_email)
c = http.client.HTTPSConnection("mlb.praetorian.com")
c.request("GET", "/hash", data, headers)
response = c.getresponse()
print(response.status,response.reason)
data = response.read()
jsondata = json.loads(data)
print(jsondata)
