"""
AsyncCoapClientConnector.py
Asynchronous CoAP client connector for constrained devices and IoT applications.
"""

import asyncio
import logging
from typing import Optional
from aiocoap import Context, Message, Code, NON, CON

class AsyncCoapClientConnector:
    """Asynchronous CoAP client connector using aiocoap library."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.client_context = None
        self._connected = False
        self._observer_task = None
        
    async def connect(self) -> None:
        """Establish async CoAP connection"""
        if not self._connected:
            self.client_context = await Context.create_client_context()
            self._connected = True
            logging.info("CoAP client connected")
    
    async def disconnect(self) -> None:
        """Close CoAP connection"""
        if self.client_context:
            await self.client_context.shutdown()
            self._connected = False
            logging.info("CoAP client disconnected")
    
    def sendDeleteRequest(self, resource: str = None, name: str = None, 
                         enableCON: bool = False, timeout: int = 30) -> bool:
        """
        Send DELETE request to CoAP server.
        """
        if resource or name:
            resource_path = self._createResourcePath(resource, name)
            logging.info(f"Issuing Async DELETE to path: {resource_path}")
            try:
                result = asyncio.run(
                    self._handleDeleteRequest(resource_path, enableCON, timeout)
                )
                return result
            except Exception as e:
                logging.error(f"Failed to execute async DELETE request: {e}")
                return False
        else:
            logging.warning("Can't issue Async DELETE - no path provided.")
            return False
    
    async def _handleDeleteRequest(self, resource_path: str = None, 
                                  enableCON: bool = False, timeout: int = 30) -> bool:
        """Handle async DELETE request."""
        try:
            if not self.client_context:
                await self.connect()
            
            full_uri = await self._build_uri(resource_path)
            msg_type = CON if enableCON else NON
            request = Message(code=Code.DELETE, uri=full_uri, mtype=msg_type)
            
            logging.info(f"Sending DELETE request to: {full_uri}")
            logging.info(f"Message type: {'CONFIRMABLE' if enableCON else 'NONCONFIRMABLE'}")
            
            response = await asyncio.wait_for(
                self.client_context.request(request).response,
                timeout=timeout
            )
            self._onDeleteResponse(response)
            return True
        except asyncio.TimeoutError:
            logging.error(f"Async DELETE request timed out after {timeout} seconds")
            return False
        except Exception as e:
            logging.error(f"DELETE request failed: {e}")
            return False
    
    def _onDeleteResponse(self, response):
        """Handle DELETE response."""
        if not response:
            logging.warning("Async DELETE response invalid. Ignoring.")
            return
        logging.info("Async DELETE response received.")
        response_data = response.payload.decode("utf-8") if response.payload else ""
        logging.info(f"Response data received. Payload: {response_data}")
    
    def _createResourcePath(self, resource: str, name: str = None) -> str:
        """Create resource path from resource and name"""
        if name:
            return f"{resource}/{name}"
        return resource
    
    async def _build_uri(self, path: str) -> str:
        """Build complete CoAP URI"""
        if self.base_url:
            return f"{self.base_url}/{path.lstrip('/')}"
        return f"coap://localhost/{path.lstrip('/')}"
    
    async def startObserver(self, resource: str):
        """
        Start a CoAP Observe request for the given resource.
        """
        try:
            if not self.client_context:
                await self.connect()
            
            full_uri = await self._build_uri(resource)
            request = Message(code=Code.GET, uri=full_uri, observe=0)
            logging.info(f"Starting CoAP Observe on resource: {full_uri}")
            
            protocol = self.client_context
            async def _observe():
                async for response in protocol.request(request).observation:
                    payload = response.payload.decode("utf-8")
                    logging.info(f"Observe notification received: {payload}")
            
            self._observer_task = asyncio.create_task(_observe())
        except Exception as e:
            logging.error(f"Failed to start observer: {e}")
    
    async def stopObserver(self):
        """
        Stop the CoAP Observe request if running.
        """
        if self._observer_task:
            self._observer_task.cancel()
            logging.info("CoAP observer stopped.")
            self._observer_task = None
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()


# ------------------ TEST CASES ------------------

import unittest

class CoapAsyncClientConnectorTest(unittest.TestCase):

    def setUp(self):
        self.coapClient = AsyncCoapClientConnector(base_url="coap://coap.me")

    def testDeleteSensorMessageCon(self):
        """DELETE SensorData with Confirmable request."""
        result = self.coapClient.sendDeleteRequest(
            resource="test",
            enableCON=True,
            timeout=5
        )
        self.assertTrue(result)

    def testDeleteSensorMessageNon(self):
        """DELETE SensorData with Non‑Confirmable request."""
        result = self.coapClient.sendDeleteRequest(
            resource="test",
            enableCON=False,
            timeout=5
        )
        self.assertTrue(result)


if __name__ == "__main__":
    # Run example usage
    async def main():
        async with AsyncCoapClientConnector(base_url="coap://coap.me") as client:
            try:
                result_con = client.sendDeleteRequest(resource="test", enableCON=True, timeout=10)
                print(f"DELETE CON result: {result_con}")
                result_non = client.sendDeleteRequest(resource="test", enableCON=False, timeout=10)
                print(f"DELETE NON result: {result_non}")
                # Example observe usage
                await client.startObserver("test")
                await asyncio.sleep(5)  # wait for notifications
                await client.stopObserver()
            except Exception as e:
                print(f"Test failed: {e}")

    asyncio.run(main())
    # Run unit tests
    unittest.main()
