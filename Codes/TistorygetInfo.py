import requests as rq
import json
from pprint import pprint

url = 'https://www.tistory.com/apis/blog/info'
access_code='7f64ff4fb10ba304855f119b754ab237_e32e5625a14d488097075f53d07c67db'

param = {'access_token' : access_code, 'output': 'json'}

response = rq.get(url, params= param)

jr = json.loads(response.text)

infos = jr['tistory']['item']['blogs'][0]

print('title: ' + infos['title'])
print('nickname : ' + infos['nickname'])
print('description: ' + infos['description'])
print('url : ' + infos['url'])