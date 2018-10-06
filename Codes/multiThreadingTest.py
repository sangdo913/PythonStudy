import threading
import json
from time import time
import requests as rq

url = 'http://httpbin.org/get'
count = 0

cntlock = threading.Lock()

class GetURL(threading.Thread):
    def __init__(self, idx):
        super().__init__()
        global url
        self.url = url
        self.idx = idx
    
    def run(self):
        global count
        try : 
            self.response = rq.get(url)
            if self.response.status_code != 200:
                raise Exception

            cntlock.acquire()
            count+=1
            cntlock.release()

        except Exception as e:
            print(e)
            print('-------id : ' + str(self.idx), ' error!!!!---------------')

        global threadpool
        global lock
        
        lock.acquire()
        threadpool.remove(self.idx)
        lock.release()
        
lock = threading.Lock()

getIdx = [10, 20, 30, 40, 50]
get = 1000
tid = 0

filename = 'Log.txt'

with open(filename, 'w') as f:
    f.write('url = ' + url+'\n')
    f.write('get : ' + str(get) + '번')
    f.write('\n\n')

    f.write('멀티 쓰레딩\n\n')
    f.write('쓰레드 개수 \t|\t시간초\n')

for nums in getIdx:
    print('쓰레드 수 : ', nums, ' started!')
    threadpool = set()
    count = 0
    tid = 0

    st = time()
    check = 0
    while count < get:
        
        if count > check:
            check = count - count%100 + 100
            print('progress :' , str(count/get*100)[:6] ,'%')
        
        lock.acquire()
        if len(threadpool) < nums:
            th = GetURL(tid)
            th.start()
            threadpool.add(tid)
            tid +=1

        lock.release()


    while len(threadpool) > 0:
        continue

    ed = time()

    with open(filename, 'a') as f:
        f.write('\t' +  str(nums) + '\t|\t' + str(ed-st))
        f.write('\n')

    print('time : ', ed - st, '\n\n')