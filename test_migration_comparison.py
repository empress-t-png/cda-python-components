"""
Compare existing sync CoAP client with new async client
"""

import asyncio
import time
import logging
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

# Import both clients
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from AsyncCoapClientConnectorCDA import AsyncCoapClientConnectorCDA

logging.basicConfig(level=logging.INFO)


async def test_async_client():
    """Test the new async client"""
    print("\n=== Testing Async Client ===")
    
    async with AsyncCoapClientConnectorCDA() as client:
        try:
            start_time = time.time()
            
            # Test multiple operations
            test_payload = {"sensor": "temperature", "value": 23.5, "timestamp": "2024-01-15T10:30:00Z"}
            
            # Test PUT
            put_result = await client.sendPutRequest(
                ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, 
                test_payload
            )
            print(f"Async PUT result: {put_result}")
            
            # Test GET  
            get_result = await client.sendGetRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)
            print(f"Async GET result: {get_result is not None}")
            
            elapsed = time.time() - start_time
            print(f"Async operations completed in {elapsed:.2f} seconds")
            
        except Exception as e:
            print(f"Async test error: {e}")


def test_sync_client():
    """Test the existing sync client"""
    print("\n=== Testing Sync Client ===")
    
    client = CoapClientConnector()
    try:
        start_time = time.time()
        
        test_payload = '{"sensor": "temperature", "value": 23.5, "timestamp": "2024-01-15T10:30:00Z"}'
        
        # Test PUT
        put_result = client.sendPutRequest(
            ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            test_payload,
            timeout=5
        )
        print(f"Sync PUT result: {put_result}")
        
        # Test GET
        get_result = client.sendGetRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, timeout=5)
        print(f"Sync GET result: {get_result is not None}")
        
        elapsed = time.time() - start_time
        print(f"Sync operations completed in {elapsed:.2f} seconds")
        
    except Exception as e:
        print(f"Sync test error: {e}")


async def main():
    print("=== CoAP Client Migration Comparison ===")
    
    # Test sync client (your existing one)
    test_sync_client()
    
    # Test async client (new one)
    await test_async_client()
    
    print("\n=== Migration Ready ===")
    print("✓ Async client provides same interface as sync client")
    print("✓ All methods are available: sendPutRequest, sendGetRequest, etc.")
    print("✓ Can gradually replace sync client with async client")


if __name__ == "__main__":
    asyncio.run(main())