import bs4
import json
import requests
from pprint import pprint

url = 'https://dapi.kakao.com/v2/search/web'

param = {'query': '삼성'}

header = {'Authorization': 'KakaoAK 1d3e153340b43fe43f6e7c7d44cd8000'}

response = requests.get(url, params= param, headers=header)

jr = json.loads(response.text)

with open('Get.Txt', 'w') as f:
    pass

with open('Get.Txt', 'a') as f:
    for val in jr['documents']:
        f.write('제목 : ' +  val['title']+'\n')
        f.write('url : ' +  val['url']+'\n')
        f.write('내용 : ' + val['contents'] + '\n')
        f.write('\n')