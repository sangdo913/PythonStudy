import json
import requests as rq
import pprint

url = 'https://kapi.kakao.com'
comm = '/v2/api/talk/memo/default/send'
getinfo = '/v1/api/talk/profile'
scrap = '/v2/api/talk/memo/scrap/send'
sendmessagecomm = '/v2/api/talk/memo/send'
seefriend = '/v1/friends'
access = 'eG8ocpF70bmmxR2s1EXSBmbnUB0jFjGe0-zkfQo8BJ4AAAFmNe3Gfw'
agree = '/oauth/authorize?client_id=1d3e153340b43fe43f6e7c7d44cd8000&redirect_uri=http://localhost:8080/Desktop/Git/Phthon/&response_type=code&scope={required_scopes.join(',')}'

param = {'template_object' : {
  "object_type": "text",
  "text": "텍스트 영역입니다. 최대 200자 표시 가능합니다.",
  "link": {
    "web_url": "https://developers.kakao.com",
    "mobile_web_url": "https://developers.kakao.com"
  },
}}

scrap_param = {'request_url' : 'https://developers.kakao.com'}

response = rq.post(url+comm,params= param  ,headers = {'Authorization': 'Bearer ' +  access})

print(response)