from tsl2561 import TSL2561
import time

class light2561:
	def __init__(self):
		self.lux = 0

	def readData(self):
		tsl = TSL2561(debug=True)
		self.lux = tsl.lux()
		print 'Lux is ', self.lux

