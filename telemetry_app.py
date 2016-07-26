import tkinter as tk
import tkinter.ttk as ttk
import telemetry
import datetime
from processing import *
import json

class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.data = telemetry.telemetry()
    try:
      with open('settings.json', mode='r') as file:
        self.settings = json.loads(file.read())
    except FileNotFoundError:
      self.settings = {'lastFile':'default.json',
                       'serverIP':'127.0.0.1'}
    self.values = dict()
    self.intervalCounter = 0
    self.telematics = telematics.telematics()
    self.telematics.data = self.data
    self.telematics.settings = self.settings
    self.telematics.initFiles()
    self.telemetryRunning = False
    self.assignVariables()
    self.createWidgets()
    self.updateTelemetry()

  def assignVariables(self):
    #Config
    self.connectedMessage = tk.StringVar()
    self.connectedMessage.set("Initialising\nConnect")
    self.serverIP = tk.StringVar()
    self.interval = tk.IntVar()
    self.interval.set(1000)
    self.serverIP.set(self.settings['serverIP'])
    self.data.serverIP = self.serverIP.get()
    #Variables
    self.values['Game connected'] = tk.StringVar()
    self.values['Time'] = tk.StringVar()
    self.values['Distance'] = tk.StringVar()

  def processData(self):
    self.data.update()
    # "warp" fix below. Not in telemetry.py because of naming issues.
    # I noticed that while using warp command, derivative speed (distance per time)
    # becomes bigger than ['truck']['speed'] by warp amount, i.e.
    # 80kph * "warp 1.5" = 120kph. So I divide one by another and multiply
    # deltatime by the result, then update last['game']['time'] again.
    self.data.deltaUpdate *= (getSpeedAsDerivative(self) / getSpeed(self))
    self.data.last['game']['time'] = self.data.current['game']['time'] - self.data.deltaUpdate
    # end of warp fix
    if (self.data.connected):
      self.values['Game connected'].set(str(gameConnected(self)))
      if (not self.data.current['game']['paused'] and gameConnected(self)):
        self.telematics.updateData()
        self.values['Time'].set(str(self.data.current['game']['time'].strftime("%Y-%m-%dT%H:%M:%SZ")))
        self.values['Distance'].set(str(self.telematics.output['totalDistanceDriven']))

  def createWidgets(self):
    #Configuration
    ttk.Label(root, text='Server IP').grid(row=0, column=0, sticky='news')
    ttk.Label(root, text='Interval (ms)').grid(row=0,column=1, sticky='news')
    ttk.Entry(root, textvariable=self.serverIP).grid(row=1,column=0,sticky='news')
    ttk.Entry(root, textvariable=self.interval).grid(row=1,column=1,sticky='news')
    #Buttons
    tk.Button(root, textvariable=self.connectedMessage, justify='center', command=self.connectToServer).\
      grid(row=2,column=0,columnspan=2,sticky='news')
    tk.Button(root, text='Open', justify='center', command=self.telematics.openFile).\
      grid(row=3,column=0,sticky='news')
    tk.Button(root, text='Save', justify='center', command=self.telematics.saveFile).\
      grid(row=3,column=1,sticky='news')
    #Variables
    r = 4
    for name, var in self.values.items():
      ttk.Label(root, text=name, width=20).grid(row=r,column=0)
      ttk.Label(root, textvariable=self.values[name], width=20).grid(row=r,column=1)
      r = r + 1

  def connectToServer(self):
    self.telemetryRunning = not self.telemetryRunning
    self.data.serverIP = self.serverIP.get()
    self.telematics.settings['serverIP'] = self.serverIP.get()

  def updateTelemetry(self):
    if (self.intervalCounter >= (1*self.interval.get())):
      self.intervalCounter = 0
      if (self.telemetryRunning):
        self.processData()
        if (self.data.connected):
          if (gameConnected(self)):
            self.connectedMessage.set("Connected\nDisconnect")
          else:
            self.connectedMessage.set("Waiting for game\nDisconnect")
        else:
          self.connectedMessage.set("Connecting\nDisconnect")
      else:
        self.connectedMessage.set("Ready to connect\nConnect")
    self.intervalCounter += 100
    self.after(100, self.updateTelemetry)

root = tk.Tk()
app = Application(master=root)
root.title("Telemetry App 0.4.4")
root.focus()
app.mainloop()
