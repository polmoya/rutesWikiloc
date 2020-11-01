# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 08:31:52 2020

@author: Xavier & Pol
"""

from bs4 import BeautifulSoup
import ClassRobotParser
from urllib import parse
import constants
import requests
import random


class Scrapper(object):
    
    #Getter de l' atribut [soup]        
    @property
    def soup (self):
        return (self.__soup);
    
    #Setter de l' atribut [soup]
    @soup.setter
    def soup (self, paramNewValue):
        self.__soup = paramNewValue;

    #Deleter de l' atribut [soup]        
    @soup.deleter
    def soup (self):
        self.__soup = None;
    
    
    #Getter de l'atribut [data]
    @property
    def data (self):
        return (self.__data);
    
    #Setter de l'atribut [data]
    @data.setter
    def data (self, paramNewValue):
        self.__data = paramNewValue;
      
    #Deleter de l'atribut [data]
    @data.deleter
    def data (self):
        self.__data.clear();
    
    def __init__(self):
        self.__soup:BeautifulSoup = None;
        #Dictionary on guardarem totes les dades obtingudes de la url
        #seleccionada mitjançant Web Scrapping
        self.__data:dict = None;
        #Instancia de l'obj. [RobotParser]
        self.myRobotParser = ClassRobotParser.RobotParser(parse.urljoin(constants.MAIN_URL,constants.ROBOTS_FILE));
        #Creem un obj. de tipus [Protego]
        self.myRobotParser.create();

    """
    Desc:
        Realitza una petició GET a una pàgina , valida si la connexió s'ha 
        realitzat correctament i retorna el text de la mateixa
        Si es produeix quelcom error en aquesta tasca llençarà una exception
    Params:
        url(str): url de la pàgina desitjada
    Return:
        Un string que conté el txt de la p+agina visitada
    """
    def __download_page(self,url:str) -> str:
        myResponse:requests.Response=None;        
        user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Mozilla/5.0 (SMART-TV; X11; Linux armv71) AppleWebKit/537.42 (KHTML, like Gecko) Chromium/25.0.1349.2 Chrome/25.0.1349.2 Safari/537.42',
            #'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        ]
        try:
            #Funció que ens escull un user_agent aleatòri
            user_agent = random.choice(user_agent_list)
            #headers que ens ajuden a simular que l'accés el fa una persona normal i evitem els anti web scraping.
            myHeader = {"User-Agent":user_agent,
               #"Accept-Language":"ca",
               "Accept-Encoding":"gzip, deflate", 
               "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
               "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1",
               "Referer": "http://www.google.com/"}
           
            
            myResponse = requests.get(url,headers = myHeader)
            if myResponse.status_code == 200:
                return myResponse.text
            else:
                raise Exception('Network Status Code: ' + str(myResponse.status_code) + ' with the URL: ' + url)
        except Exception as e:
            raise Exception("Method download_page(): Error: {0}".format(e))
     
    
    def __isAllowed(self, url, fileLog) -> bool:
        allowUrl = self.myRobotParser.is_allowed(url)
        if (allowUrl == False):
            fileLog.write('DENIED URL: '+url+'\n')
        fileLog.write('ALLOWED URL: '+url+'\n')
        fileLog.flush()
        return allowUrl
          
    """
    Desc:
        Realitza tota la feina de .
    Params:
        activitat: activitat introduïda per l'usuari
        pais: pais introduït per l'ususuari
        regio1: regio1 introduït per l'ususuari
        regio2: regio2 introduït per l'ususuari
        fileLog: fitxer log
    Return: Vector de diccionnaris amb totes les dades scrapejades.
    """        
    def scrape(self, activitat:str, pais:str, regio1:str, regio2:str, fileLog):
        try:
            url_rutes = self.get_urls(activitat, pais, regio1, regio2, fileLog)
            data = dict()
            for idx, ruta in enumerate(url_rutes):
                #print(ruta)
                #Validem si l' Url està permessa dins del site o no
                if self.__isAllowed(ruta, fileLog):
                    self.start_ruta(ruta)
                    try:
                        self.getTypeTrack();
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n')
                    try:
                        self.getTrailRank()
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n') 
                    try:
                        self.getUserRank();
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n')  
                    try:   
                        self.getDataTrack();
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n')   
                    try:
                        self.getDateCreation();
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n')
                    try:
                        self.getVotes();
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n')
                    try:
                        self.getCards();
                    except Exception as e:
                        fileLog.write('Warning: '+str(e)+'\n')
                    data["url" + str(idx)] = self.data
                print('.',end='')
                fileLog.flush()
        except Exception as e:
            raise Exception("Method scrape(): Error: {0}".format(e))
        finally:        
            self.stop()
        return data
        
    """
    Desc:
        Recorre totes les pàgines de les rutes filtrades per activitat, país, 
        regio1 i regio2.
    Params:
        activitat: activitat introduïda per l'usuari
        pais: pais introduït per l'ususuari
        regio1: regio1 introduït per l'ususuari
        regio2: regio2 introduït per l'ususuari
        fileLog: fitxer log
    Return: Vector que conté les adreces url.
    """
    def get_urls(self, activitat:str, pais:str, regio1:str, regio2:str, fileLog):
         #Rutes regio2
        if (regio2 != '-1'):
            url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1+regio2
            #Modificar a buscar_url_valorades()
            return self.__buscar_urls_valorades(url_base, fileLog) 
        #Rutes regio1
        if (regio1 != '-1'):
            url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais+regio1
            urls_regio2 = self.__get_urls_filter(url_base, activitat, fileLog)
            url_rutes_regio1 = []
            for url in urls_regio2:
                #Modificar a buscar_url_valorades()
                url_rutes_regio1 = url_rutes_regio1 + self.__buscar_urls_valorades(url, fileLog)
            return url_rutes_regio1
        #Rutes pais
        if (pais != '-1'):
            url_base = 'https://ca.wikiloc.com/rutes/'+activitat+pais
            urls_filter_pais = self.__get_urls_filter(url_base, activitat, fileLog)
            url_rutes_pais = []
            for url_regio1 in urls_filter_pais:
                urls_regio2 = self.__get_urls_filter(url_regio1, activitat, fileLog)
                for url_regio2 in urls_regio2:
                    url_rutes_pais = url_rutes_pais + self.__buscar_urls_valorades(url_regio2, fileLog)
            return url_rutes_pais  
        return self.__buscar_urls_valorades('https://ca.wikiloc.com/rutes/'+activitat) 
    
    """
    Desc:
        Mètode que recorre les urls amb id="filters" que pertanyen a url_base.
    Params:
        url_base: adreça url de la pàgina a tractar
        activitat: activitat introduïda per l'usuari
        fileLog: fitxer log.
    Return: 
        Vector amb les adreces url trobades.
    """
    def __get_urls_filter(self, url_base, activitat, fileLog):
        urls_filter = []
        if self.__isAllowed(url_base, fileLog):
            try:
                #Descarreguem la pàgina url_actual
                htmlDom = self.__download_page(url_base);
                soup = BeautifulSoup(htmlDom,'html.parser');
                if (soup.find(id="filters") == None):
                    raise Exception('Soup Error: There arent filter links for ' + url_base);
                ul = soup.find(id="filters").find('ul')
                #Recorrem totes les regions
                for link in ul.find_all('a'):
                    #Substituim 'outdoor' per l'activitat per accedir a la ruta correcta
                    url = str.replace(link.get('href'), 'outdoor', activitat)
                    urls_filter.append(url)
                    fileLog.write('FILTER ----> '+url+'\n')
            except Exception as e:
                fileLog.write(str(e)+'\n')
            else:
                return urls_filter
        fileLog.flush()
        return urls_filter
    
    """
    Desc:
        Es recorre totes les pàgines de l'adreça "url_principal" i es retorna
        totes les adreces urls de les rutes valorades que s'hi troben.
    Params:
        url_principal: adreça url de la pàgina a tractar
        fileLog: fitxer log.
    Return:
        
    """
    def __buscar_urls_valorades(self, url_principal, fileLog):
        next = ''
        actual_page = ''
        url_rutes_regio2 = []
        #Iterem mentre disposem de pàgines.
        while next != None: 
            url_actual = url_principal + actual_page
            if self.__isAllowed(url_actual, fileLog):
                try:
                    print('.',end='')
                    #Descarreguem la pàgina url_actual
                    htmlDom = self.__download_page(url_actual);
                    soup = BeautifulSoup(htmlDom,'html.parser');
                    if (soup.find(id="trails") == None):
                        raise Exception('Soup Error: There arent trail links for ' + url_actual);
                    #Recorrem totes les rutes de la pàgina
                    for row in soup.find(id="trails").find_all_next('div', 'row'):
                        #print(row.find('a', 'rating-container')) #Test
                        if row.find('a', 'rating-container') != None:
                            url_rutes_regio2.append(row.find('a', 'trail-title').get('href'))        
                    next = soup.find('a', 'next')
                    if next != None:
                        actual_page = next.get('href')
                except Exception as e:
                    fileLog.write(str(e)+'\n')
                    break
            else:
                break
        fileLog.write('Num rutes valorades a '+url_principal+' -> '+str(len(url_rutes_regio2))+'\n')
        fileLog.flush()
        return url_rutes_regio2
        
        
    """
    Desc: 
        Es carrega tota la pàgina .html a l' objecte de tipus [BeautifulSoup]
        i es fa una instància d' un Dictionary que és l'objecte que guardarà
        tota la informació obtinguda de la pàgina desprès de fer el 
        Web Scrapping
    Params:
        paramUrl: adreça url de la pàgina a tractar
    """
    def start_ruta(self, paramUrl):
        self.__data:dict = dict();
        htmlDom:str = None;
        
        try:
            htmlDom = self.__download_page(paramUrl);
            self.__soup = BeautifulSoup(htmlDom,'html.parser');
            self.__data['Url'] = paramUrl;
            
            #Code to use when the html page is a file
            """
            with open(paramUrl, 'r', encoding='utf-8') as foo_file:
                self.__soup = BeautifulSoup(foo_file,'lxml');
                self.__data['Url'] = paramUrl;
            """
        except Exception as e:
            raise Exception("Method start_ruta(): Error: {0}".format(e));
    
    """
    Desc:
        Eliminem de la memòria tant el Dictionary com l'obj. [BeautifulSoup],
        d' aquesta manera estaran lliures quan tornem a fer Scrapping
        amb la següent pàgina
    """
    def stop(self):
        del self.__soup;
        del self.__data;
    
    
    """
    Desc: 
        Obtenim el valor que indica la posició d'aquesta ruta dins del ranking
        del site
    """
    def getTrailRank(self) -> str:

        myValue:str = "";
        obj1:object = None;
        obj2:object = None;
        
        try:
            #Obtenim un obj. de tipus [bs4.element.ResultSet]
            obj1 = self.__soup.find_all("div", {"class":"breadcrumb-title"});
            if (len(obj1) != 1):
                raise Exception('soup Error: There are more than one tag with the class [breadcrumb-title]');
            else:
                #Obtenim un obj. de tipus [bs4.element.Tag] en cada iteració
                for item in obj1:
                    #Obtenim un obj. de tipus [bs4.element.ResultSet]
                    obj2 = item.find_all("a",{"class":"trail-rank good"})
                    if (len(obj2) != 1):
                       raise Exception('Soup Error: There are more than one tag <a> with the class [trail-rank good]'); 
                    else:
                        #Si volem saber tots els atributs que té el tag haurem
                        #d'accedir al dictionary .attrs
                        #Amb el métode items() covertim el dictionary en list
                        if constants.ATTR_TITLE in obj2[0].attrs:
                            myValue = obj2[0].attrs[constants.ATTR_TITLE];
                            if (myValue == constants.ATTR_TRAILRANK):
                                self.__data['TrailTrack'] = obj2[0].text;
                                myValue = obj2[0].text;
                            else:
                                raise Exception('Soup Error: There is not a TrailRank title')
                        else:
                            raise Exception('Soup Error: There is not an attribute [title]');
                            
                return(myValue);
        except Exception as e:
            raise Exception("Method getTrailRank(): Error: {0}".format(e));
        finally:
            if (obj1 != None):
                del obj1;
            if (obj2 != None):
                del obj2;
            del myValue;
    
    
    """
    Desc:
        Obtenim el tipus de ruta que estem avaluant
    """
    def getTypeTrack(self) -> str:

        myValue:str = "";
        obj1:object = None;
        obj2:object = None;
        
        try:
            #Obtenim un obj. de tipus [bs4.element.ResultSet]
            obj1 = self.__soup.find_all("div", {"class":"col-xs-12 col-sm-7 col-md-8 col-lg-9"});
            if (len(obj1) != 1):
                raise Exception('soup Error: There are more than one tag with the class [col-xs-12 col-sm-7 col-md-8 col-lg-9]');
            else:
                #Obtenim un obj. de tipus [bs4.element.Tag] en cada iteració
                for item in obj1:
                    #Obtenim un obj. de tipus [bs4.element.ResultSet]
                    obj2 = item.find_all("a",id="activity-badge")
                    if (len(obj2) != 1):
                       raise Exception('Soup Error: There are more than one tag <a> with the id [activity-badge]'); 
                    else:
                        #Si volem saber tots els atributs que té el tag haurem
                        #d'accedir al dictionary .attrs
                        #Amb el métode items() covertim el dictionary en list
                        if constants.ATTR_TITLE in obj2[0].attrs:
                            myValue = obj2[0].attrs[constants.ATTR_TITLE];
                            self.__data['TypeTrack'] = myValue;
                        else:
                            raise Exception('Soup Error: There is not an attribute [title]');
                            
                return(myValue);
        except Exception as e:
            raise Exception("Method getTypeTrack(): Error: {0}".format(e));
        finally:
            if (obj1 != None):
                del obj1;
            if (obj2 != None):
                del obj2;
            del myValue;
            
    
    """
    Desc:
        Obtenim la puntuació que té l'usuari que ha pujat la ruta dins del ranking
        del site
    """
    def getUserRank(self) -> str:

        myValue:str = "";
        obj1:object = None;
        obj2:object = None;
        
        try:
            #Obtenim un obj. de tipus [bs4.element.ResultSet]
            obj1 = self.__soup.find_all("div", {"class":"user-box clearfix"});
            if (len(obj1) != 1):
                raise Exception('Soup Error: There are more than one tag with the class [user-box clearfix]');
            else:
                #Obtenim un obj. de tipus [bs4.element.Tag] en cada iteració
                for item in obj1:
                    #Obtenim un obj. de tipus [bs4.element.ResultSet]
                    obj2 = item.find_next("div", {"class":"user-tags"}).find_next("a",{"class":"utag userrank"})
                    if (obj2 != None):
                        myValue = obj2.text;
                        self.__data['UserRank'] = myValue;
                    else:
                        raise Exception('Soup Error: There is not an attribute [title=UserRank]');
                            
                return(myValue);
        except Exception as e:
            raise Exception("Method getUserRank(): Error: {0}".format(e));
        finally:
            if (obj1 != None):
                del obj1;
            if (obj2 != None):
                del obj2;
            del myValue;
        
        
    def __getInf(self, paramList, paramTag):
        
        myList:list = None;
        
        try:
            for item in paramList:
                if (item == 'icon-length'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data[myList[0]] = myList[1] + ' ' + myList[2];
                elif (item == 'icon-loop'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data['Loop'] = myList[1];
                elif (item == 'icon-uphill'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data[myList[0] + ' ' + myList[1]] = myList[2] + ' ' + myList[3];
                elif (item == 'icon-height'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data[myList[0] + ' ' + myList[1]] = myList[2] + ' ' + myList[3];
                elif (item == 'icon-downhill'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data[myList[0] + ' ' + myList[1]] = myList[2] + ' ' + myList[3];
                elif (item == 'icon-low'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data[myList[0] + ' ' + myList[1]] = myList[2] + ' ' + myList[3];
                elif (item == 'icon-difficult'):
                    myList = paramTag.a['title'].rsplit("\xa0");
                    self.__data[myList[0]] = myList[1];
                    
                myList = None;
        except Exception as e:
            raise Exception("Method __getInf(): Error: {0}".format(e));
        finally:
            myList = None;
    
    """
    Desc:
        Obtenim informació variada sobre la ruta avaluada:
            Distància                          Es circular
            Desnivell acumulat pujant          Alçada màxima
            Desnivell acumulat baixant         Alçada mínima
            Dificultad Tècnica
    """
    def getDataTrack(self):

        spanClass:list = None;
        obj1:object = None;
        obj2:object = None;
        
        try:
            #Obtenim un obj. de tipus [bs4.element.ResultSet]
            obj1 = self.__soup.find_all("div", {"class":"data-items clearfix"});
            if (len(obj1) != 1):
                raise Exception('Soup Error: There are more than one tag with the class [data-items clearfix]');
            else:
                #Obtenim un obj. de tipus [bs4.element.Tag] en cada iteració
                for item in obj1:
                    #Obtenim un obj. de tipus [bs4.element.ResultSet]
                    obj2 = item.find_all_next("div", {"class":"d-item"})
                    if (obj2 != None):
                        for itemsNext in obj2:
                            spanClass = itemsNext.a.span['class'];
                            self.__getInf(spanClass, itemsNext);
                            
                    else:
                        raise Exception('Soup Error: There is not an attribute [title=UserRank]');
                            
        except Exception as e:
            raise Exception("Method getDataTrack(): Error: {0}".format(e));
        finally:
            if (obj1 != None):
                del obj1;
            if (obj2 != None):
                del obj2;
            if (spanClass != None):
                del spanClass;
       
            
    """        
    Desc:
        Obtenim la data de realització de la ruta
    """
    def getDateCreation(self) -> str:

        myValue:str = "";
        obj1:object = None;
        
        try:
            #Obtenim un obj. de tipus [bs4.element.ResultSet]
            obj1 = self.__soup.find("div", id = "trail-data").find_next("div",{"class":"more-data"})
            if (obj1 == None):
                raise Exception('Soup Error: There are more than one tag with the class [more-data]');
            else:
                #myValue = obj1.find_next("h4").find_next("h4").find_next("h4").find_next("h4").text;
                myValue = obj1.find_next("h4")
                while (myValue.text.find(constants.FIELD11,0,len(myValue.text)) == constants.NOTFOUND and
                       myValue.text.find(constants.FIELD11_ENG,0,len(myValue.text)) == constants.NOTFOUND and
                       myValue.text.find(constants.FIELD11_CAT,0,len(myValue.text)) == constants.NOTFOUND):
                    myValue = myValue.find_next("h4");
                    
                self.__data[myValue.text.rsplit("\xa0")[0]] = myValue.text.rsplit("\xa0")[1];
                
                return(myValue);
        except Exception as e:
            raise Exception("Method getDateCreation(): Error: {0}".format(e));
        finally:
            if (obj1 != None):
                del obj1;
            del myValue;
            
            
    """
    Desc:
        Obtenim la valoració feta pels usuaris d'aquesta ruta, obtenim:
            La valoració sobre 5
            Quantitat de vots efectuats
    """        
    def getVotes(self) -> str:

        myValue:str = "";
        myText:list = None;
        #myPos:int = 0;
        obj1:object = None;
        
        try:
            #Obtenim un obj. de tipus [bs4.element.Tag]
            obj1 = self.__soup.find("div", id = "trail-rating").find_next("ul",{"class":"ratings"});
            if (obj1 == None):
                raise Exception('Soup Error: There are more than one tag with the class [ratings]');
            else:
               #Obtenim un obj. de tipus [list] amb tots els tags fills del tag analitzat
               myText = obj1.contents[1]['title'].rsplit("\xa0");
               myText = myText[0].split(' ');
               #URL's en anglès
               if (myText[0] == 'Rated'):
                   self.__data[myText[0]] = myText[1] + ' ' + myText[2] + ' ' + myText[3] + ' ' + myText[4];
                   pos = myText[6].rfind(')');
                   self.__data[myText[6][0:pos]] = myText[5][1:9];
               else:
                   self.__data[myText[0]] = myText[1] + ' ' + myText[2] + ' ' + myText[3];
                   pos = myText[5].rfind(')');
                   self.__data[myText[5][0:pos]] = myText[4][1:9];
                
                
            return(myValue);
        except Exception as e:
            raise Exception("Method getVotes(): Error: {0}".format(e));
        finally:
            if (obj1 != None):
                del obj1;
            del myValue;
            
    """
    Desc:
        Obtenim característiques de la ruta avaluada que ens indiquen quines
        particularitats té, com a ara si hi podem trobar:
            Llacs
            Fonts
            Rius
            Parquings
            Ponts
            Refugis Coverts
            Refugis Gratuits
            Panoràmiques
            Cascades d' aigua
            
    """        
    def getCards(self):

        myValue:int = 0;
        myActivities:dict = None;
        obj1:object = None;
        
        
        myActivities = {
                "Lake":0,
                "Fountain":0,
                "Panoramic":0,
                "River":0,
                "CarPark":0,
                "Bridge":0,
                "WaterFall":0,
                "Refuge":0,
                "Shelter":0
            }
        
        try:
            #Obtenim un obj. de tipus [bs4.element.ResulSet]
            obj1 = self.__soup.find("div", id = "cointainer-simplecard").find_all_next("div",{"class":"simplecard"});
            if (obj1 == None):
                raise Exception('Soup Error: There are more than one tag with the class [ratings]');
            else:
               #Obtenim un obj. de tipus [bs4.element.Tag]
               for item in obj1:                   
                   if (item.a.span['class'][1] == constants.LAKE):
                       myValue = myActivities['Lake'] + 1;
                       myActivities['Lake'] = myValue;
                   elif (item.a.span['class'][1] == constants.FOUNTAIN):
                       myValue = myActivities['Fountain'] + 1;
                       myActivities['Fountain'] = myValue;
                   elif (item.a.span['class'][1] == constants.PANORAMIC):
                       myValue = myActivities['Panoramic'] + 1;
                       myActivities['Panoramic'] = myValue;
                   elif (item.a.span['class'][1] == constants.RIVER):
                       myValue = myActivities['River'] + 1;
                       myActivities['River'] = myValue;
                   elif (item.a.span['class'][1] == constants.REFUGE):
                       myValue = myActivities['Refuge'] + 1;
                       myActivities['Refuge'] = myValue;
                   elif (item.a.span['class'][1] == constants.SHELTER):
                       myValue = myActivities['Shelter'] + 1;
                       myActivities['Shelter'] = myValue;
                   elif (item.a.span['class'][1] == constants.CARPARK):
                       myValue = myActivities['CarPark'] + 1;
                       myActivities['CarPark'] = myValue;
                   elif (item.a.span['class'][1] == constants.BRIDGE):
                       myValue = myActivities['Bridge'] + 1;
                       myActivities['Bridge'] = myValue;
                   elif (item.a.span['class'][1] == constants.WATERFALL):
                       myValue = myActivities['WaterFall'] + 1;
                       myActivities['WaterFall'] = myValue;
               
               for keys in myActivities:
                   if (myActivities[keys] == 0):
                       self.__data[keys] = 'No';
                   else:
                       self.__data[keys] = 'Si';
                
                
        except Exception as e:
            raise Exception("Method getCards(): Error: {0}".format(e));
        finally:
            del obj1;
            del myValue;
            del myActivities;