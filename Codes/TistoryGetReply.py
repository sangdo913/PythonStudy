import requests
import json
from pprint import pprint
import time

url =  'https://www.tistory.com/apis/post/list'
reply_url = 'https://www.tistory.com/apis/comment/list'

param = { 'access_token' : 'ff09fcd6654d39de28821ffe1e5035c3_71543e1bd62c46ae4c236ca54a63452e', 'blogName' : 'sangdo913','output' : 'json'}

reply_param = param
param['count'] = '30'

st = time.time()

with open('post_lists.txt', 'w') as f:
    pass

for i in range(1,10):
    param['page'] = str(i)
    response = requests.get(url, params=param)
    jr = json.loads(response.text)

    try:
        infos = jr['tistory']['item']['posts']


        for value in infos:
            if value['comments'] == '0':
                continue
            
            
            reply_param['postId'] = value['id']
            reply_response = requests.get(reply_url, params = reply_param)
            
            reply_json = json.loads(reply_response.text)

            replys = reply_json['tistory']['item']['comments']
            
            
            try : 
                for v in replys:
                    reply = ''
                    reply += '\tid : ' + v['name'] +' ' + v['date']+'\n'
                    a =  (v['comment'].split('\n'))
                    b = '\n\t\t'.join(a)
                    reply += '\t내용\n'+'\t\t' + b +'\n'


            except :
                print("댓글 에러")

            
            s = ''

            s += '제목 : ' + value['title'] + ' ' + value['date'] + '\n'
            s += 'id : ' + value['id'] + '\n'
            s += 'postUrl : ' + value['postUrl'] + '\n'
            s += '\n'

            with open('post_lists.txt', 'a') as f:
                pass
                f.write(s)
                f.write('댓글들\n')
                f.write(reply)
                f.write('\n\n')
    except :
        break

ed = time.time()

print(ed - st)