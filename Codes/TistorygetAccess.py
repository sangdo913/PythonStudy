import json
import requests as rq

url = 'https://www.tistory.com/oauth/authorize'
param = {'client_id': '915cef83af53385eaa94db9f10ada058', 'redirect_uri' : 'http://localhost:8080/Desktop/Git/Phthon/tistory/tistory.html', 'response_type' : 'token'}

response = rq.get(url, params= param)
print(response.text)