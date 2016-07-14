import time
import math
import datetime
import telematics

def gameConnected(self):
  return self.data.current['game']['connected']

# Delta values since last telemetry frame
# Positive, unless stated otherwise

def deltaGameTime(self): # datetime.timedelta object, in-game time
  return self.data.current['game']['time'] - self.data.last['game']['time']

def getOdometerChange(self): # kilometers
  return self.data.current['truck']['odometer'] - self.data.last['truck']['odometer']

def getFuelChange(self): # liters
  return self.data.last['truck']['fuel'] - self.data.current['truck']['fuel']

# Calculated values

def getSpeed(self):
  return self.data.current['truck']['speed']

def getSpeedAsDerivative(self):
  if (deltaGameTime(self).total_seconds() == 0):
    speed = 0
  else:
    speed = getOdometerChange(self) / (deltaGameTime(self).total_seconds()/3600)
  return speed

def getTurbocharger(self):
  # roundowl:
  # self.data.current['truck']['gameThrottle'] *\
  # self.data.current['truck']['oilPressure'] *\
  #(self.data.current['truck']['engineRpm']*0.001)
  # m4rc10w:
  return  self.data.current['truck']['gameThrottle'] *\
         (self.data.current['truck']['oilPressure'] * 1.4) *\
         (self.data.current['truck']['engineRpm']*0.035)

def getTransportWork(self):
  return self.data.current['trailer']['mass']/1000 \
       * getOdometerChange(self) / getFuelChange(self)

def addRunningData(self):
  telematics.transportWork += getTransportWork(self)
  telematics.fuelUsed += getFuelChange(self)
  telematics.distanceTravelled += getOdometerChange(self)
  telematics.engineRunningTime += 0
  telematics.engineIdlingTime += 0

def getAverageFuelConsumption(self): # liters per 100 km
  return (telematics.fuelUsed / telematics.distanceTravelled)*100
