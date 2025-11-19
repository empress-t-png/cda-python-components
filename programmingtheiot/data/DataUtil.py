

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
        """
        Convert SensorData to JSON string
        
        Args:
            data: SensorData instance
            
        Returns:
            JSON string representation
        """
        if data:
            return json.dumps(self._sensorDataToDict(data))
        return None
    
    def _sensorDataToDict(self, data: SensorData) -> dict:
        """
        Convert SensorData to dictionary
        
        Args:
            data: SensorData instance
            
        Returns:
            Dictionary representation
        """
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
            
            # Only add value if it's not None
            if data.getValue() is not None:
                data_dict["value"] = data.getValue()
                
            return data_dict
        return None
    
    def jsonToSensorData(self, jsonData: str) -> SensorData:
        """
        Convert JSON string to SensorData
        
        Args:
            jsonData: JSON string
            
        Returns:
            SensorData instance
        """
        if jsonData:
            try:
                data_dict = json.loads(jsonData)
                sensor_data = SensorData()
                
                # Set properties from dictionary
                if "name" in data_dict:
                    sensor_data.setName(data_dict["name"])
                if "value" in data_dict:
                    sensor_data.setValue(data_dict["value"])
                if "timeStamp" in data_dict:
                    sensor_data.setTimeStamp(data_dict["timeStamp"])
                if "typeID" in data_dict:
                    sensor_data.setTypeID(data_dict["typeID"])
                if "locationID" in data_dict:
                    sensor_data.setLocationID(data_dict["locationID"])
                    
                return sensor_data
            except Exception as e:
                logging.error(f"Error converting JSON to SensorData: {e}")
        return None

# Example usage when run directly
if __name__ == "__main__":
    util = DataUtil()
    
    # Test SensorData conversion
    sensor = SensorData()
    sensor.setName("TestSensor")
    sensor.setValue(25.5)
    sensor.setTypeID(1)
    
    json_str = util.sensorDataToJson(sensor)
    print(f"SensorData JSON: {json_str}")
    
    # Test converting back
    sensor_back = util.jsonToSensorData(json_str)
    print(f"Converted back - Name: {sensor_back.getName()}, Value: {sensor_back.getValue()}")
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
        """
        Convert SensorData to JSON string
        
        Args:
            data: SensorData instance
            
        Returns:
            JSON string representation
        """
        if data:
            return json.dumps(self._sensorDataToDict(data))
        return None
    
    def _sensorDataToDict(self, data: SensorData) -> dict:
        """
        Convert SensorData to dictionary
        
        Args:
            data: SensorData instance
            
        Returns:
            Dictionary representation
        """
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
            
            # Only add value if it's not None
            if data.getValue() is not None:
                data_dict["value"] = data.getValue()
                
            return data_dict
        return None
    
    def jsonToSensorData(self, jsonData: str) -> SensorData:
        """
        Convert JSON string to SensorData
        
        Args:
            jsonData: JSON string
            
        Returns:
            SensorData instance
        """
        if jsonData:
            try:
                data_dict = json.loads(jsonData)
                sensor_data = SensorData()
                
                # Set properties from dictionary
                if "name" in data_dict:
                    sensor_data.setName(data_dict["name"])
                if "value" in data_dict:
                    sensor_data.setValue(data_dict["value"])
                if "timeStamp" in data_dict:
                    sensor_data.setTimeStamp(data_dict["timeStamp"])
                if "typeID" in data_dict:
                    sensor_data.setTypeID(data_dict["typeID"])
                if "locationID" in data_dict:
                    sensor_data.setLocationID(data_dict["locationID"])
                    
                return sensor_data
            except Exception as e:
                logging.error(f"Error converting JSON to SensorData: {e}")
        return None

# Example usage when run directly
if __name__ == "__main__":
    util = DataUtil()
    
    # Test SensorData conversion
    sensor = SensorData()
    sensor.setName("TestSensor")
    sensor.setValue(25.5)
    sensor.setTypeID(1)
    
    json_str = util.sensorDataToJson(sensor)
    print(f"SensorData JSON: {json_str}")
    
    # Test converting back
    sensor_back = util.jsonToSensorData(json_str)
    print(f"Converted back - Name: {sensor_back.getName()}, Value: {sensor_back.getValue()}")


