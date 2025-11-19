"""
Test CoAP DELETE functionality
"""

import logging
import unittest
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

logging.basicConfig(level=logging.INFO)

class CoapClientConnectorTest(unittest.TestCase):
    
    def setUp(self):
        self.coapClient = CoapClientConnector()
    
    #@unittest.skip("Ignore for now.")
    def testDeleteSensorMessageCon(self):
        """Test DELETE with CONFIRMABLE request"""
        result = self.coapClient.sendDeleteRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, 
            enableCON=True, 
            timeout=5
        )
        
        self.assertIsNotNone(result, "DELETE CON request should be attempted")
        print("✓ DELETE CON test completed")
    
    #@unittest.skip("Ignore for now.") 
    def testDeleteSensorMessageNon(self):
        """Test DELETE with NONCONFIRMABLE request"""
        result = self.coapClient.sendDeleteRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, 
            enableCON=False, 
            timeout=5
        )
        
        self.assertIsNotNone(result, "DELETE NON request should be attempted")
        print("✓ DELETE NON test completed")

if __name__ == "__main__":
    unittest.main()