#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

from pisense import SenseHAT

class HumiditySensorEmulatorTask(BaseSensorSimTask):
	"""
	Humidity sensor emulator that generates simulated humidity data.
	"""

	def __init__(self, dataSet = None):
		super(HumiditySensorEmulatorTask, self).__init__(
			sensorType=ConfigConst.HUMIDITY_SENSOR_TYPE,
			minVal=SensorData.DEFAULT_MIN_HUMIDITY_VAL,
			maxVal=SensorData.DEFAULT_MAX_HUMIDITY_VAL,
			sensorName=ConfigConst.HUMIDITY_SENSOR_NAME
		)
	
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(
			sensorType=ConfigConst.HUMIDITY_SENSOR_TYPE,
			name=ConfigConst.HUMIDITY_SENSOR_NAME
		)
		
		# Get simulated humidity value from parent class
		sensorVal = self.generateTelemetryValue()
		
		sensorData.setValue(sensorVal)
		
		self.latestSensorData = sensorData
		
		return sensorData