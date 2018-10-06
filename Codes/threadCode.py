import os
from bs4 import BeautifulSoup
import requests as rq
import json
import threading
import time

count = 0

filename = 'TestImage'
extends = ['jpg', 'png']

class myThread(threading.Thread):
    def __init__(self, url , tid):
        super().__init__()
        self.url = url
        self.tid = tid
        global extends
        self.extends = extends[tid]
        self.response = rq.get(self.url)

    def run(self):
        global count
        global filename

        image = self.response.content
        
        while count < 100:
            lock.acquire()
            count+=1
            nc = count
            lock.release()

            name = filename + ' ' + str(nc) + '.' + self.extends

            with open(name, 'wb') as f:
                f.write(image)
            
            print(name + ' generated' , ' ' , self.tid)

lock = threading.Lock()

threads = []

response = []
response.append(  rq.get('https://nghttp2.org/httpbin/image/jpeg'))
response.append(rq.get('https://nghttp2.org/httpbin/image/png'))

url= ['https://nghttp2.org/httpbin/image/jpeg','https://nghttp2.org/httpbin/image/png']
images = []
images.append(  response[0].content)
images.append(response[1].content)


for i in range(0,2):
    th = myThread(url[i], i)
    threads.append(th)

time.sleep(2)

for th in threads:
    th.start()