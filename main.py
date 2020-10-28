# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 20:40:16 2020

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
fileLog = fileLog = open('main.log','a');


def main():
   #S'inicialitza el log
    try:
        initDate = datetime.datetime.now()
        fileLog.write(str(datetime.datetime.now()) + ' ======== Start The Web Scrapping =========\n')
    except Exception as e:
        raise e;  
  
    '''
    #Llegim els arguments
    activitat=sys.argv[1]
    pais=sys.argv[2]
    regio1=sys.argv[3]
    regio2=sys.argv[4]
    '''
    #ToDo: Adaptar! Paràmetres per a testejar
    activitat='sender-accessible'
    pais=''
    regio1=''
    regio2=''
    
    #Es normalitzen els arguments afegint la / per a accedir a la url
    if (pais != ''):
        pais = '/'+pais
    if (regio1 != ''):
        regio1 = '/'+regio1   
    if (regio2 != ''):
        regio2 = '/'+regio2  
   
    url_rutes_get = get_urls(activitat, pais, regio1, regio2)
    
    try:
        fileLog.write('urls_rutes_valorades -> ' + str(url_rutes_get) +'\n')
        fileLog.write('Length urls_rutes_valorades -> ' + str(len(url_rutes_get))+'\n')
    except Exception as e:
        raise e;
        
    try:
        elapsed = (datetime.datetime.now() - initDate).total_seconds();
        fileLog.write(str(datetime.datetime.now()) + ' ======== Elapsed Time: ' + str(elapsed) + '=========\n');
        fileLog.write(str(datetime.datetime.now()) + ' ======== End The Web Scrapping =========\n');
        fileLog.close()
    except Exception as e:
        raise e;

#Mètode que retorna les urls amb id="filters" que pertanyen a una regió.
def get_urls_filter(url_base, activitat):
    try:
        page = requests.get(url_base, headers=headers)
        soup = BeautifulSoup(page.content, features="lxml")
        if (soup.find(id="filters") == None):
            #ToDo: Preguntar Xavier si hauria de fer d'escriure al log o no cal
            fileLog.write('Soup Error: There arent filter links for '+url_base+'\n');
            raise Exception('Soup Error: There arent filter links for ' + url_base);
        ul = soup.find(id="filters").find('ul')
        urls_filter = []
        for link in ul.find_all('a'):
            #Substituim 'outdoor' per l'activitat per accedir a la ruta correcta
            url = str.replace(link.get('href'), 'outdoor', activitat)
            urls_filter.append(url)
            fileLog.write('FILTER ----> '+url+'\n')
            #print(url)
    except Exception as e:
        raise e;
    else:
        return urls_filter    
    

#Mètode que retorna totes les urls de les rutes filtrades per activitat, país, regio1 i regio2.
def get_urls(activitat, pais, regio1, regio2):
     #Rutes regio2
    if (regio2 != ''):
        url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1+regio2
        #Modificar a buscar_url_valorades()
        return buscar_urls_valorades(url_base) 
    #Rutes regio1
    if (regio1 != ''):
        url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1
        urls_regio2 = get_urls_filter(url_base, activitat)
        url_rutes_regio1 = []
        for url in urls_regio2:
            #Modificar a buscar_url_valorades()
            url_rutes_regio1 = url_rutes_regio1 + buscar_urls_valorades(url)
        return url_rutes_regio1
    #Rutes pais
    if (pais != ''):
        url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais
        urls_filter_pais = get_urls_filter(url_base, activitat)
        url_rutes_pais = []
        for url_regio1 in urls_filter_pais:
            urls_regio2 = get_urls_filter(url_regio1, activitat)
            for url_regio2 in urls_regio2:
                url_rutes_pais = url_rutes_pais + buscar_urls_valorades(url_regio2)
        return url_rutes_pais  
    return buscar_urls_valorades('https://ca.wikiloc.com/rutes/'+activitat)  
 
#Mètode que recorre totes les pàgines de la url_principal i retorna les url de les rutes valorades.    
def buscar_urls_valorades(url_principal):
    next = ''
    actual_page = ''
    url_rutes_regio2 = []
    #Iterem disposem de pàgines.
    while next != None: 
        url_actual = url_principal + actual_page
        try:
            fileLog.write('PAGE -> '+url_actual+'\n')
            page = requests.get(url_actual, headers=headers)
            soup = BeautifulSoup(page.content, features="lxml")
            if (soup.find(id="trails") == None):
                #ToDo: Preguntar Xavier si hauria de fer d'escriure al log o no cal
                fileLog.write('Soup Error: There arent trail links for '+url_actual+'\n');
                raise Exception('Soup Error: There arent trail links for ' + url_actual); 
        except Exception as e:
            raise e;
        else:
            for row in soup.find(id="trails").find_all_next('div', 'row'):
                #print(row.find('a', 'rating-container')) #Test
                if row.find('a', 'rating-container') != None:
                    url_rutes_regio2.append(row.find('a', 'trail-title').get('href'))        
            next = soup.find('a', 'next')
            if next != None:
                actual_page = next.get('href')
            
    fileLog.write('Num rutes valorades a '+url_principal+' -> '+str(len(url_rutes_regio2))+'\n')
    return url_rutes_regio2
    

     
main()
