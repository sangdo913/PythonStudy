import json
import bs4
import requests

url = 'https://kapi.kakao.com/v1/translation/translate'

header = {'Authorization' : 'KakaoAK 1d3e153340b43fe43f6e7c7d44cd8000'}

param = {'query' : '동해물과 백두산이 마르고 닳도록 하느님이 보우사하사 우리나라 만세.', 'src_lang' : 'kr', 'target_lang':'en'}

response = requests.get(url, params= param, headers= header)

jr = json.loads(response.text)

print(jr['translated_text'][0][0])