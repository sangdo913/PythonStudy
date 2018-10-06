import json
import requests as rq
import pprint 

url = 'https://www.tistory.com/apis/comment/write'
rcheck_url = 'https://www.tistory.com/apis/comment/newest'
del_url = 'https://www.tistory.com/apis/comment/delete'

access_token = '51f4bfb63f70384cc1a3500e593ec848_4a17b4836679ac19c61d995500125310'
blogName = 'sangdo913'

param_basic = {'access_token' : access_token, 'blogName' : blogName, 'output' : 'json'}

param = {'access_token' : '51f4bfb63f70384cc1a3500e593ec848_4a17b4836679ac19c61d995500125310',
            'blogName' : 'sangdo913', 'postId' : '150' }

content = 'Tistory API Testing...'

del_param = dict()

param['content'] = content
param['output'] = 'json'

param = param_basic
param['count'] = '1'
check_res = rq.get(rcheck_url, params = param)
jr = json.loads(check_res.text)

info = (jr['tistory']['item']['comments'][0]['postId'], jr['tistory']['item']['comments'][0]['id'])

param = param_basic
param['postId'] = info[0]
param['commentId'] = info[1]

response = rq.post(del_url, params = param)

jr = json.loads(response.text)

pprint.pprint(jr)