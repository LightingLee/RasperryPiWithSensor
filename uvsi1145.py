import time
import SI1145.SI1145 as SI1145

class uv1145:
	def __init__(self):
            self.uv_index = 0
            self.sensor = SI1145.SI1145()

	def readData(self):
            UV = self.sensor.readUV()
            self.uv_index = UV / 100.0
            print 'UV index is ', self.uv_index
