import tkinter as tk
import tkinter.ttk as ttk
import telemetry
import datetime
from processing import *

class Application(tk.Frame):
  values = {}
  widgets = {}
  telemetryRunning=False
  intervalCounter = 0

  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.data = telemetry.telemetry()
    self.telematics = telematics.telematics()
    self.telematics.data = self.data
    self.assignVariables()
    self.createWidgets()
    self.updateTelemetry()

  def assignVariables(self):
    #Config
    self.connectedMessage = tk.StringVar()
    self.connectedMessage.set("Disconnected\nConnect")
    self.serverIP = tk.StringVar()
    self.interval = tk.IntVar()
    self.interval.set(1000)
    self.serverIP.set("127.0.0.1")
    #Variables
    self.values['Game connected'] = tk.StringVar()
    self.values['Time'] = tk.StringVar()
    self.values['Derivative'] = tk.StringVar()

  def processData(self):
    self.data.update()
    if (self.data.connected):
      if (not self.data.current['game']['paused']):
        self.telematics.updateData()
        self.values['Game connected'].set(str(gameConnected(self)))
        self.values['Time'].set(str(self.data.current['game']['time'].strftime("%Y-%m-%dT%H:%M:%SZ")))
        self.values['Derivative'].set(str(getSpeedAsDerivative(self)))

  def createWidgets(self):
    #Configuration
    ttk.Entry(root, textvariable=self.serverIP, width=16).grid(row=0,column=0,sticky='news')
    ttk.Entry(root, textvariable=self.interval, width=6).grid(row=0,column=1,sticky='news')
    #Buttons
    tk.Button(root, textvariable=self.connectedMessage, justify='center', command=self.connectToServer).\
      grid(row=1,column=0,columnspan=2,sticky='news')
    tk.Button(root, text='Save to file', justify='center', command=self.telematics.updateFile).\
      grid(row=2,column=0,columnspan=2,sticky='news')
    #Variables
    r = 3
    for name, var in self.values.items():
      ttk.Label(root, text=name, width=15).grid(row=r,column=0)
      ttk.Label(root, textvariable=self.values[name], width=20).grid(row=r,column=1)
      r = r + 1

  def connectToServer(self):
    self.telemetryRunning = not self.telemetryRunning
    self.data.serverIP = self.serverIP.get()

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
        self.connectedMessage.set("Disconnected\nConnect")
    self.intervalCounter += 100
    self.after(100, self.updateTelemetry)

root = tk.Tk()
global app
app = Application(master=root)
root.title("Telemetry App 0.3.1")
root.focus()
app.mainloop()
