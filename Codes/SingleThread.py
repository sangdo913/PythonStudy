import json
import requests as rq

url = 'http://httpbin.org/get'

from time import time

st = time()

cnt = 0
MAX = 100

while cnt < MAX:
    try:   
        response = rq.get(url)
        print(cnt)
        cnt+=1
    except:
        continue
    
ed = time()

print(st - ed)