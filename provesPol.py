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

   
    
    initDate = datetime.datetime.now();
    fileLog = open('ProvesPol.log','a');
    fileLog.write(str(datetime.datetime.now()) + ' ======== Start The Web Scrapping =========\n');
    
    
   

    activitat='btt'
    pais='/andorra'
    regio1='/canillo'
    regio2=''
    
    
    url_principal = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1+regio2

    print('Url principal: '+url_principal) #Test
    fileLog.write('Url principal -> '+ url_principal + '\n');
    
    #page = requests.get(url_principal, headers=headers)
    #soup = BeautifulSoup(page.content, features="lxml")
    #print(soup.prettify())


    url_rutes = []
    url_rutes = buscar_urls_valorades(url_principal, url_rutes)
    
    for link in url_rutes:
        print('URL -> ' + link) 
        fileLog.write('URL -> ' + link + '\n');
        
    print('Total rutes -> ' + str(len(url_rutes)))
    
    elapsed = (datetime.datetime.now() - initDate).total_seconds();
    fileLog.write(str(datetime.datetime.now()) + ' ======== Elapsed Time: ' + str(elapsed) + '=========\n');
    fileLog.write(str(datetime.datetime.now()) + ' ======== End The Web Scrapping =========\n');
    fileLog.close()

    
   
    url_rutes_get = []
    url_rutes_get = get_urls(activitat, pais, regio1, regio2, url_rutes_get)
    
    url_rutes_buscar = []
    url_rutes_buscar = buscar_urls(url_principal, url_rutes_buscar)
    
    print(url_rutes_get)
    print(url_rutes_buscar)
    print('Url rutes get: '+str(len(url_rutes_get)))
    print('Url rutes buscar: '+str(len(url_rutes_buscar)))


def get_urls(activitat, pais, regio1, regio2, url_rutes):
    #Funció que accedeix als filtres i va avançant per aquest per tal d'aconseguir totes les urls de les rutes
    url_base = 'https://ca.wikiloc.com/rutes/'+activitat+'/'+pais+regio1
    page1 = requests.get(url_base, headers=headers)
    soup1 = BeautifulSoup(page1.content, features="lxml")
    ul = soup1.find(id="filters").find('ul')
    for link in ul.find_all('a'):
        #Substituim 'outdoor' per l'activitat per accedir a la ruta correcta
        url = str.replace(link.get('href'), 'outdoor', activitat)
        print(url)
        buscar_urls(url, url_rutes) 
    return url_rutes    
 
    
def buscar_urls_valorades(url_principal, url_rutes):
    #Funció que recorre totes les pàgines de la url_principal i retorna les url de les rutes trobades.
    next = ''
    actual_page = '?s=trailrank'
    #Iterem disposem de pàgines.
    while next != None: 
        url_actual = url_principal + actual_page
        #print(url_actual) #Test
        page = requests.get(url_actual, headers=headers)
        soup = BeautifulSoup(page.content, features="lxml")
        
        for row in soup.find(id="trails").find_all_next('div', 'row'):
            #print(row.find('a', 'rating-container')) #Test
            if row.find('a', 'rating-container') != None:
                url_rutes.append(row.find('a', 'trail-title').get('href'))
        next = soup.find('a', 'next')
        if next != None:
            actual_page = next.get('href')
            
    return(url_rutes)
    

def buscar_urls(url_principal, url_rutes):
    #Funció que recorre totes les pàgines de la url_principal i retorna les url de les rutes trobades.
    next = ''
    actual_page = ''
    while next != None: 
        url_actual = url_principal + actual_page
        #print(url_actual) #Test
        page = requests.get(url_actual, headers=headers)
        soup = BeautifulSoup(page.content, features="lxml")
        for link in soup.find(id="trails").find_all('a', 'trail-title'):
            url_rutes.append(link.get('href'))    
        next = soup.find('a', 'next')
        if next != None:
            actual_page = next.get('href')
    return(url_rutes)



 

       
main()
 