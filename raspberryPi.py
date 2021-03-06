import os
import sys
import json
from webServer import *
from light import *
from blinds import *
from alarm import *

from uuid import getnode as getMac
import RPi.GPIO as io


class raspberryPi:
    allUserInfo = ''
    user = ''
    raspberryPi = ''
    id = 0
    userEndPoint = '/user/?format=json'
    piEndPoint = '/raspberry_pi/?format=json'
    response = ''
    mac = 0
    def __init__(self,webServer):
        self.getPiData(webServer)
        self.mac = getMac()
        io.setmode(io.BCM)
    
    def updatePiInfo(self,webServer,light,blind,alarm):
        response = webServer.getFromDatabase(self.userEndPoint)        
        light.updateLightInfo(response.json()['objects'][0]['lights'])
        blind.updateBlindInfo(response.json()['objects'][0]['blinds'])
        alarm.updateAlarmInfo(response.json()['objects'][0]['entrance'])
      
    def registerPi(self,webServer):
        data = {'uuid': 453665356334} #self.mac}
        if webServer.postToDatabase(data,self.piEndPoint):
            return 'RaspberryPi successfully register'
        else:
            return 'Problem registering RaspberryPi'
    def getPiData(self,webServer):
        self.response = webServer.getFromDatabase(self.userEndPoint)
        if not self.response:
            return
        else: 
            self.allUserInfo = self.response.json() 
            self.user = self.allUserInfo['objects'][0]
        if self.user['raspberry_pi']:
            self.raspberryPi = self.user['raspberry_pi'][0]
            self.id = self.raspberryPi['id']
        else:
            print 'no device found'
    def getId(self):
        return self.id
        
        
#web = webServer()
#light = light()
#blind = blinds()
#cam = camera()
#alarm = alarm()
#web.setUsername('shawn')
#web.setPassword('shawn')
#web.setAuth()

#pi = raspberryPi(web)
#pi.updatePiInfo(web,light,blind,alarm)
