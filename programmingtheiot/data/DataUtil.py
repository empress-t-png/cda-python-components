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

import json
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	"""
	Utility class for converting data objects to/from JSON.
	
	"""
	
	def __init__(self, encodeToUtf8 = False):
		"""
		Constructor.
		
		@param encodeToUtf8 If True, encode to UTF-8. Default is False.
		"""
		self.encodeToUtf8 = encodeToUtf8
	
	def actuatorDataToJson(self, data: ActuatorData = None):
		"""
		Converts ActuatorData to JSON string.
		
		@param data The ActuatorData instance to convert.
		@return JSON string representation, or None if data is None.
		"""
		if data:
			jsonData = json.dumps(data, cls=JsonDataEncoder)
			if self.encodeToUtf8:
				return jsonData.encode('utf-8')
			return jsonData
		return None
	
	def sensorDataToJson(self, data: SensorData = None):
		"""
		Converts SensorData to JSON string.
		
		@param data The SensorData instance to convert.
		@return JSON string representation, or None if data is None.
		"""
		if data:
			jsonData = json.dumps(data, cls=JsonDataEncoder)
			if self.encodeToUtf8:
				return jsonData.encode('utf-8')
			return jsonData
		return None
	
	def systemPerformanceDataToJson(self, data: SystemPerformanceData = None):
		"""
		Converts SystemPerformanceData to JSON string.
		
		@param data The SystemPerformanceData instance to convert.
		@return JSON string representation, or None if data is None.
		"""
		if data:
			jsonData = json.dumps(data, cls=JsonDataEncoder)
			if self.encodeToUtf8:
				return jsonData.encode('utf-8')
			return jsonData
		return None
	
	def jsonToActuatorData(self, jsonData: str = None):
		"""
		Converts JSON string to ActuatorData object.
		
		@param jsonData The JSON string to convert.
		@return ActuatorData instance, or None if jsonData is None.
		"""
		if jsonData:
			jsonStruct = json.loads(jsonData)
			data = ActuatorData()
			self._updateIotData(data, jsonStruct)
			return data
		return None
	
	def jsonToSensorData(self, jsonData: str = None):
		"""
		Converts JSON string to SensorData object.
		
		@param jsonData The JSON string to convert.
		@return SensorData instance, or None if jsonData is None.
		"""
		if jsonData:
			jsonStruct = json.loads(jsonData)
			data = SensorData()
			self._updateIotData(data, jsonStruct)
			return data
		return None
	
	def jsonToSystemPerformanceData(self, jsonData: str = None):
		"""
		Converts JSON string to SystemPerformanceData object.
		
		@param jsonData The JSON string to convert.
		@return SystemPerformanceData instance, or None if jsonData is None.
		"""
		if jsonData:
			jsonStruct = json.loads(jsonData)
			data = SystemPerformanceData()
			self._updateIotData(data, jsonStruct)
			return data
		return None
	
	def _updateIotData(self, data, jsonStruct):
		"""
		Helper method to update data object attributes from JSON structure.
		
		@param data The data object to update.
		@param jsonStruct The JSON dictionary structure.
		"""
		# Update all attributes from the JSON structure
		for key in jsonStruct:
			if hasattr(data, key):
				setattr(data, key, jsonStruct[key])

class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		return o.__dict__