import requests
import time
import asyncio
import json
from bs4 import BeautifulSoup
async def restGet(num):
    
    url = 'http://httpbin.org/get'
    res = await loop.run_in_executor(None, requests.get, url)
    #print(num, res.status_code)
futures = [restGet(i) for i in range(1000)]
# 시작 시간
start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
loop.close
# 종료 시간
print("--- %s seconds ---" %(time.time() - start_time))