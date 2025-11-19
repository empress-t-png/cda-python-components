"""
Compare async vs sync CoAP client performance
"""

import asyncio
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AsyncCoapClientConnector import AsyncCoapClientConnector

async def test_async_performance():
    """Test async client with multiple concurrent requests"""
    print("=== Testing Async Client Performance ===")
    
    client = AsyncCoapClientConnector(base_url="coap://coap.me", timeout=10)
    
    start_time = time.time()
    
    try:
        # Make multiple concurrent requests
        tasks = [
            client.get("/test"),
            client.get("/hello"),
            client.get("/separate"),
            client.post("/test", {"test": "data"}),
            client.get("/validate")
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = 0
        for i, response in enumerate(responses):
            if not isinstance(response, Exception):
                print(f"Request {i+1}: {response.code}")
                successful += 1
            else:
                print(f"Request {i+1}: Failed - {response}")
        
        elapsed = time.time() - start_time
        print(f"✓ Completed {successful}/{len(tasks)} requests in {elapsed:.2f} seconds")
        
    except Exception as e:
        print(f"✗ Performance test failed: {e}")
    finally:
        await client.disconnect()

async def main():
    await test_async_performance()

if __name__ == "__main__":
    asyncio.run(main())