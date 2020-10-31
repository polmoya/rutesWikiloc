# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 08:56:59 2020

@author: Xavier & Pol
"""
import ClassScrapper
import csv
import constants
import ClassRobotParser
from urllib import parse
import datetime
import sys


myScrapper:ClassScrapper.Scrapper = None;
myDictData:dict = dict();
myRobotParser:ClassRobotParser.RobotParser = None;
allowUrl:bool = False;


"""
Desc:
    Escriu en un fitxer de tipus .csv tots els elements d' un Dictionary.
    Estructura del Dictionary:
        Les keys tindran el format url####, on #### pot ser un nombre >= 0
        El value de cada key serà un altre Dictionary que contindrà les dades
        obtingudes desprès de fer Scrapping sobre una pàgina .html. Aquest
        Dictionary tindrà 23 keys amb els seus valors.
    Per saber l'idioma en el que hem d'escriure les headers en aquest fitxer
    hem avaluar la key 12 d' aquest Dictionary que en:
        Anglès té el value [Rated]
        Castellà té el value [Valoración]
        Català té el value [Valoració]
Params:
    paramDataUrls: dictionary que conté les dades obtingudes desprès de fer
    el Web Scrapping sobre la pàgina.
"""
def writeCSV(paramDataUrls:dict):
    fieldNames:list = None;
    
    try:
        #Segons l'idioma els headers seran uns o uns altres
        if (constants.FIELD12_ENG in paramDataUrls["url0"]):
            fieldNames = [constants.FIELD1,constants.FIELD2,constants.FIELD3,constants.FIELD4_ENG,
                          constants.FIELD5,constants.FIELD6_ENG,constants.FIELD7_ENG,constants.FIELD8_ENG,
                          constants.FIELD9_ENG,constants.FIELD10_ENG,constants.FIELD11_ENG,constants.FIELD12_ENG,
                          constants.FIELD13_ENG,constants.FIELD14,constants.FIELD15,constants.FIELD16,
                          constants.FIELD17,constants.FIELD18,constants.FIELD19,constants.FIELD20,
                          constants.FIELD21,constants.FIELD22,constants.FIELD23];
        elif (constants.FIELD12 in paramDataUrls["url0"]):
            fieldNames = [constants.FIELD1,constants.FIELD2,constants.FIELD3,constants.FIELD4,
                          constants.FIELD5,constants.FIELD6,constants.FIELD7,constants.FIELD8,
                          constants.FIELD9,constants.FIELD10,constants.FIELD11,constants.FIELD12,
                          constants.FIELD13,constants.FIELD14,constants.FIELD15,constants.FIELD16,
                          constants.FIELD17,constants.FIELD18,constants.FIELD19,constants.FIELD20,
                          constants.FIELD21,constants.FIELD22,constants.FIELD23];
        else:
            fieldNames = [constants.FIELD1,constants.FIELD2,constants.FIELD3,constants.FIELD4_CAT,
                          constants.FIELD5,constants.FIELD6_CAT,constants.FIELD7_CAT,constants.FIELD8_CAT,
                          constants.FIELD9_CAT,constants.FIELD10_CAT,constants.FIELD11_CAT,constants.FIELD12_CAT,
                          constants.FIELD13_CAT,constants.FIELD14,constants.FIELD15,constants.FIELD16,
                          constants.FIELD17,constants.FIELD18,constants.FIELD19,constants.FIELD20,
                          constants.FIELD21,constants.FIELD22,constants.FIELD23];
        
        #ToDo: Canviar path file al nom del CSV, ha de ser representatiu
        with open(constants.PATHCSVFILE, 'a', newline='') as csvfile:
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldNames);
            
            writer.writeheader();
            
            for x in range(len(paramDataUrls)):
                writer.writerow(paramDataUrls["url" + str(x)]);
            
    except Exception as e:
        raise Exception("Method writeCSV(): Error: {0}".format(e));
    finally:        
        if (fieldNames != None):
            del fieldNames;
    

if __name__ == '__main__':
    
    
    try:
        #S'inicialitza i s'obra el log
        initDate:datetime;
        elapsed:float;
        #Canviar nom a scrapper.log ??
        fileLog = fileLog = open('main.log','a');
        initDate = datetime.datetime.now()
        fileLog.write(str(datetime.datetime.now()) + ' ======== Start The Web Scrapping =========\n')
         
        
        '''
        #Llegim els arguments
        activitat=sys.argv[1]
        pais=sys.argv[2]
        regio1=sys.argv[3]
        regio2=sys.argv[4]
        '''
        #ToDo: Adaptar! Paràmetres per a testejar
        activitat='outdoor'
        pais='andorra'
        regio1='canillo'
        regio2='canillo'
        
        #Es normalitzen els arguments afegint la / per a accedir a la url
        if (pais != ''):
            pais = '/'+pais
        if (regio1 != ''):
            regio1 = '/'+regio1   
        if (regio2 != ''):
            regio2 = '/'+regio2
           
            
        #myScrapper = ClassScrapper.Scrapper('E:\\UOC\\Subjects\\Tipologia_Dades\\PRACTICA\\PRACT1\\WikilocTest.html');
        #myScrapper = ClassScrapper.Scrapper('X:\\WikilocTest.html');
        
        #Obtenim una instancia del obj. [Scrapper]
        myScrapper = ClassScrapper.Scrapper();
        #Instancia de l'obj. [RobotParser]
        myRobotParser = ClassRobotParser.RobotParser(parse.urljoin(constants.MAIN_URL,constants.ROBOTS_FILE));
        #Creem un obj. de tipus [Protego]
        myRobotParser.create();
    
    
        data = myScrapper.scrape(activitat, pais, regio1, regio2, fileLog)
        fileLog.write('Rutes trobades = '+str(len(data))+'\n')
        print('Rutes trobades = '+str(len(data)))
        writeCSV(data)
            
    except Exception as e:
        print(e);
    finally:
        del myScrapper;
        del myDictData;
        del myRobotParser;
        elapsed = (datetime.datetime.now() - initDate).total_seconds();
        fileLog.write(str(datetime.datetime.now()) + ' ======== Elapsed Time: ' + str(elapsed) + '=========\n');
        fileLog.write(str(datetime.datetime.now()) + ' ======== End The Web Scrapping =========\n');
        fileLog.close()


            