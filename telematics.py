import processing
import json
import datetime
from tkinter import filedialog
import os
import tracking

# TODO: Refactor this module so that try-except is used once per divisor value.
# Probably by making one function to count all relative values.

class telematics:
  def __init__(self):
    self.data = 0
    self.settings = dict()
    self.braking = False
    self.speed = 0.0
    self.accelerating = False
    self.tracking = tracking.tracking()
    self.tracking.data = self.data

  def initFiles(self):
    self.output = {
    'timestamp' : 0,               ## IRL "%Y-%m-%d<br>%H:%M:%S" string
    
    #Quality data
    'averageTransportWork' : 0.0,  ## tonne-km / litre
    'averageFuelConsumption' : 0,  ## l/100km
    'idling' : 0,                  ## % of engineRunning
    'engineOverspeed' : 0,         ## % of engineRunning
    'speeding' : 0,                ## % of engineRunning
    'outsideEngineSpeed' : 0,      ## % of engineRunning
    'brakeAppsPer100km' : 0,       ## No. per 100km
    'harshBrakeAppsPer100km' : 0,  ## No. per 100km
    'harshAccelPer100km' : 0,      ## No. per 100km
    'coasting' : 0,                ## % of distance
    'drivingWithWarning' : 0,      ## % of distance
    'averageDriverScore' : 0,      # %
    
    #Lifetime data
    'totalDistanceDriven' : 0.0,   ## km
    'distanceWithTrailer' : 0,     ## km
    'distanceWithWarning' : 0,     ## km
    'averageSpeed' : 0,            ## km/h
    'electricRunningTime' : 0.0,   ## hours
    'engineRunningTime' : 0.0,     ## hours
    'engineIdlingTime' : 0.0,      ## hours
    'engineOverspeedTime' : 0.0,   ## hours
    'engineOutsideRangeTime' : 0.0,## hours
    'speedingTime' : 0.0,          ## hours
    'fuelUsed' : 0.0,              ## litres
    'fuelUsedPerHour' : 0,         ## l/h
    'averageWeight' : 0,           ## tonne
    'transportWork' : 0,           ## tonne-km
    'maxVehicleSpeed' : 0,         ## km/h
    'maxEngineSpeed' : 0,          ## rpm
    'distanceWithCC' : 0,          ## km
    'coastingDistance' : 0,        ## km
    'brakeApps' : 0,               ## number
    'harshBrakeApps' : 0,          ## number
    'harshAccelerations' : 0,      ## number
    }
    try:
      with open(os.path.join(os.getcwd(), 'data', 'accountlist.json'), mode='r') as file:
        self.accountlist = json.loads(file.read())
    except FileNotFoundError:
      self.accountlist = dict() # Expects following format.
      #{ 
      #  'default' : {
      #    'id' : 'default',
      #    'filename' : 'default.json',
      #    'start' : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
      #    'stop' : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
      #    'odometer' : 0,
      #    'distance' : 0,
      #    'totalFuel' : 0,
      #    'averageFuel' : 0,
      #    'averageSpeed' : 0,
      #    'rating' : 0,
      #  }
      #}

  def updateTimestamp(self):
    self.output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d<br>%H:%M:%S")

  def updateTotals(self):
    # Distance
    self.output['totalDistanceDriven'] += processing.getOdometerChange(self)
    if (self.data.current['trailer']['attached']):
      self.output['distanceWithTrailer'] += processing.getOdometerChange(self)
    if (max([self.data.current['truck']['wearEngine'], self.data.current['truck']['wearTransmission'], \
             self.data.current['truck']['wearChassis'], self.data.current['truck']['wearCabin'],\
             self.data.current['truck']['wearWheels']]) > 0.15):
      self.output['distanceWithWarning'] += processing.getOdometerChange(self)
    try:
      self.output['drivingWithWarning'] = (self.output['distanceWithWarning'] / self.output['totalDistanceDriven']) * 100
    except:
      pass
    # Fuel
    self.output['fuelUsed'] += processing.getFuelChange(self)
    # Time
    if (self.data.current['truck']['engineOn']):
      self.output['engineRunningTime'] += self.data.deltaUpdate.total_seconds()/3600
      try:
        self.output['fuelUsedPerHour'] = self.output['fuelUsed'] / self.output['engineRunningTime']
      except:
        self.output['fuelUsedPerHour'] = 0
    if (self.data.current['truck']['electricOn']):
      self.output['electricRunningTime'] += self.data.deltaUpdate.total_seconds()/3600

  def updateTransportWork(self):
    self.output['transportWork'] += processing.getTransportWork(self)
    try:
      self.output['averageWeight'] = self.output['transportWork'] / self.output['distanceWithTrailer']
    except:
      pass
    try:
      self.output['averageTransportWork'] = self.output['transportWork'] / self.output['fuelUsed']
    except:
      pass

  def updateAverageFuelConsumption(self): # liters per 100 km
    try:
      self.output['averageFuelConsumption'] = self.output['fuelUsed'] / (self.output['totalDistanceDriven'] / 100)
    except:
      pass

  def updateIdlingCoastingSpeeding(self):
    if ((self.data.current['truck']['gameThrottle'] < 0.01) and (self.data.last['truck']['gameThrottle'] < 0.01)):
      self.output['coastingDistance'] += processing.getOdometerChange(self)
      if (processing.getFuelChange(self) > 0):
        self.output['engineIdlingTime'] += self.data.deltaUpdate.total_seconds()/3600
    else:
      if ((self.data.current['truck']['engineRpm'] > 1600 or self.data.current['truck']['engineRpm'] < 900) and (self.data.current['truck']['speed'] > 10)):
        self.output['engineOutsideRangeTime'] += self.data.deltaUpdate.total_seconds()/3600
        try:
          self.output['outsideEngineSpeed'] = (self.output['engineOutsideRangeTime'] / self.output['engineRunningTime'])*100
        except:
          pass 
      if (self.data.current['truck']['speed'] > (self.data.current['navigation']['speedLimit'] + 5) and (self.data.current['navigation']['speedLimit'] > 0)):
        self.output['speedingTime'] += self.data.deltaUpdate.total_seconds()/3600
        try:
          self.output['speeding'] = (self.output['speedingTime'] / self.output['engineRunningTime'])*100
        except:
          pass       
    try:
      self.output['idling'] = (self.output['engineIdlingTime'] / self.output['engineRunningTime'])*100
    except:
      pass
    try:
      self.output['coasting'] = (self.output['coastingDistance'] / self.output['totalDistanceDriven'])*100
    except:
      pass

  def updateEngineOverspeed(self):
    if (self.data.current['truck']['engineRpm'] > (self.data.current['truck']['engineRpmMax'] - 100)):
      self.output['engineOverspeedTime'] += self.data.deltaUpdate.total_seconds()/3600
    try:
      self.output['engineOverspeed'] = (self.output['engineOverspeedTime'] / self.output['engineRunningTime'])*100
    except:
      pass   

  def updateSpeeds(self):
    try:
      self.output['averageSpeed'] = self.output['totalDistanceDriven'] / self.output['electricRunningTime']
    except:
      pass
    if (self.data.current['truck']['cruiseControlOn']):
      self.output['distanceWithCC'] += processing.getOdometerChange(self)
    if (self.output['maxVehicleSpeed'] < self.data.current['truck']['speed']):
      self.output['maxVehicleSpeed'] = self.data.current['truck']['speed']
    if (self.output['maxEngineSpeed'] < self.data.current['truck']['engineRpm']):
      self.output['maxEngineSpeed'] = self.data.current['truck']['engineRpm']

  def updateCounts(self):
    # Brakings
    if (self.data.last['truck']['gameBrake'] < 0.1 and self.data.current['truck']['gameBrake'] > 0.1):
      self.braking = True
      self.speed = self.data.last['truck']['speed']
    if (self.data.current['truck']['gameBrake'] < 0.1 and self.data.last['truck']['gameBrake'] > 0.1):
      self.braking = False
      self.output['brakeApps'] += 1
      if ((self.speed**2) - (self.data.current['truck']['speed']**2) > 3200):
        self.output['harshBrakeApps'] += 1
    # Accelerations
    if (self.data.current['truck']['engineRpm'] > 1600 and self.data.current['truck']['userThrottle'] > 0.5 and not self.accelerating):
      self.accelerating = True
      self.speed = self.data.last['truck']['speed']
    if (self.data.current['truck']['userThrottle'] < 0.1 and self.data.last['truck']['userThrottle'] > 0.1):
      self.accelerating = False
      if ((self.data.current['truck']['speed']**2) - (self.speed**2) > 3200):
        self.output['harshAccelerations'] += 1
    # Both per 100 km
    try:
      self.output['brakeAppsPer100km'] = self.output['brakeApps'] / (self.output['totalDistanceDriven'] / 100)
      self.output['harshBrakeAppsPer100km'] = self.output['harshBrakeApps'] / (self.output['totalDistanceDriven'] / 100)
      self.output['harshAccelPer100km'] = self.output['harshAccelerations'] / (self.output['totalDistanceDriven'] / 100)
    except:
      pass

  def updatePosition(self):
    id = os.path.basename(self.settings['lastFile'])
    id = id.split('.')[0]
    self.tracking.id = id
    self.tracking.x = self.data.current['truck']['placement']['x']
    self.tracking.y = self.data.current['truck']['placement']['z']
    self.tracking.upload()

  def updateData(self):
    self.updateTotals()
    self.updateTransportWork()
    self.updateAverageFuelConsumption()
    self.updateIdlingCoastingSpeeding()
    self.updateEngineOverspeed()
    self.updateSpeeds()
    self.updateCounts()
    self.updateTimestamp()
    self.updatePosition()

  def openFile(self):
    self.settings['lastFile'] = filedialog.askopenfilename(filetypes=[('JSON file', '.json'), ('All files', '*')])
    try:
      with open(self.settings['lastFile'], mode='r') as file:
        self.output = json.loads(file.read())
    except FileNotFoundError:
      pass

  def saveFile(self):
    self.settings['lastFile'] = filedialog.asksaveasfilename(filetypes=[('JSON file', '.json'), ('All files', '*')], initialfile=self.settings['lastFile'])
    id = os.path.basename(self.settings['lastFile'])
    id = id.split('.')[0]
    # Return if file name was not chosen (user closed the dialog)
    if (len(id) < 1):
      return
    with open(os.path.join(os.getcwd(), 'settings.json'), mode='w') as file:
      file.write(json.dumps(self.settings))
    try:
      with open(os.path.join(os.getcwd(), 'data', (id + '.json')), mode='w') as file:
        file.write(json.dumps(self.output))
    except:
      return
    if (not (id in self.accountlist)):
      self.accountlist[id] = dict()
    try:
      with open(os.path.join(os.getcwd(), 'data', (id + '.0.json')), mode='r') as file:
        self.accountlist[id]['start'] = json.loads(file.read())['timestamp']
    except:
      with open(os.path.join(os.getcwd(), 'data', (id + '.0.json')), mode='w') as file:
        self.output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d<br>%H:%M:%S")
        file.write(json.dumps(self.output))
        self.accountlist[id]['start'] = self.output['timestamp']
    self.accountlist[id]['id'] = id
    self.accountlist[id]['filename'] = self.settings['lastFile']
    self.accountlist[id]['stop'] = self.output['timestamp']
    try:
      self.accountlist[id]['odometer'] = self.data.current['truck']['odometer']
    except:
      self.accountlist[id]['odometer'] = 0
    self.accountlist[id]['distance'] = self.output['totalDistanceDriven']
    self.accountlist[id]['totalFuel'] = self.output['fuelUsed']
    self.accountlist[id]['averageFuel'] = self.output['averageFuelConsumption']
    self.accountlist[id]['averageSpeed'] = self.output['averageSpeed']
    self.accountlist[id]['rating'] = 'N/A' #TODO: Make rating system
    with open(os.path.join(os.getcwd(), 'data', ('accountlist.json')), mode='w') as file:
      file.write(json.dumps(self.accountlist))
