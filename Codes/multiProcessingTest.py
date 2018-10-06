import multiprocessing as mp
import requests as rq
import json
import time

cntlock = mp.Lock()
filename = 'process_log'

def multi(idx, q, res):
    while True:
        url = q.get()
        #print('id : {id} something doing...'.format(id = idx))
        try:
            response = rq.get(url)
            with open(filename, 'a') as f:
                f.write(response.text + '\n\n')
            res.put((1,url))
        #    print("id : {id} task complete!".format(id=idx))
    
        except Exception as err:
            print(err)
            res.put((1,'no'))

get = 1000

if __name__ == '__main__':
    with open(filename, 'w') as f:
        pass

    st = time.time()
    q = mp.Queue()
    res = mp.Queue()
    url = 'http://httpbin.org/get'

    for i in range(200):
        proc = mp.Process(target= multi, args=(i,q,res))
        proc.daemon = True
        proc.start()

    cnt = 0
    re = 0
    while cnt < get:
        q.put(url)
        ech = cnt
        while ech < get:
            q.put(url)
            ech+=1
        
        while cnt < get:
            r = res.get() 
            if r[1] == 'no':
                re+=1
            cnt+=1

        get+=re
        re = 0
            

    ed = time.time()
    print(ed - st)