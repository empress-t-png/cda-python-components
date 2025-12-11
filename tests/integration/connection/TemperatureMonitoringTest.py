"""
Integration test for Lab Module 12 Temperature Monitoring System
Tests the Smart Room Temperature Management functionality
"""

import unittest
import logging
from time import sleep

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst

class TemperatureMonitoringTest(unittest.TestCase):
    """
    Integration test for temperature-based HVAC control
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
        logging.info("Testing Lab Module 12 Temperature Monitoring System")
    
    def setUp(self):
        self.ddm = DeviceDataManager()
        
    def testTemperatureBelowThreshold(self):
        """
        Test HVAC activation when temperature falls below 20°C
        """
        logging.info("\n\n***** TemperatureMonitoringTest: Temperature Below Threshold *****")
        
        # Create sensor data with temp below threshold (< 20°C)
        sensorData = SensorData()
        sensorData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        sensorData.setValue(18.0)  # Below 20°C threshold
        sensorData.setName("TempSensor")
        
        # Send to DeviceDataManager
        result = self.ddm.handleSensorMessage(sensorData)
        
        self.assertTrue(result)
        logging.info("Successfully triggered HVAC for low temperature")
        
    def testTemperatureAboveThreshold(self):
        """
        Test HVAC activation when temperature exceeds 24°C
        """
        logging.info("\n\n***** TemperatureMonitoringTest: Temperature Above Threshold *****")
        
        # Create sensor data with temp above threshold (> 24°C)
        sensorData = SensorData()
        sensorData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        sensorData.setValue(26.0)  # Above 24°C threshold
        sensorData.setName("TempSensor")
        
        # Send to DeviceDataManager
        result = self.ddm.handleSensorMessage(sensorData)
        
        self.assertTrue(result)
        logging.info("Successfully triggered HVAC for high temperature")
        
    def testTemperatureWithinRange(self):
        """
        Test no HVAC activation when temperature is within 20-24°C range
        """
        logging.info("\n\n***** TemperatureMonitoringTest: Temperature Within Range *****")
        
        # Create sensor data within comfortable range
        sensorData = SensorData()
        sensorData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        sensorData.setValue(22.0)  # Within 20-24°C range
        sensorData.setName("TempSensor")
        
        # Send to DeviceDataManager
        result = self.ddm.handleSensorMessage(sensorData)
        
        self.assertTrue(result)
        logging.info("Temperature within range - no HVAC activation needed")

if __name__ == '__main__':
    unittest.main()
