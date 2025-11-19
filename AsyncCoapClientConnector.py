"""
AsyncCoapClientConnector.py
Asynchronous CoAP client connector for constrained devices and IoT applications.
"""

import asyncio
import logging
import traceback
from typing import Optional, Dict, Any, Union, List
import json
import aiocoap
from aiocoap import Message, Code, CONTENT, CHANGED, DELETED, BAD_REQUEST, NOT_FOUND
import urllib.parse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoAPResponse:
    """Wrapper for CoAP response data"""
    
    def __init__(self, code: Code, payload: bytes, content_format: Optional[int] = None):
        self.code = code
        self.payload = payload
        self.content_format = content_format
        self.success = code.is_successful()
    
    @property
    def text(self) -> str:
        """Return payload as text"""
        return self.payload.decode('utf-8') if self.payload else ""
    
    def json(self) -> Any:
        """Return payload as JSON"""
        return json.loads(self.text) if self.payload else None
    
    def __str__(self) -> str:
        return f"CoAPResponse(code={self.code}, payload={self.payload[:50] if self.payload else 'None'}...)"


class AsyncCoapClientConnector:
    """
    Asynchronous CoAP client connector for communicating with CoAP servers.
    Supports GET, POST, PUT, DELETE operations with various payload formats.
    """
    
    # Common CoAP content formats
    CONTENT_FORMAT_JSON = 50
    CONTENT_FORMAT_TEXT = 0
    CONTENT_FORMAT_CBOR = 60
    CONTENT_FORMAT_LINK = 40
    
    def __init__(self, base_url: Optional[str] = None, timeout: int = 30):
        """
        Initialize the CoAP client connector.
        
        Args:
            base_url: Base URL for CoAP server (e.g., 'coap://localhost:5683')
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or "coap://localhost:5683"  # Default base URL
        self.timeout = timeout
        self.protocol: Optional[aiocoap.protocol.Context] = None
        self._connected = False
        
    async def connect(self) -> None:
        """Establish async CoAP connection"""
        if not self._connected:
            try:
                self.protocol = await aiocoap.Context.create_client_context()
                self._connected = True
                logger.info("CoAP client connected successfully")
            except Exception as e:
                logger.error(f"Failed to connect CoAP client: {e}")
                raise
    
    async def disconnect(self) -> None:
        """Close CoAP connection"""
        if self.protocol and self._connected:
            if hasattr(self.protocol, 'shutdown'):
                # Properly await the shutdown if it's a coroutine
                shutdown_method = self.protocol.shutdown()
                if asyncio.iscoroutine(shutdown_method):
                    await shutdown_method
                else:
                    self.protocol.shutdown()
            self._connected = False
            logger.info("CoAP client disconnected")
    
    def sendPostRequest(self, resource: str = None, name: str = None, 
                       enableCON: bool = False, payload: str = None, 
                       timeout: int = 30) -> bool:
        """
        Send POST request to CoAP server
        
        Args:
            resource: Resource path
            name: Additional path detail
            enableCON: True for CONFIRMABLE, False for NONCONFIRMABLE
            payload: The payload to send to the server
            timeout: Request timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if resource or name:
            resource_path = self._createResourcePath(resource, name)
            
            logger.info(f"Issuing Async POST to path: {resource_path}")
            
            # Run the async request in the current event loop
            try:
                result = asyncio.run(
                    self._handlePostRequest(resource_path, payload, enableCON, timeout)
                )
                return result
            except Exception as e:
                logger.error(f"Failed to execute async POST request: {e}")
                return False
        else:
            logger.warning("Can't issue Async POST - no path provided.")
            return False
    
    async def _handlePostRequest(self, resource_path: str = None, payload: str = None, 
                               enableCON: bool = False, timeout: int = 30):
        """
        Handle async POST request
        
        Args:
            resource_path: Full resource path
            payload: Payload to send
            enableCON: True for CONFIRMABLE, False for NONCONFIRMABLE
            timeout: Request timeout
        """
        try:
            # Build complete URI with scheme
            uri_and_resource_path = await self._build_uri(resource_path)
            
            # Create message
            payload_bytes = payload.encode("utf-8") if payload else b''
            
            # Create message - aiocoap handles CON/NON automatically based on context
            # For explicit control, we can use request() with observe option
            msg = Message(code=Code.POST, payload=payload_bytes, uri=uri_and_resource_path)
            
            # Ensure connected
            if not self._connected:
                await self.connect()
            
            # Send request with timeout
            # Note: aiocoap handles message types automatically based on the request
            # CON is used by default for reliable delivery
            request = self.protocol.request(msg)
            
            # For NONCONFIRMABLE, we can set the request to be non-confirmable
            if not enableCON:
                request.non_timeout = 0  # This makes it NONCONFIRMABLE
            
            response = await asyncio.wait_for(
                request.response,
                timeout=timeout
            )
            
            self._onPostResponse(response)
            return True
            
        except asyncio.TimeoutError:
            logger.error(f"Async POST request timed out after {timeout} seconds")
            return False
        except Exception as e:
            logger.warning(f"Failed to process Async POST request for path: {resource_path}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    def _onPostResponse(self, response):
        """
        Handle POST response
        
        Args:
            response: Response from CoAP server
        """
        if not response:
            logger.warning("Async POST response invalid. Ignoring.")
            return
        
        logger.info("Async POST response received.")
        
        response_data = response.payload.decode("utf-8") if response.payload else ""
        
        logger.info(f"Response data received. Payload: {response_data}")
    
    def _createResourcePath(self, resource: str, name: str = None) -> str:
        """
        Create resource path from resource and name
        
        Args:
            resource: Base resource path
            name: Additional path component
            
        Returns:
            Complete resource path
        """
        if name:
            return f"{resource}/{name}"
        return resource
    
    async def _build_uri(self, path: str) -> str:
        """Build complete CoAP URI"""
        if self.base_url:
            if path.startswith('/'):
                path = path[1:]
            # Ensure the URI has the scheme
            if not path.startswith('coap://'):
                return f"{self.base_url}/{path}"
            return path
        # If no base_url, ensure path has scheme
        if not path.startswith('coap://'):
            return f"coap://{path}"
        return path
    
    async def get(self, path: str, 
                 accept_format: Optional[int] = None,
                 **query_params) -> CoAPResponse:
        """
        Perform async GET request.
        """
        uri = await self._build_uri(path)
        if query_params:
            query_string = urllib.parse.urlencode(query_params)
            uri = f"{uri}?{query_string}"
        
        if not self._connected:
            await self.connect()
        
        try:
            response = await asyncio.wait_for(
                self.protocol.request(Message(code=Code.GET, uri=uri)).response,
                timeout=self.timeout
            )
            
            return CoAPResponse(
                code=response.code,
                payload=response.payload,
                content_format=response.opt.content_format
            )
            
        except asyncio.TimeoutError:
            logger.error(f"CoAP request timed out after {self.timeout} seconds")
            raise
        except Exception as e:
            logger.error(f"CoAP request failed: {e}")
            raise
    
    async def post(self, path: str, 
                  data: Union[bytes, str, Dict, List],
                  content_format: Optional[int] = None,
                  **query_params) -> CoAPResponse:
        """
        Alternative POST method for simpler usage
        """
        uri = await self._build_uri(path)
        if query_params:
            query_string = urllib.parse.urlencode(query_params)
            uri = f"{uri}?{query_string}"
        
        payload = await self._prepare_payload(data, content_format)
        
        if content_format is None and isinstance(data, (dict, list)):
            content_format = self.CONTENT_FORMAT_JSON
        
        if not self._connected:
            await self.connect()
        
        try:
            message = Message(code=Code.POST, uri=uri, payload=payload)
            if content_format is not None and payload:
                message.opt.content_format = content_format
            
            response = await asyncio.wait_for(
                self.protocol.request(message).response,
                timeout=self.timeout
            )
            
            return CoAPResponse(
                code=response.code,
                payload=response.payload,
                content_format=response.opt.content_format
            )
            
        except asyncio.TimeoutError:
            logger.error(f"CoAP request timed out after {self.timeout} seconds")
            raise
        except Exception as e:
            logger.error(f"CoAP request failed: {e}")
            raise
    
    async def _prepare_payload(self, data: Union[bytes, str, Dict, List], 
                             content_format: Optional[int]) -> bytes:
        """Convert data to bytes based on content format"""
        if data is None:
            return b''
        
        try:
            if isinstance(data, bytes):
                return data
            elif isinstance(data, str):
                return data.encode('utf-8')
            elif isinstance(data, (dict, list)):
                return json.dumps(data).encode('utf-8')
            else:
                return str(data).encode('utf-8')
        except Exception as e:
            logger.error(f"Failed to prepare payload: {e}")
            return b''
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()


# Example usage and testing
async def main():
    """Test the async POST functionality"""
    
    async with AsyncCoapClientConnector(base_url="coap://coap.me") as client:
        try:
            # Test POST with CONFIRMABLE
            result_con = client.sendPostRequest(
                resource="test",
                payload='{"message": "test CON"}',
                enableCON=True,
                timeout=10
            )
            print(f"POST CON result: {result_con}")
            
            # Test POST with NONCONFIRMABLE
            result_non = client.sendPostRequest(
                resource="test", 
                payload='{"message": "test NON"}',
                enableCON=False,
                timeout=10
            )
            print(f"POST NON result: {result_non}")
            
        except Exception as e:
            print(f"Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())