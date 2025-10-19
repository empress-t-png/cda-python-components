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
import logging

from decimal import Decimal
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
		
		logging.info("Created DataUtil instance.")
	
	def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False):
		"""
		Converts ActuatorData to JSON string.
		
		@param data The ActuatorData instance to convert.
		@param useDecForFloat If True, use Decimal for float values.
		@return JSON string representation, or empty string if data is None.
		"""
		if not data:
			logging.debug("ActuatorData is null. Returning empty string.")
			return ""
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = useDecForFloat)
		
		return jsonData
	
	def sensorDataToJson(self, data: SensorData = None, useDecForFloat: bool = False):
		"""
		Converts SensorData to JSON string.
		
		@param data The SensorData instance to convert.
		@param useDecForFloat If True, use Decimal for float values.
		@return JSON string representation, or empty string if data is None.
		"""
		if not data:
			logging.debug("SensorData is null. Returning empty string.")
			return ""
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = useDecForFloat)
		
		return jsonData
	
	def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False):
		"""
		Converts SystemPerformanceData to JSON string.
		
		@param data The SystemPerformanceData instance to convert.
		@param useDecForFloat If True, use Decimal for float values.
		@return JSON string representation, or empty string if data is None.
		"""
		if not data:
			logging.debug("SystemPerformanceData is null. Returning empty string.")
			return ""
		
		jsonData = self._generateJsonData(obj = data, useDecForFloat = useDecForFloat)
		
		return jsonData
	
	def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts JSON string to ActuatorData object.
		
		@param jsonData The JSON string to convert.
		@param useDecForFloat If True, use Decimal for float values.
		@return ActuatorData instance, or None if jsonData is None.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		ad = ActuatorData()
		
		self._updateIotData(jsonStruct, ad)
		
		return ad
	
	def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts JSON string to SensorData object.
		
		@param jsonData The JSON string to convert.
		@param useDecForFloat If True, use Decimal for float values.
		@return SensorData instance, or None if jsonData is None.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		sd = SensorData()
		
		self._updateIotData(jsonStruct, sd)
		
		return sd
	
	def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False):
		"""
		Converts JSON string to SystemPerformanceData object.
		
		@param jsonData The JSON string to convert.
		@param useDecForFloat If True, use Decimal for float values.
		@return SystemPerformanceData instance, or None if jsonData is None.
		"""
		if not jsonData:
			logging.warning("JSON data is empty or null. Returning null.")
			return None
		
		jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat = useDecForFloat)
		
		spd = SystemPerformanceData()
		
		self._updateIotData(jsonStruct, spd)
		
		return spd
	
	def _formatDataAndLoadDictionary(self, jsonData: str, useDecForFloat: bool = False) -> dict:
		"""
		Helper method to format JSON string and load it into a dictionary.
		
		@param jsonData The JSON string to format and load.
		@param useDecForFloat If True, parse floats as Decimal.
		@return Dictionary representation of the JSON data.
		"""
		# Replace single quotes with double quotes and Python boolean format with JSON format
		jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		jsonStruct = None
		
		if useDecForFloat:
			jsonStruct = json.loads(jsonData, parse_float = Decimal)
		else:
			jsonStruct = json.loads(jsonData)
		
		return jsonStruct
	
	def _generateJsonData(self, obj, useDecForFloat: bool = False) -> str:
		"""
		Helper method to generate JSON string from an object.
		
		@param obj The object to convert to JSON.
		@param useDecForFloat If True, use Decimal for float values (currently not used in encoding).
		@return JSON string representation of the object.
		"""
		jsonData = None
		
		if self.encodeToUtf8:
			jsonData = json.dumps(obj, cls = JsonDataEncoder).encode('utf8')
		else:
			jsonData = json.dumps(obj, cls = JsonDataEncoder, indent = 4)
		
		if jsonData:
			jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
		
		return jsonData
	
	def _updateIotData(self, jsonStruct, obj):
		"""
		Helper method to update data object attributes from JSON structure.
		
		@param jsonStruct The JSON dictionary structure.
		@param obj The data object to update.
		"""
		varStruct = vars(obj)
		
		for key in jsonStruct:
			if key in varStruct:
				setattr(obj, key, jsonStruct[key])
			else:
				logging.warn("JSON data contains key not mappable to object: %s", key)

class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		"""
		Override default method to return object's dictionary representation.
		
		@param o The object to encode.
		@return Dictionary representation of the object.
		"""
		return o.__dict__