#!/usr/bin/env python3

import logging
import sys
import os
import json

# Add the project root to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData

logging.basicConfig(level=logging.INFO)

def test_put_functionality():
    """Test PUT functionality with both CON and NON requests"""
    
    print("=== Testing CoAP PUT Functionality ===")
    
    # Create CoAP client
    coap_client = CoapClientConnector()
    print("✓ CoAP client created successfully")
    
    # Create test sensor data and convert to JSON manually
    sensor_data = SensorData()
    sensor_data.value = 23.5
    sensor_data.name = "TestSensor"
    
    # Convert to JSON manually
    json_data = json.dumps({
        "name": sensor_data.name,
        "value": sensor_data.value,
        "typeID": sensor_data.typeID,
        "timeStamp": str(sensor_data.timeStamp)
    })
    
    print(f"Test payload: {json_data}")
    
    # Test 1: PUT with CONFIRMABLE request
    print("\n1. Testing PUT with CONFIRMABLE request...")
    try:
        success_con = coap_client.sendPutRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            enableCON=True,
            payload=json_data,
            timeout=5
        )
        print(f"   PUT CON result: {success_con}")
    except Exception as e:
        print(f"   PUT CON failed: {e}")
    
    # Test 2: PUT with NON-CONFIRMABLE request  
    print("\n2. Testing PUT with NON-CONFIRMABLE request...")
    try:
        success_non = coap_client.sendPutRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            enableCON=False,
            payload=json_data,
            timeout=5
        )
        print(f"   PUT NON result: {success_non}")
    except Exception as e:
        print(f"   PUT NON failed: {e}")
    
    print("\n=== PUT Functionality Test Completed ===")
    print("Note: These tests require a CoAP server running on localhost:5683")

if __name__ == "__main__":
    test_put_functionality()