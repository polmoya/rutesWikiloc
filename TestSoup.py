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
    Per saber l'idioma en el que tenim que escriure les headers en aquest fitxer
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
        
        with open(constants.PATHCSVFILE, 'a') as csvfile:
            
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
        #myScrapper = ClassScrapper.Scrapper('E:\\UOC\\Subjects\\Tipologia_Dades\\PRACTICA\\PRACT1\\WikilocTest.html');
        #myScrapper = ClassScrapper.Scrapper('X:\\WikilocTest.html');
        
        #Obtenim una instancia del obj. [Scrapper]
        myScrapper = ClassScrapper.Scrapper();
        #Instancia de l'obj. [RobotParser]
        myRobotParser = ClassRobotParser.RobotParser(parse.urljoin(constants.MAIN_URL,constants.ROBOTS_FILE));
        #Creem un obj. de tipus [Protego]
        myRobotParser.create();
        
        #Validem si l' Url està permessa dins del site o no
        allowUrl = myRobotParser.is_allowed('https://ca.wikiloc.com/rutes-alpinisme/170722-100-cims-andorra-no-192-pic-de-la-serrera-des-dels-plans-de-ransol-18773078');
        if (allowUrl == False):
            raise Exception ('Url: ' + constants.RUTAS_PAGE + ' is NOT allowed... \n');
        
        #Arranquem l'acció per executar el Web Scrapping
        myScrapper.start('https://ca.wikiloc.com/rutes-alpinisme/170722-100-cims-andorra-no-192-pic-de-la-serrera-des-dels-plans-de-ransol-18773078');
        
        myScrapper.getTypeTrack();
        myScrapper.getTrailRank();
        myScrapper.getUserRank();
        myScrapper.getDataTrack();
        myScrapper.getDateCreation();
        
        #Tant els vots com les senyals del diferents punts de la ruta
        #són opcionals i per això hem de controlar la possibilitat
        #de que no hi siguin
        try:
            p = myScrapper.getVotes();
        except Exception as e:
            print(e);
        
        try:
            myScrapper.getCards();
        except Exception as e:
            print(e);
            
        print(myScrapper.data);
        
        for x in range(5):
            myDictData["url" + str(x)] = myScrapper.data;
            
        myScrapper.stop();
        
        
        #Arranquem l'acció per executar el Web Scrapping
        myScrapper.start('https://ca.wikiloc.com/rutes-alpinisme/160727-2x100-cims-andorra-pic-negre-denvalira-no-169-i-montmalus-no-170-des-de-grau-roig-14170224');
        
        p = myScrapper.getTypeTrack();
        p = myScrapper.getTrailRank();
        p = myScrapper.getUserRank();
        myScrapper.getDataTrack();
        p = myScrapper.getDateCreation();
        
        #Tant els vots com les senyals del diferents punts de la ruta
        #són opcionals i per això hem de controlar la possibilitat
        #de que no hi siguin
        try:
            p = myScrapper.getVotes();
        except Exception as e:
            print(e);
        
        try:
            myScrapper.getCards();
        except Exception as e:
            print(e);
            
        print(myScrapper.data);
        
        for x in range(5,10):
            myDictData["url" + str(x)] = myScrapper.data;
        
        writeCSV(myDictData);
            
        
    except Exception as e:
        print(e);
    finally:
        del myScrapper;
        del myDictData;
        del myRobotParser;


            