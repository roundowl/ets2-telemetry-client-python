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
  return abs(self.data.current['truck']['odometer'] - self.data.last['truck']['odometer'])

def getFuelChange(self): # liters
  diff = self.data.last['truck']['fuel'] - self.data.current['truck']['fuel']
  if (diff > 0):
    return diff
  else:
    return 0

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
  self.data.current['truck']['gameThrottle'] *\
  self.data.current['truck']['oilPressure'] *\
 (self.data.current['truck']['engineRpm']*0.001)

def getTransportWork(self):
  return self.data.current['trailer']['mass']/1000 * getOdometerChange(self)

def getAverageFuelConsumption(self): # liters per 100 km
  try:
    return (getFuelChange() / getOdometerChange())*100
  except:
    return 0