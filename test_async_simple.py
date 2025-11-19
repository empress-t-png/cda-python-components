"""
Simple test for AsyncCoapClientConnector
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AsyncCoapClientConnector import AsyncCoapClientConnector

async def test_async_client_basic():
    """Test basic functionality of the async client"""
    print("=== Testing AsyncCoapClientConnector Basic Functionality ===")
    
    # Test with a public CoAP server
    client = AsyncCoapClientConnector(base_url="coap://coap.me", timeout=10)
    
    try:
        print("1. Testing connection...")
        await client.connect()
        print("✓ Connected successfully")
        
        print("2. Testing resource discovery...")
        resources = await client.discover_resources()
        print(f"✓ Discovered {len(resources)} resources")
        
        print("3. Testing GET request...")
        response = await client.get("/test")
        print(f"✓ GET response: {response.code} - {response.text[:50]}...")
        
        print("4. Testing POST request...")
        response = await client.post("/test", {"message": "test from async client"})
        print(f"✓ POST response: {response.code}")
        
        print("✓ All basic tests passed!")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
    finally:
        await client.disconnect()

async def test_async_with_local():
    """Test with local server (will fail if no server running)"""
    print("\n=== Testing AsyncCoapClientConnector with Local Server ===")
    
    client = AsyncCoapClientConnector(base_url="coap://localhost:5683", timeout=5)
    
    try:
        print("Testing ping to local server...")
        is_alive = await client.ping()
        if is_alive:
            print("✓ Local CoAP server is running!")
            
            # Test with your CDA resource paths
            test_paths = [
                "/PIOT/ConstrainedDevice/SensorMsg",
                "/.well-known/core",
                "/system/info"
            ]
            
            for path in test_paths:
                try:
                    response = await client.get(path)
                    print(f"✓ GET {path}: {response.code}")
                except Exception as e:
                    print(f"✗ GET {path} failed: {e}")
        else:
            print("✗ No local CoAP server running on localhost:5683")
            
    except Exception as e:
        print(f"✗ Local server test failed: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    # Test with public server (should work)
    asyncio.run(test_async_client_basic())
    
    # Test with local server (will fail if no server running)
    asyncio.run(test_async_with_local())