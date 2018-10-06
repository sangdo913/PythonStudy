import multiprocessing as mp
import json
import requests
import pprint
from time import *
from pprint import pprint
import bs4

perpage = 500
pnum = 50

search = set()

def getRank():
   url = 'https://www.naver.com/' 
   response = requests.get(url)
   soup = bs4.BeautifulSoup(response.text, 'html.parser')

   pkg_list = soup.select('.PM_CL_realtimeKeyword_rolling span[class*=ah_k]')
   global search

   for name in pkg_list:
      search.add(name.text) 

def imgprocess(name, q,r,semaphore):
    try:
        i = q.get()
        
        url = 'http://farm' + str(i['farm']) + '.staticflickr.com/'+i['server'] +'/' +i['id'] + '_' + i['secret'] + '.jpg'


        response = requests.get(url)
        #filename = 'img/{}_{}image.jpg'.format(name[0],name[1])

        with open('img/log.txt', 'a') as f:
            f.write('{}_{} processed\n'.format (name[0],name[1]))

        #with open(filename, 'wb') as f:
        #    f.write(response.content)

        r.put((1,name[1]))
        semaphore.release()

    except Exception as e:
        semaphore.release()
        print(e)
        print(name, '--------- image get error')
        r.put((-1,i))
        return

def searchprocess(idx, q, r,semaphore):
    try:
        url = 'https://api.flickr.com/services/rest'
        param_basic = {'format' : 'json', 'api_key': 'a886763ddcb5a78a297f93bb29ab75c2'}
        
        param = param_basic
        name = q.get()
        param['text'] = name 
        param['method'] = 'flickr.photos.search'
        param['per_page'] = str(perpage)

        response = requests.get(url, params=param)


        s = response.text[14:len(response.text)-1]
        jr = json.loads(s)

        infos = jr['photos']['photo']

        oq = mp.Queue()
        iq = mp.Queue()
        global pnum
        cpid = 0
        

        procs = set()

        for val in infos:
            iq.put(val)
            #procs.add(cpid)
            semaphore.acquire()
            proc = mp.Process(target= imgprocess, args=((idx,cpid),iq,oq,semaphore))
            procs.add(cpid)
            proc.start()
            cpid+=1

        dst = len(infos)
        cnt = 0

        while len(procs):
            res = oq.get()

            if res[0] == 1:
                cnt+=1
                procs.remove(res[1])
            else:
                print(idx, 'put again')
                pprint(res[1])
                iq.put(res[1])
                procs.add(cpid)
                semaphore.acquire()
                proc = mp.Process(target= imgprocess, args=((idx,cpid),iq,oq,semaphore))
                proc.start()
                cpid+=1
        '''

        dst = len(infos)
        cnt = 0
        for proc in procs:
            proc.join()
            while not oq.empty():
                res = oq.get()
                if res[0]!=1:
                    iq.put(res[1])
                    semaphore.acquire()
                    proc = mp.Process(target=imgprocess,args=((idx,cpid),iq,oq,semaphore))

                    procs.append(proc) 
                    proc.start()
                    cpid+=1
                else:
                    cnt+=1

        '''

        r.put((1,name))

        try: 
            print(idx, ':', str(cnt/dst *100)[:6], dst)
        except ZeroDivisionError:
            semaphore.release()
            print(idx, 'dst : zero')
            return
        
        semaphore.release()

    except Exception as e:
        print(e)
        print('------------response error')
        r.put((-1, name))
        semaphore.release()


if __name__ == '__main__':
    getRank()
    st = time()

    iq = mp.Queue()
    oq = mp.Queue()

    mpnum = mp.Semaphore(pnum)

    keyword = search
    pid = 0

    f = open('img/log.txt', 'w')
    f.close()

    keyword = search 

    print(keyword)
    for key in keyword:
        iq.put(key)

    procs = []
    l = len(keyword)

    for i in range(len(keyword)):
        mpnum.acquire()
        proc = mp.Process(target= searchprocess, args=(pid, iq,oq,mpnum,))
        procs.append(proc)

        proc.start()
        pid+=1
        

    cnt = 0
    '''
    for proc in procs:
        proc.join()
        while not oq.empty():
            res = oq.get()
            if res[0] == 1:
                cnt+=1
            else:
                print('root error checking')
                iq.put(res[1])
                mpnum.acquire()
                proc = mp.Process(target = searchprocess, args=(pid,iq,oq,mpnum,))
                procs.append(proc)
                pid+=1
    '''
    while len(keyword):
        r = oq.get()
        if r[0] == 1:
            keyword.remove(r[1])
            #print(r[1], 'completed')
            cnt+=1
        else:
            iq.put(r[1]) 
            mpnum.acquire()
            proc = mp.Process(target = searchprocess, args = (pid, iq,oq,mpnum,))
            pid+=1
    

    
    ed = time()
    print(l , cnt)

    print(ed-st)