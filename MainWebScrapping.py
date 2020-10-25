# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 14:59:34 2020

@author: XMB1483
"""

from bs4 import BeautifulSoup
#import robots
import TasksWithPages
from urllib import parse
import datetime
import constants



if __name__ == '__main__':
    url:str = '';
    fileLog:None;
    initDate:datetime;
    elapsed:float;
    soup:BeautifulSoup;
    htmlPage:str = '';
    linksLevel1:list;
    linksLevel2:list;
    linksLevel3:list;
    linksLevel4:list = list();
    tagHref:str = '';
    linksHrefLevel1:list;
    linksHrefLevel2:list = list();
    linksHrefLevel3:list = list();
    linksHrefLevel4:list = list();
    
    url = parse.urljoin(constants.MAIN_URL,constants.RUTAS_PAGE);

    try:
        initDate = datetime.datetime.now();
        fileLog = open(constants.LOG_FILE,'a');
        fileLog.write(str(datetime.datetime.now()) + ' ======== Start The Web Scrapping =========\n');
        htmlPage = TasksWithPages.download_page(url);
        #Si hem pogut fer la connexió passem a crear un obj de tipu [BeautifulSoup]
        soup = BeautifulSoup(htmlPage,'html.parser');
        #for link in soup.find_all('a'):
        #    fileLog.write(link.get('href') + '\n')
        print(str(type(soup)));
        print('Type Soup: ' + soup.section.name);
        
        #Busquem els tags <section>, hauríem de trobar només 2
        #El métode retorna un obj. de tipus [bs4.element.ResultSet]
        linksLevel1 = soup.find_all('section');
        
        #Si obtenim més de 2 tags <section> ha hagut un canvi a l'estructura
        #de la pàgina
        if (len(linksLevel1) != constants.QTY_TAGSLEVEL1):
            raise Exception('The structure of site has been modified...');
        #Quan iterem, cada element obtingut és de tipus [bs4.element.Tag]
        for link in linksLevel1:
            #Validem el tag <h1>
            if (link.h1.text.upper() == constants.H1_ACTIVIDADES):
                continue;
            fileLog.write(str(datetime.datetime.now()) + ' ' + str(link)+'\n');
            linksHrefLevel1 = TasksWithPages.get_Links(link,'andorra');
            #linksHref = TasksWithPages.get_Links(link);
            for url1 in linksHrefLevel1:
                fileLog.write('Level1: Url -> ' + url1 + '\n');
                htmlPage = TasksWithPages.download_page(url1);
                soup = None;
                soup = BeautifulSoup(htmlPage,'html.parser');
                #En aquest 2º nivell només hi podem trobar 2 tags
                #que tinguin aquesta estructura
                linksLevel2 = soup.find_all('ul', class_='limited-list');
                if (len(linksLevel2) != constants.QTY_TAGSLEVEL2):
                    raise Exception('The structure of site has been modified...');
                    
                for items in linksLevel2[0].find_all('li'):
                    fileLog.write('Level2: Url -> ' + items.a.get('href') + '\n');
                    linksHrefLevel2.append(items.a.get('href'));
                    
                for url2 in linksHrefLevel2:
                    htmlPage = None;
                    htmlPage = TasksWithPages.download_page(url2);
                    soup = None;
                    soup = BeautifulSoup(htmlPage,'html.parser');
                    #En aquest 2º nivell només hi podem trobar 2 tags
                    #que tinguin aquesta estructura
                    linksLevel3 = soup.find_all('ul', class_='limited-list');
                    if (len(linksLevel3) != constants.QTY_TAGSLEVEL3):
                        raise Exception('The structure of site has been modified...');
                    
                    for items in linksLevel3[0].find_all('li'):
                        fileLog.write('Level3: Url -> ' + items.a.get('href') + '\n');
                        linksHrefLevel3.append(items.a.get('href'));
                        
                    for url3 in linksHrefLevel3:
                        print('Level3 -> Url: ' + url3);
                        if (url3.find('/andorra-la-vella/santa-coloma') > 0):
                            print('Stop');
                        htmlPage = None;
                        htmlPage = TasksWithPages.download_page(url3);
                        soup = None;
                        soup = BeautifulSoup(htmlPage,'html.parser');
                        linksLevel4.clear();
                        #En aquest 3º nivell només hi podem trobar 2 tags
                        #que tinguin aquesta estructura
                        linksLevel4 = soup.find_all('div', class_='info col-md-7 col-sm-6 col-xs-10');
                        if (len(linksLevel4) == constants.QTY_TAGSLEVEL4):
                            raise Exception('The structure of site has been modified...');
                    
                        for items in linksLevel4:
                            try:
                                fileLog.write('Level4: Name: ' + items.h3.a.text + ' Url -> ' + items.h3.a.get('href') + '\n');
                            except Exception as e:
                                fileLog.write('Level4: Url -> ' + items.h3.a.get('href') + '\n');
                            print('Level4 -> Url: ' + items.h3.a.get('href'));
                            linksHrefLevel4.append(items.h3.a.get('href'));
        print('End...');            
    except Exception as e:
        fileLog.write('Failed -> ' + e.args[0] + '\n');
    finally:
        elapsed = (datetime.datetime.now() - initDate).total_seconds();
        fileLog.write(str(datetime.datetime.now()) + ' ======== Elapsed Time: ' + str(elapsed) + '=========\n');
        fileLog.write(str(datetime.datetime.now()) + ' ======== End The Web Scrapping =========\n');
        fileLog.close();
        soup = None;
        linksLevel1 = None;
        linksLevel2 = None;
        linksLevel3 = None;
        del linksLevel4;
        linksHrefLevel1 = None;
        linksHrefLevel2 = None;
        linksHrefLevel3 = None;
        linksHrefLevel4 = None;


