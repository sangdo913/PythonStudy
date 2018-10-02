import os
from bs4 import BeautifulSoup
import requests as rq
import json


response = rq.get('https://nghttp2.org/httpbin/robots.txt')

print(response.text)

with open('I.txt', 'wb') as f:
    f.write(response.content)

'''
response = []
response.append(  rq.get('https://nghttp2.org/httpbin/image/jpeg'))
response.append(rq.get('https://nghttp2.org/httpbin/image/png'))

images = []
images.append(  response[0].content)
images.append(response[1].content)



filename = 'TestImage'
extends = ['jpg', 'png']


for i in range(0,2):
    name = filename + str(i) + '.' + extends[i]
    with open(name, 'wb') as f:
        f.write(images[i])
'''
'''
jr = response.json()

print(jr)
print('\n')

for v in jr['form']:
    if type(jr['form'][v]) == type([]):
        a = '' 
        for v2 in jr['form'][v]:
            a += v2 + ' '
        
        print(a)

    else :
        print(jr['form'][v])
        '''