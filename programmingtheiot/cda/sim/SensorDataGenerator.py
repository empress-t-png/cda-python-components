#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import logging
import random

class SensorDataGenerator():
    """
    Generates simulated sensor data with configurable ranges and patterns.
    """
    
    # Temperature constants (Celsius)
    LOW_NORMAL_INDOOR_TEMP = 18.0
    HI_NORMAL_INDOOR_TEMP = 24.0
    
    # Humidity constants (percentage)
    LOW_NORMAL_ENV_HUMIDITY = 30.0
    HI_NORMAL_ENV_HUMIDITY = 70.0
    
    # Pressure constants (kPa)
    LOW_NORMAL_ENV_PRESSURE = 990.0
    HI_NORMAL_ENV_PRESSURE = 1010.0
    
    def __init__(self):
        self.enableRandomness = True
        self.useSeconds = False
        
        # Temperature settings (Celsius)
        self.minTemperature = self.LOW_NORMAL_INDOOR_TEMP
        self.maxTemperature = self.HI_NORMAL_INDOOR_TEMP
        
        # Humidity settings (percentage)
        self.minHumidity = self.LOW_NORMAL_ENV_HUMIDITY
        self.maxHumidity = self.HI_NORMAL_ENV_HUMIDITY
        
        # Pressure settings (kPa)
        self.minPressure = self.LOW_NORMAL_ENV_PRESSURE
        self.maxPressure = self.HI_NORMAL_ENV_PRESSURE
        
        self.curTempVal = self.minTemperature
        self.curHumidityVal = self.minHumidity
        self.curPressureVal = self.minPressure
        
    def generateTelemetry(self, minVal: float, maxVal: float, curVal: float) -> float:
        """
        Generates a telemetry value within the specified range.
        """
        newVal = curVal
        
        if self.enableRandomness:
            newVal = random.uniform(minVal, maxVal)
        else:
            increment = 0.1
            newVal = curVal + increment
            
            if newVal > maxVal:
                newVal = minVal
                
        return newVal
    
    def generateTemperature(self) -> float:
        """
        Generates simulated temperature data.
        """
        self.curTempVal = self.generateTelemetry(
            self.minTemperature, 
            self.maxTemperature, 
            self.curTempVal
        )
        return self.curTempVal
    
    def generateHumidity(self) -> float:
        """
        Generates simulated humidity data.
        """
        self.curHumidityVal = self.generateTelemetry(
            self.minHumidity, 
            self.maxHumidity, 
            self.curHumidityVal
        )
        return self.curHumidityVal
    
    def generatePressure(self) -> float:
        """
        Generates simulated pressure data.
        """
        self.curPressureVal = self.generateTelemetry(
            self.minPressure, 
            self.maxPressure, 
            self.curPressureVal
        )
        return self.curPressureVal