#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import logging
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class BaseSensorSimTask():
    """
    Base class for simulated sensor tasks.
    """
    
    def __init__(self, name: str = "BaseSensorSimTask", typeID: int = 0, dataSet = None):
        self.name = name
        self.typeID = typeID
        self.dataSet = dataSet
        self.generator = SensorDataGenerator()
        
        if self.dataSet is not None:
            self.generator.enableRandomness = False
            self.useDataSet = True
        else:
            self.generator.enableRandomness = True
            self.useDataSet = False
            
        logging.info("Initialized sensor simulation task: " + self.name)
    
    def generateTelemetry(self) -> SensorData:
        """
        Abstract method to be implemented by subclasses.
        Should return a SensorData object with simulated readings.
        """
        pass
    
    def getTelemetryValue(self) -> float:
        """
        Generates and returns the telemetry value.
        """
        if self.useDataSet:
            # Use predefined dataset if available
            return self.generator.generateTelemetry()
        else:
            # Generate random value based on sensor type
            if self.typeID == 1:  # Temperature
                return self.generator.generateTemperature()
            elif self.typeID == 2:  # Humidity
                return self.generator.generateHumidity()
            elif self.typeID == 3:  # Pressure
                return self.generator.generatePressure()
            else:
                return 0.0
