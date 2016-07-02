import urllib.request
import json

class telemetry():
  ets2 = {'game': {'connected' : False}}
  running = True
  interval = 100
  serverIP = "127.0.0.1"
  
  def stop(self):
    self.running = False
    print("Telemetry reading stopped")

  def start(self):
    self.running = True
    print("Telemetry reading started")

  def update(self):
    try:
      self.jsonResponse = urllib.request.urlopen \
      ("http://" + self.serverIP + ":25555/api/ets2/telemetry")
      self.ets2 = json.loads(self.jsonResponse.read().decode("UTF-8"))
    except:
      self.ets2['game']['connected'] = False
      print("No connection")
