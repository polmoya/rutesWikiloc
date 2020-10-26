# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 15:36:35 2020

@author: moyap
"""
import datetime
import requests
from bs4 import BeautifulSoup
import random
import sys
#Variables globals:
#Agent lists per simular que s'accedeix a la url des d'un navegador normal
user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        #'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    ]

#Funció que ens escull un user_agent aleatòri
user_agent = random.choice(user_agent_list)
#headers que ens ajuden a simular que l'accés el fa una persona normal i evitem els anti web scraping.
headers = {"User-Agent":user_agent,
           "Accept-Language":"ca",
           "Accept-Encoding":"gzip, deflate", 
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
           "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1",
           "Referer": "http://www.google.com/"}

initDate:datetime;
elapsed:float;

def main():
    '''
    #Llegim els arguments
    activitat=sys.argv[1]
    pais=sys.argv[2]
    regio1=sys.argv[3]
    regio2=sys.argv[4]
    '''
    #Paràmetres per a testejar
    activitat='outdoor'
    pais='/argentina'
    regio1='/entre-rios'
    regio2=''
    
    
    initDate = datetime.datetime.now();
    fileLog = open('ProvesPol.log','a');
    fileLog.write(str(datetime.datetime.now()) + ' ======== Start The Web Scrapping =========\n');
    
    
    
    url_principal = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1+regio2

    print('Url principal: '+url_principal) #Test
    #fileLog.write('Url principal -> '+ url_principal + '\n');
    
    #page = requests.get(url_principal, headers=headers)
    #soup = BeautifulSoup(page.content, features="lxml")
    #print(soup.prettify())
    
    
    url_rutes_get = get_urls(activitat, pais, regio1, regio2)
    

    url_rutes_buscar = buscar_urls(url_principal)
    
    print(url_rutes_get)
    print(url_rutes_buscar)
    print('Url rutes get: '+str(len(url_rutes_get)))
    print('Url rutes buscar: '+str(len(url_rutes_buscar)))

    '''
    url_rutes = []
    url_rutes = buscar_urls_valorades(url_principal, url_rutes)
    
    for link in url_rutes:
        print('URL -> ' + link) 
        fileLog.write('URL -> ' + link + '\n');
        
    print('Total rutes -> ' + str(len(url_rutes)))
    '''
    
    elapsed = (datetime.datetime.now() - initDate).total_seconds();
    fileLog.write(str(datetime.datetime.now()) + ' ======== Elapsed Time: ' + str(elapsed) + '=========\n');
    fileLog.write(str(datetime.datetime.now()) + ' ======== End The Web Scrapping =========\n');
    fileLog.close()
    

#Funcio que agafa totes les regions per les quals es pot filtrar
def get_urls_filter(url_base, activitat):
    page = requests.get(url_base, headers=headers)
    soup = BeautifulSoup(page.content, features="lxml")
    ul = soup.find(id="filters").find('ul')
    urls_filter = []
    for link in ul.find_all('a'):
        #Substituim 'outdoor' per l'activitat per accedir a la ruta correcta
        url = str.replace(link.get('href'), 'outdoor', activitat)
        urls_filter.append(url)
        print(url)
    return urls_filter    
    

#Funció que accedeix als filtres i va avançant per aquest per tal d'aconseguir totes les urls de les rutes
def get_urls(activitat, pais, regio1, regio2):
     #Rutes regio2
    if (regio2 != ''):
        url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1+regio2
        #Modificar a buscar_url_valorades()
        return buscar_urls(url_base) 
    #Rutes regio1
    if (regio1 != ''):
        url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1
        urls_regio2 = get_urls_filter(url_base, activitat)
        url_rutes_regio1 = []
        for url in urls_regio2:
            #Modificar a buscar_url_valorades()
            url_rutes_regio1 = url_rutes_regio1 + buscar_urls(url)
        return url_rutes_regio1
    #Rutes pais
    url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais
    urls_filter_pais = get_urls_filter(url_base, activitat)
    url_rutes_pais = []
    for url_regio1 in urls_filter_pais:
        urls_regio2 = get_urls_filter(url_regio1, activitat)
        for url_regio2 in urls_regio2:
            #Modificar a buscar_url_valorades()
            url_rutes_pais = url_rutes_pais + buscar_urls(url_regio2)
    return url_rutes_pais    
 
#Funció que recorre totes les pàgines de la url_principal i retorna les url de les rutes trobades.    
def buscar_urls_valorades(url_principal):
    next = ''
    actual_page = '?s=trailrank'

    url_rutes_regio2 = []
    #Iterem disposem de pàgines.
    while next != None: 
        url_actual = url_principal + actual_page
        print(url_actual) #Test
        page = requests.get(url_actual, headers=headers)
        soup = BeautifulSoup(page.content, features="lxml")
        
        for row in soup.find(id="trails").find_all_next('div', 'row'):
            print(row.find('a', 'rating-container')) #Test
            if row.find('a', 'rating-container') != None:
                url_rutes_regio2.append(row.find('a', 'trail-title').get('href'))
        next = soup.find('a', 'next')
        if next != None:
            actual_page = next.get('href')
    return url_rutes_regio2
    
#Funció que recorre totes les pàgines de la url_principal i retorna les url de les rutes trobades.
def buscar_urls(url_principal):
    #Funció que recorre totes les pàgines de la url_principal i retorna les url de les rutes trobades.
    next = ''
    actual_page = ''
    url_rutes_regio2 = []
    while next != None: 
        url_actual = url_principal + actual_page
        print(url_actual) #Test
        page = requests.get(url_actual, headers=headers)
        soup = BeautifulSoup(page.content, features="lxml")
        for link in soup.find(id="trails").find_all('a', 'trail-title'):
            url_rutes_regio2.append(link.get('href'))    
        next = soup.find('a', 'next')
        if next != None:
            actual_page = next.get('href')
    return url_rutes_regio2


 

       
main()
 