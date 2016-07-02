import tkinter as tk
import tkinter.ttk as ttk
import telemetry
from processing import *

class Application(tk.Frame):
  values = {}
  widgets = {}
  telemetryRunning=False

  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.data = telemetry.telemetry()
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
    self.values['Speed'] = tk.StringVar()

  def processData(self):
    self.data.update()
    if (self.data.connected):
      self.values['Game connected'].set(str(gameConnected(self)))
      self.values['Speed'].set(str(self.data.ets2['truck']['speed']))

  def createWidgets(self):
    #Configuration
    ttk.Entry(root, textvariable=self.serverIP, width=16).grid(row=0,column=0,sticky='news')
    ttk.Entry(root, textvariable=self.interval, width=6).grid(row=0,column=1,sticky='news')
    #Button
    tk.Button(root, textvariable=self.connectedMessage, justify='center', command=self.connectToServer).\
      grid(row=1,column=0,columnspan=2,sticky='news')
    #Variables
    r = 2
    for name, var in self.values.items():
      ttk.Label(root, text=name, width=15).grid(row=r,column=0)
      ttk.Label(root, textvariable=self.values[name], width=10).grid(row=r,column=1)
      r = r + 1

  def connectToServer(self):
    self.telemetryRunning = not self.telemetryRunning
    self.data.serverIP = self.serverIP.get()

  def updateTelemetry(self):
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
    self.after(self.interval.get(), self.updateTelemetry)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
