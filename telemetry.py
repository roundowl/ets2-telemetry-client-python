import urllib.request
import json

class telemetry():
  connected = False
  serverIP = ""

  def update(self):
    try:
      self.jsonResponse = urllib.request.urlopen \
      ("http://" + self.serverIP + ":25555/api/ets2/telemetry")
      self.ets2 = json.loads(self.jsonResponse.read().decode("UTF-8"))
      self.connected = True
    except:
      self.connected = False

