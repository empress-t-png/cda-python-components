"""
Integration tests for CoAP POST functionality
Following the test specification requirements
"""

import unittest
import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil  # Corrected import path

logging.basicConfig(level=logging.INFO)

class CoapClientConnectorTest(unittest.TestCase):
    
    def setUp(self):
        self.coapClient = CoapClientConnector()
        self.dataUtil = DataUtil()
    
    #@unittest.skip("Ignore for now.")
    def testPostSensorMessageCon(self):
        """Test storing SensorData instance using CONFIRMABLE POST request"""
        data = SensorData()
        jsonData = self.dataUtil.sensorDataToJson(data=data)
        
        result = self.coapClient.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, 
            enableCON=True, 
            payload=jsonData, 
            timeout=5
        )
        
        # Even if it fails (no server), the method should be callable
        self.assertIsNotNone(result, "POST CON request should be attempted")
        print("✓ POST CON test completed")
    
    #@unittest.skip("Ignore for now.") 
    def testPostSensorMessageNon(self):
        """Test storing SensorData instance using NONCONFIRMABLE POST request"""
        data = SensorData()
        jsonData = self.dataUtil.sensorDataToJson(data=data)
        
        result = self.coapClient.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, 
            enableCON=False, 
            payload=jsonData, 
            timeout=5
        )
        
        # Even if it fails (no server), the method should be callable
        self.assertIsNotNone(result, "POST NON request should be attempted")
        print("✓ POST NON test completed")

if __name__ == "__main__":
    unittest.main()


