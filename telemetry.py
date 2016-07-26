import urllib.request
import json
import re
import datetime
import copy

class telemetry():
  connected = False
  serverIP = ""
  lastIngameTimestamp = 0
  deltaUpdate = 0
  last = 0

  def update(self):
    try:
      if (self.connected):
        self.last = copy.deepcopy(self.current)
      self.jsonResponse = urllib.request.urlopen \
      ("http://" + self.serverIP + ":25555/api/ets2/telemetry")
      self.current = json.loads(self.jsonResponse.read().decode("UTF-8"), object_hook=self.datetime_parser)
      if(not self.connected):                   # Makes first "last snapshot" equal to current
        self.last = copy.deepcopy(self.current) # since another one does not exist yet
        self.lastUpdateTimestamp = datetime.datetime.now()
      
      self.deltaUpdate = (datetime.datetime.now() - self.lastUpdateTimestamp) * self.current['game']['timeScale']
      self.last['game']['time'] = self.current['game']['time'] - self.deltaUpdate
      self.lastUpdateTimestamp = datetime.datetime.now()
      
      self.connected = True
    except:
      self.connected = False

  def datetime_parser(self, dct):
    for k, v in dct.items():
      if isinstance(v, str) and re.search("Z", v):
        try:
          DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
          dct[k] = datetime.datetime.strptime(v, DATE_FORMAT)
        except:
          pass
    return dct

