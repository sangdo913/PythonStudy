import bs4
import requests as rq
import json
import multiprocessing as mp
import threading
import time

from pprint import pprint

search = list()
check = set()

perpage = 300
imgpnum = 10
tnum = 0
imgnum = 0
processed = 0
ch = [0,0]


lock = threading.Lock()
imglock = threading.Lock()
thnum = threading.Semaphore(100)
manth = threading.Semaphore(20)
ulock = threading.Lock()
unhandle = []
mlock = threading.Lock()
mhandle = []
datas = []

param_basic = {'api_key' : 'a8867610ddcb5a78a297f93bb29ab75c2', 'format' : 'json'}
class IMGThread(threading.Thread):
    def __init__(self, idx, i):
        super().__init__()
        self.idx = idx 
        self.i = i

    def run(self):
        i = self.i
        url = 'http://farm' + str(i['farm']) + '.staticflickr.com/'+i['server'] +'/' +i['id'] + '_' + i['secret'] + '.jpg'
        
        global lock
        global processed
        global ulock
        global thnum
        global unhandle

        try:
            response = rq.get(url)

            imglock.acquire()
            datas.append(response.content)
            imglock.release()

            thnum.release()
            #print('tid({num}): image was processed'.format(num = self.idx))

        except Exception as e:
            print(e)
            print('--------picture error-------------')

            ulock.acquire()
            unhandle.append(i)
            ulock.release()

            thnum.release()

def getRank():
   url = 'https://www.naver.com/' 
   response = rq.get(url)
   soup = bs4.BeautifulSoup(response.text, 'html.parser')

   pkg_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
   global search

   for name in pkg_list:
      search.append(name.text) 

class searchThread(threading.Thread):
    def __init__(self, idx,name):
        super().__init__()
        self.idx = idx
        self.name = name
    
    def run(self):
        url = 'https://api.flickr.com/services/rest'
        param_basic = {'format' : 'json', 'api_key': 'a886763ddcb5a78a297f93bb29ab75c2'}
        
        param = param_basic
        param['text'] = self.name 
        param['method'] = 'flickr.photos.search'
        param['per_page'] = str(perpage)
        global ch

        try :
            response = rq.get(url, params= param)

        except Exception as e:
            print(e)
            print('----------here------------')
            mlock.acquire()
            mhandle.append(name)
            mlock.release()

            manth.release()
            
            
            return
            
        s = response.text[14:len(response.text)-1]
        jr = json.loads(s)

        infos = jr['photos']['photo']

        global lock
        global thnum
        global tnum
        
        for val in infos:
           thnum.acquire()
           th = IMGThread(tnum, val)
           th.start()

        lock.acquire()
        ch[1]+= len(infos)
        ch[0]+=1
        lock.release()
        print('tid({id}): {name}search was processed'.format(id=self.idx, name= self.name))
        manth.release()
        
if __name__ == '__main__':
    getRank()

    import time

    st = time.time()

    ch[0] = 0

    for name in search:
        manth.acquire()
        th = searchThread(tnum, name)
        th.start()

    inum = 0
    while ch[1] != processed or ch[0] != len(search):
        print('not end...remain : {remain}, {ch1}, {ch2}'.format(remain= processed, ch1 = ch[1], ch2= ch[0]))
        while len(mhandle):
            print('-------lencheck....')
            manth.acquire()
            mlock.acquire()
            th = searchThread(tnum, mhandle.pop())
            mlock.release()
            
            th.start()

        while len(unhandle):
            print('----------unhandle check')
            thnum.acquire()
            ulock.acquire()
            th = IMGThread(tnum, unhandle.pop())
            ulock.release()

            th.start()
        
        imglock.acquire()
        l = len(datas)
        imglock.release()
        
        while l:
            filename = 'img/img{id}.jpg'.format(id=inum)
            inum+=1
            with open(filename, 'wb') as f:
                imglock.acquire()
                f.write(datas.pop(0))
                imglock.release()
                processed+=1

            l-=1

        time.sleep(5)




    ed = time.time()
    print('processed time :', ed-st)
    print('processed :', processed)
    print('all num:', ch[1])