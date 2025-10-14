#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.data.SensorData import SensorData

from pisense import SenseHAT

class HumiditySensorEmulatorTask(BaseSensorSimTask):
	"""
	Humidity sensor emulator that generates simulated humidity data.
	"""

	def __init__(self, dataSet=None):
		super(HumiditySensorEmulatorTask, self).__init__(
			name=ConfigConst.HUMIDITY_SENSOR_NAME,
			typeID=ConfigConst.HUMIDITY_SENSOR_TYPE,
			dataSet=dataSet,
			minVal=0.0,
			maxVal=100.0
		)
		
		enableEmulation = ConfigUtil().getBoolean(
			ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.sh = SenseHAT(emulate=enableEmulation)
	
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(name=self.getName(), typeID=self.getTypeID())
		sensorVal = self.sh.environ.humidity
		
		sensorData.setValue(sensorVal)
		self.latestSensorData = sensorData
		
		return sensorData
