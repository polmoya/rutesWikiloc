# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 15:02:39 2020

@author: XMB1483
"""
import requests
from bs4 import BeautifulSoup

"""
Description:
    Realitza una petició GET a una pàgina , valida si la connexió s'ha 
    realitzat correctament i retorna el text de la mateixa
    Si es produeix quelcom error en aquesta tasca llençarà una exception
Parameters:
    url(str): url de la pàgina desitjada
Return:
    Un string que conté el txt de la p+agina visitada
"""
def download_page(url:str) -> str:
    myResponse:requests.Response=None;
    #header ={'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '};
    myHeader={'User-Agent':'Mozilla/5.0 (SMART-TV; X11; Linux armv71) AppleWebKit/537.42 (KHTML, like Gecko) Chromium/25.0.1349.2 Chrome/25.0.1349.2 Safari/537.42'};
    try:
        myResponse = requests.get(url,headers = myHeader);
        if myResponse.status_code == 200:
            return myResponse.text;
        else:
            raise Exception('Network Error:' + str(myResponse.status_code) + ' with the URL: ' + url)
    except Exception as e:
        raise e;

"""
Description:
    Si passem 2 paràmetres:
        Busca entre tots els tags fills de tipus <a> d'un donat quin té com a text
        el passat en el paràmetre [paramTxt]
    Si passem 1 paràmetre:
        Obté tots els href dels tags buscats.
Parameters:
    Si passem 2 paràmetres:
        1- paramTag(bs4.element.Tag): es farà un recorregut per tots els fills d'aquest tag
        2- paramTxt(str): text que ha de tenir el tag <a> buscat.
    Si passem 1 paràmetre:
        1- paramTag(bs4.element.Tag): es farà un recorregut per tots els fills d'aquest tag
Return:
    Un obj. de tipus [list] amb les url's corresponents,
    en cas contrari es llençarà una exception.
"""        
def get_Links(*paramArgs):
    links:list;
    qtyTags:int = 0;
    linksHref:list = list();
    
    try:
        if len(paramArgs) == 2:
            links = paramArgs[0].find_all('a');
            if (len(links) == 0):
                raise Exception('Soup Error: ' + 'There arent links for this tag...');
        
            for link in links:
                if (link.text.upper().find(paramArgs[1].upper()) > 0):
                    linksHref.append(link.get('href'));
                    break;
                else:
                    qtyTags = qtyTags + 1;
        
            if (qtyTags == len(links)):
                raise Exception('Soup Error: ' + 'The text ' + paramArgs[1] + ' doesnt exist...');
        else:
            links = paramArgs[0].find_all('a');
            if (len(links) == 0):
                raise Exception('Soup Error: ' + 'There arent links for this tag...');
        
            for link in links:
                linksHref.append(link.get('href'));
                
        return(linksHref);
    except Exception as e:
        raise e;
    finally:
        links.clear();
        links = None;