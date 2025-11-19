"""
AsyncCoapClientConnector.py
Asynchronous CoAP client connector for constrained devices and IoT applications.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, Union, List
from aiocoap import Context, Message, Code, NON, CON

class AsyncCoapClientConnector:
    """Asynchronous CoAP client connector using aiocoap library."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.client_context = None
        self._connected = False
        
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
        
        Args:
            resource: The resource path
            name: Additional name to append to resource path  
            enableCON: If True, use CONFIRMABLE request; else NONCONFIRMABLE
            timeout: Timeout for the request
            
        Returns:
            bool: True if request was successful, False otherwise
        """
        if resource or name:
            resource_path = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing Async DELETE to path: {resource_path}")
            
            # Run the async request
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
        """
        Handle async DELETE request.
        
        Args:
            resource_path: Full resource path
            enableCON: True for CONFIRMABLE, False for NONCONFIRMABLE
            timeout: Request timeout
            
        Returns:
            bool: Success status
        """
        try:
            if not self.client_context:
                await self.connect()
            
            # Build complete URI
            full_uri = await self._build_uri(resource_path)
            
            # Set message type
            msg_type = CON if enableCON else NON
            
            # Create DELETE request
            request = Message(code=Code.DELETE, uri=full_uri, mtype=msg_type)
            
            logging.info(f"Sending DELETE request to: {full_uri}")
            logging.info(f"Message type: {'CONFIRMABLE' if enableCON else 'NONCONFIRMABLE'}")
            
            # Send request and await response
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
        """
        Handle DELETE response.
        
        Args:
            response: Response from CoAP server
        """
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
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

# Example usage and testing
async def main():
    """Test the async DELETE functionality"""
    
    async with AsyncCoapClientConnector(base_url="coap://coap.me") as client:
        try:
            # Test DELETE with CONFIRMABLE
            result_con = client.sendDeleteRequest(
                resource="test",
                enableCON=True,
                timeout=10
            )
            print(f"DELETE CON result: {result_con}")
            
            # Test DELETE with NONCONFIRMABLE
            result_non = client.sendDeleteRequest(
                resource="test", 
                enableCON=False,
                timeout=10
            )
            print(f"DELETE NON result: {result_non}")
            
        except Exception as e:
            print(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
