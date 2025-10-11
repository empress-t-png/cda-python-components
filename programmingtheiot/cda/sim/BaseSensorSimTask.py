#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class BaseSensorSimTask():
    """
    Base class for simulated sensor tasks.
    """
    
    def __init__(self, name: str = "BaseSensorSimTask", typeID: int = 0, dataSet = None, minVal: float = 0.0, maxVal: float = 1000.0):
        self.name = name
        self.typeID = typeID
        self.dataSet = dataSet
        self.dataGenerator = SensorDataGenerator()
        self.latestSensorData = None
        
        if self.dataSet is not None:
            self.dataGenerator.enableRandomness = False
            self.useDataSet = True
        else:
            self.dataGenerator.enableRandomness = True
            self.useDataSet = False
            
        logging.info("Initialized sensor simulation task: " + self.name)
    
    def generateTelemetry(self) -> SensorData:
        """
        Generates telemetry data and returns a SensorData object.
        """
        sensorData = SensorData(name=self.name, typeID=self.typeID)
        sensorVal = self.getTelemetryValue()
        sensorData.setValue(sensorVal)
        
        self.latestSensorData = sensorData
        
        logging.debug("Generated sensor data: %s", sensorData)
        
        return sensorData
    
    def getTelemetryValue(self) -> float:
        """
        Generates and returns the telemetry value based on sensor type.
        """
        if self.typeID == ConfigConst.TEMP_SENSOR_TYPE:
            return self.dataGenerator.generateTemperature()
        elif self.typeID == ConfigConst.HUMIDITY_SENSOR_TYPE:
            return self.dataGenerator.generateHumidity()
        elif self.typeID == ConfigConst.PRESSURE_SENSOR_TYPE:
            return self.dataGenerator.generatePressure()
        else:
            return 0.0
