import time
import math

def gameConnected(self):
  return self.data.ets2['game']['connected']

def getSpeed(self):
  return self.data.ets2['truck']['speed']

def getTurbocharger(self):
  return self.data.ets2['truck']['gameThrottle'] *\
         self.data.ets2['truck']['oilPressure'] *\
        (self.data.ets2['truck']['engineRpm']*0.001)
