# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 15:36:35 2020

@author: moyap
"""

import requests
from bs4 import BeautifulSoup
import random
import sys

'''
activitat=sys.argv[1]
pais=sys.argv[2]
regio1=sys.argv[3]
regio2=sys.argv[4]
'''
#Paràmetres prova
activitat='outdoor'
pais='andorra'
regio1='canillo'
regio2='el-tarter'


user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    #'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
]

user_agent = random.choice(user_agent_list)
headers = {"User-Agent":user_agent,
           "Accept-Language":"ca",
           "Accept-Encoding":"gzip, deflate", 
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
           "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1",
           "Referer": "http://www.google.com/"}

url_principal = 'https://ca.wikiloc.com/rutes/'+activitat+'/'+pais+'/'+regio1+'/'+regio2
print('Url principal: '+url_principal)

page = requests.get(url_principal, headers=headers)
soup = BeautifulSoup(page.content, features="lxml")
#print(soup.prettify())


def buscar_urls(url_principal):
    #Funció que recorre totes les pàgines de la url_principal i retorna les url de les rutes trobades.
    url_rutes = []
    next = ''
    actual_page = ''
    while next != None: 
        url_actual = url_principal + actual_page
        print(url_actual)
        page = requests.get(url_actual, headers=headers)
        soup = BeautifulSoup(page.content, features="lxml")
        for link in soup.find(id="trails").find_all('a', 'trail-title'):
            url_rutes.append(link.get('href'))    
        next = soup.find('a', 'next')
        if next != None:
            actual_page = next.get('href')
    return(url_rutes)
        
url_rutes = buscar_urls(url_principal)
print(url_rutes)
print(len(url_rutes))
 