import tkinter as tk
import tkinter.ttk as ttk
import telemetry
from processing import *

class Application(tk.Frame):
  values = {}
  widgets = {}

  def __init__(self, master=None):
    tk.Frame.__init__(self, master)
    self.data = telemetry.telemetry()
    self.assignVariables()
    self.processData()
    self.createWidgets()
    self.updateTelemetry()

  def assignVariables(self):
    self.values['Game connected'] = tk.StringVar()
    self.values['Speed'] = tk.StringVar()
    
  def processData(self):
    self.data.update()
    self.values['Game connected'].set(str(gameConnected(self)))
    self.values['Speed'].set(str(self.data.ets2['truck']['speed']))

  def createWidgets(self):
    r = 0
    for name, var in self.values.items():
      ttk.Label(root, text=name, width=15).grid(row=r,column=0)
      ttk.Label(root, textvariable=self.values[name], width=10).grid(row=r,column=1)
      r = r + 1
      
  def updateTelemetry(self):
    if (self.data.running == True):
      self.processData()
    self.after(self.data.interval, self.updateTelemetry)
      
root = tk.Tk()
app = Application(master=root)
app.mainloop()
