"""
DataUtil.py - Utility class for data conversion between objects and JSON
"""

import json
import logging
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil:
    """
    Utility class for converting between data objects and JSON representations
    """
    
    def __init__(self):
        logging.info("Created DataUtil instance.")
    
    def sensorDataToJson(self, data: SensorData) -> str:
        if data:
            return json.dumps(self._sensorDataToDict(data))
        return None
    
    def _sensorDataToDict(self, data: SensorData) -> dict:
        if data:
            data_dict = {
                "name": data.getName(),
                "typeID": data.getTypeID(),
                "timeStamp": data.getTimeStamp(),
                "statusCode": data.getStatusCode(),
                "locationID": data.getLocationID(),
                "latitude": data.getLatitude(),
                "longitude": data.getLongitude(),
                "elevation": data.getElevation()
            }
            if data.getValue() is not None:
                data_dict["value"] = data.getValue()
            return data_dict
        return None
    
    def jsonToSensorData(self, jsonData: str) -> SensorData:
        if jsonData:
            try:
                data_dict = json.loads(jsonData)
                sensor_data = SensorData()
                if "name" in data_dict:
                    sensor_data.setName(data_dict["name"])
                if "value" in data_dict:
                    sensor_data.setValue(data_dict["value"])
                if "timeStamp" in data_dict:
                    # FIX: SensorData has no setTime(), assign directly
                    sensor_data.timeStamp = data_dict["timeStamp"]
                if "typeID" in data_dict:
                    sensor_data.setTypeID(data_dict["typeID"])
                if "locationID" in data_dict:
                    sensor_data.setLocationID(data_dict["locationID"])
                return sensor_data
            except Exception as e:
                logging.error(f"Error converting JSON to SensorData: {e}")
        return None
    
    def actuatorDataToJson(self, data: ActuatorData) -> str:
        if data:
            logging.debug(f"Encoding ActuatorData to JSON [pre]  --> {data}")
            json_str = json.dumps(self._actuatorDataToDict(data), indent=4)
            logging.info(f"Encoding ActuatorData to JSON [post] --> {json_str}")
            return json_str
        return None
    
    def _actuatorDataToDict(self, data: ActuatorData) -> dict:
        if data:
            data_dict = {
                "timeStamp": str(data.getTimeStamp()),
                "name": data.getName(),
                "hasError": data.hasError,
                "statusCode": data.getStatusCode(),
                "isResponse": data.isResponseFlagEnabled(),
                "actuatorType": data.getTypeID(),
                "command": data.getCommand(),
                "stateData": data.getStateData(),
                "curValue": data.getValue()
            }
            return data_dict
        return None
    
    def jsonToActuatorData(self, jsonData: str) -> ActuatorData:
        if jsonData:
            try:
                logging.debug(f"Decoding ActuatorData from JSON [pre]  --> {jsonData}")
                data_dict = json.loads(jsonData)
                actuator_data = ActuatorData()
                if "name" in data_dict:
                    actuator_data.setName(data_dict["name"])
                if "actuatorType" in data_dict or "typeID" in data_dict:
                    type_id = data_dict.get("actuatorType", data_dict.get("typeID"))
                    actuator_data.setTypeID(type_id)
                if "command" in data_dict:
                    actuator_data.setCommand(data_dict["command"])
                if "stateData" in data_dict:
                    actuator_data.setStateData(data_dict["stateData"])
                if "curValue" in data_dict or "value" in data_dict:
                    value = data_dict.get("curValue", data_dict.get("value"))
                    actuator_data.setValue(value)
                if "timeStamp" in data_dict:
                    # FIX: ActuatorData has no setTime(), assign directly
                    actuator_data.timeStamp = data_dict["timeStamp"]
                if "locationID" in data_dict:
                    actuator_data.setLocationID(data_dict["locationID"])
                if "statusCode" in data_dict:
                    actuator_data.setStatusCode(data_dict["statusCode"])
                if "isResponse" in data_dict and data_dict["isResponse"]:
                    actuator_data.setAsResponse()
                logging.debug(f"Decoding ActuatorData from JSON [post] --> {actuator_data}")
                return actuator_data
            except Exception as e:
                logging.exception(f"Error converting JSON to ActuatorData: {e}")
        return None

    def systemPerformanceDataToJson(self, data: SystemPerformanceData) -> str:
        if data:
            return json.dumps(self._systemPerformanceDataToDict(data))
        return None
    
    def _systemPerformanceDataToDict(self, data: SystemPerformanceData) -> dict:
        if data:
            data_dict = {
                "name": data.getName(),
                "typeID": data.getTypeID(),
                "timeStamp": data.getTimeStamp(),
                "statusCode": data.getStatusCode(),
                "locationID": data.getLocationID(),
                "cpuUtil": data.getCpuUtilization(),
                "memUtil": data.getMemoryUtilization()
            }
            return data_dict
        return None
