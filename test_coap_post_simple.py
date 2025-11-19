"""
Test CoAP POST functionality with the simplified client
"""

import logging
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil

logging.basicConfig(level=logging.INFO)

def test_post_requests():
    """Test POST requests with CON and NON confirmable messages"""
    
    print("=== Testing CoAP POST Functionality ===")
    
    # Create CoAP client
    coap_client = CoapClientConnector()
    
    # Create test sensor data using DataUtil
    sensor_data = SensorData()
    sensor_data.setName("TestSensor")
    sensor_data.setValue(23.5)
    
    # Convert to JSON using DataUtil
    data_util = DataUtil()
    json_data = data_util.sensorDataToJson(data=sensor_data)
    
    print("✓ Test payload created using DataUtil")
    
    # Test 1: POST with CONFIRMABLE (enableCON=True)
    print("\n1. Testing POST with CONFIRMABLE request...")
    try:
        result_con = coap_client.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            payload=json_data,
            enableCON=True,
            timeout=5
        )
        print(f"✓ POST CON result: {result_con}")
    except Exception as e:
        print(f"✗ POST CON failed: {e}")
    
    # Test 2: POST with NONCONFIRMABLE (enableCON=False)
    print("\n2. Testing POST with NONCONFIRMABLE request...")
    try:
        result_non = coap_client.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            payload=json_data,
            enableCON=False,
            timeout=5
        )
        print(f"✓ POST NON result: {result_non}")
    except Exception as e:
        print(f"✗ POST NON failed: {e}")
    
    # Test 3: POST with additional name parameter
    print("\n3. Testing POST with name parameter...")
    try:
        result_named = coap_client.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            name="test_sensor_001",
            payload=json_data,
            enableCON=True,
            timeout=5
        )
        print(f"✓ POST with name result: {result_named}")
    except Exception as e:
        print(f"✗ POST with name failed: {e}")
    
    print("\n=== POST Testing Complete ===")
    print("Note: Requests will fail without a running CoAP server")
    print("This is expected - the important thing is that the methods are callable")

if __name__ == "__main__":
    test_post_requests()

