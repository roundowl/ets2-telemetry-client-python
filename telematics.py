import processing
import json
import datetime
from tkinter import filedialog

class telematics:
  def __init__(self):
    self.data = 0
    self.settings = dict()
    self.braking = False
    self.speed = 0.0
    self.accelerating = False

  def initFiles(self):
    try:
      with open(self.settings['lastFile'], mode='r') as file:
        self.output = json.loads(file.read())
    except FileNotFoundError:
      self.output = {
      'timestamp' : 0,               ## IRL datetime object
      
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
      'drivingWithWarning' : 0,      # % of distance
      'averageDriverScore' : 'N/A',      # %
      
      #Lifetime data
      'totalDistanceDriven' : 0.0,   ## km
      'distanceWithTrailer' : 0,     ## km
      'distanceWithWarning' : 'N/A',     # km
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
      with open('./data/accountList.json', mode='r') as file:
        self.accountList = json.loads(file.read())
    except FileNotFoundError:
      self.accountList = dict() # Expects following format.
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
    # Fuel
    self.output['fuelUsed'] += processing.getFuelChange(self)
    # Time
    if (self.data.current['truck']['engineOn']):
      self.output['engineRunningTime'] += self.data.deltaUpdate.total_seconds()/3600
      self.output['fuelUsedPerHour'] = self.output['fuelUsed'] / self.output['engineRunningTime']
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

  def updateData(self):
    self.updateTotals()
    self.updateTransportWork()
    self.updateAverageFuelConsumption()
    self.updateIdlingCoastingSpeeding()
    self.updateEngineOverspeed()
    self.updateSpeeds()
    self.updateCounts()
    self.updateTimestamp()

  def openFile(self):
    self.settings['lastFile'] = filedialog.askopenfilename(filetypes=[('JSON file', '.json'), ('All files', '*')])
    try:
      with open(self.settings['lastFile'], mode='r') as file:
        self.output = json.loads(file.read())
    except FileNotFoundError:
      pass

  def saveFile(self):
    self.settings['lastFile'] = filedialog.asksaveasfilename(filetypes=[('JSON file', '.json'), ('All files', '*')], initialfile=self.settings['lastFile'])
    try:
      with open(self.settings['lastFile'], mode='w') as file:
        file.write(json.dumps(self.output))
    except:
      return
    with open(self.settings['lastFile'].rsplit('/',1)[0] + '/settings.json', mode='w') as file:
        file.write(json.dumps(self.settings))
    id = self.settings['lastFile'].split('.')[0]
    id = id.rsplit('/',1)[1]
    if (not (id in self.accountList)):
      self.accountList[id] = dict()
    try:
      with open(self.settings['lastFile'].split('.')[0] + '.0.json', mode='r') as file:
        self.accountList[id]['start'] = self.output['timestamp']
    except:
      with open(self.settings['lastFile'].split('.')[0] + '.0.json', mode='w') as file:
        self.output['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d<br>%H:%M:%S")
        file.write(json.dumps(self.output))
        self.accountList[id]['start'] = self.output['timestamp']
    self.accountList[id]['id'] = id
    self.accountList[id]['filename'] = self.settings['lastFile']
    self.accountList[id]['stop'] = self.output['timestamp']
    try:
      self.accountList[id]['odometer'] = self.data.current['truck']['odometer']
    except:
      self.accountList[id]['odometer'] = 0
    self.accountList[id]['distance'] = self.output['totalDistanceDriven']
    self.accountList[id]['totalFuel'] = self.output['fuelUsed']
    self.accountList[id]['averageFuel'] = self.output['averageFuelConsumption']
    self.accountList[id]['averageSpeed'] = self.output['averageSpeed']
    self.accountList[id]['rating'] = 'N/A' #TODO: Make rating system
    with open(self.settings['lastFile'].rsplit('/',1)[0] + '/accountList.json', mode='w') as file:
      file.write(json.dumps(self.accountList))