import urllib.parse
import urllib.request
import json

# POST
class tracking():
    id = "default"
    x = 0.0
    y = 0.0

    def upload(self):
        params = ('{"'+self.id+'":{"id":"'+self.id+'", "x":"'+str(self.x)+'", "y":"'+str(self.y)+'"}}').encode('utf-8')
        f = urllib.request.urlopen("http://roundowl.tk:23456", params)