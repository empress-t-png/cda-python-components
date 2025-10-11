#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

class SensorDataGenerator():
    """
    Generates simulated sensor data with configurable ranges and patterns.
    """
    
    def __init__(self):
        self.enableRandomness = True
        self.useSeconds = False
        
        # Temperature settings (Celsius)
        self.minTemperature = 18.0
        self.maxTemperature = 24.0
        
        # Humidity settings (percentage)
        self.minHumidity = 30.0
        self.maxHumidity = 70.0
        
        # Pressure settings (kPa)
        self.minPressure = 990.0
        self.maxPressure = 1010.0
        
        self.curTempVal = self.minTemperature
        self.curHumidityVal = self.minHumidity
        self.curPressureVal = self.minPressure
        
    def generateTelemetry(self, minVal: float, maxVal: float, curVal: float) -> float:
        """
        Generates a telemetry value within the specified range.
        """
        newVal = curVal
        
        if self.enableRandomness:
            # Generate random value within range
            newVal = random.uniform(minVal, maxVal)
        else:
            # Increment value gradually
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





	

