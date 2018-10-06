import requests as rq
import json
import pprint

code = '6f01f8e44d86c781661a1dada170eec8c5abdb6861f042db10e0d5b5ff7f6609ea9b5c5d'
client_id = '915cef83af53385eaa94db9f10ada058'
secret_id = '915cef83af53385eaa94db9f10ada0587ef542da8c94c94ed5b620381c78a5a780754ad9'
redirect_id = 'http://localhost:8080/Desktop/Git/Phthon/tistory/tistory.html'
url = 'https://www.tistory.com/oauth/access_token' 

param = {'client_id': client_id, 'client_secret' : secret_id, 'redirect_uri': redirect_id, 'code' : code,'grant_type' : 'authorization_code'}

check_url= redirect_id
check_param = {'code': code}

check_response = rq.get(check_url, params= check_param)

response = rq.get(url, params=param)

code = response.text
code = code[len('access_token='):]

