import requests as rq
import json

url = 'https://api.flickr.com/services/rest'
param_basic = {'format' : 'json', 'api_key': 'a886763ddcb5a78a297f93bb29ab75c2'}

param = param_basic
param['text'] = '1억개의 별'
param['method'] = 'flickr.photos.search'
response = rq.get(url, params=param)
print(response.text)