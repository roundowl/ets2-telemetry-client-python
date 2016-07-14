import processing

class telemetry():
  distanceTravelled = 0.0
  fuelUsed = 0.0
  averageTransportWork = 0.0

  def getTransportWork(self):
    self.averageTransportWork *= self.fuelUsed
    self.fuelUsed += getFuelChange()
    self.distanceTravelled += getOdometerChange()
    self.averageTransportWork = (self.averageTransportWork + self.data.current['truck']['mass'] \
                          * getOdometerChange()) / fuelUsed

