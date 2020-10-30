# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 21:45:53 2020

@author: XMB1483
"""
from protego import Protego

class RobotParser(object):
    host:str = "";
    robotsUrl:str = "";
    userAgent:str = "";
    
    def __init__(self, paramUrl, paramUserAgent='*'):
        self.robotParser:Protego = None;
        RobotParser.robotsUrl = paramUrl;
        RobotParser.userAgent = paramUserAgent;
        #print('Robots.txt: ' + RobotParser.robotsUrl + '\n');
        #print('User Agent: ' + RobotParser.userAgent + '\n')
       
    def create (self) -> Protego:
        try:
            self.robotParser = Protego.parse(RobotParser.robotsUrl);
        except Exception as e:
            raise Exception("Method create(): Error: {0}".format(e)); 
                
    def is_allowed (self, paramUrl) -> bool:
        try:
            if (self.robotParser.can_fetch(paramUrl,RobotParser.userAgent)):
                return (True);
            else:
                return (False);
        except Exception as e:
            raise Exception("Method is_allowed(): Error: {0}".format(e));
        