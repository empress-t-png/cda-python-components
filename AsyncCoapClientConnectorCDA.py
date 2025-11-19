"""
AsyncCoapClientConnectorCDA.py
Drop-in async replacement for CoapClientConnector in CDA
"""

import asyncio
import logging
from typing import Optional, Union
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from AsyncCoapClientConnector import AsyncCoapClientConnector

logger = logging.getLogger(__name__)


class AsyncCoapClientConnectorCDA:
    """
    Async CoAP client connector that matches the CDA CoapClientConnector interface
    but uses async/await internally.
    """
    
    def __init__(self):
        """Initialize the async CoAP client with CDA configuration"""
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the async CoAP client"""
        # You can modify these to match your CDA config
        host = "localhost"
        port = 5683
        timeout = 30
        
        base_url = f"coap://{host}:{port}"
        self.client = AsyncCoapClientConnector(base_url=base_url, timeout=timeout)
        
        logger.info(f"Async CoAP Client configured for {base_url}")
    
    async def sendPutRequest(self, 
                           resource: ResourceNameEnum, 
                           payload: Union[str, dict],
                           timeout: int = None) -> bool:
        """
        Async version of sendPutRequest - matches existing CDA interface
        
        Args:
            resource: ResourceNameEnum specifying the resource path
            payload: Data to send (string or dict)
            timeout: Request timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert ResourceNameEnum to path string
            resource_path = self._get_resource_path(resource)
            
            # Prepare payload
            if isinstance(payload, str):
                # If it's already a string, use as-is
                data_to_send = payload
            else:
                # Convert to JSON string if it's a dict
                import json
                data_to_send = json.dumps(payload)
            
            # Use the async client
            response = await self.client.put(resource_path, data_to_send)
            
            if response.success:
                logger.info(f"PUT request successful for {resource_path}: {response.code}")
                return True
            else:
                logger.warning(f"PUT request failed for {resource_path}: {response.code}")
                return False
                
        except Exception as e:
            logger.error(f"Error in sendPutRequest for {resource}: {e}")
            return False
    
    async def sendGetRequest(self, 
                           resource: ResourceNameEnum,
                           timeout: int = None) -> Optional[str]:
        """
        Async version of sendGetRequest
        
        Args:
            resource: ResourceNameEnum specifying the resource path
            timeout: Request timeout in seconds
            
        Returns:
            Response payload as string, or None if failed
        """
        try:
            resource_path = self._get_resource_path(resource)
            response = await self.client.get(resource_path)
            
            if response.success:
                logger.info(f"GET request successful for {resource_path}: {response.code}")
                return response.text
            else:
                logger.warning(f"GET request failed for {resource_path}: {response.code}")
                return None
                
        except Exception as e:
            logger.error(f"Error in sendGetRequest for {resource}: {e}")
            return None
    
    async def sendPostRequest(self, 
                            resource: ResourceNameEnum,
                            payload: Union[str, dict],
                            timeout: int = None) -> bool:
        """
        Async version of sendPostRequest
        
        Args:
            resource: ResourceNameEnum specifying the resource path
            payload: Data to send (string or dict)
            timeout: Request timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            resource_path = self._get_resource_path(resource)
            
            if isinstance(payload, str):
                data_to_send = payload
            else:
                import json
                data_to_send = json.dumps(payload)
            
            response = await self.client.post(resource_path, data_to_send)
            
            if response.success:
                logger.info(f"POST request successful for {resource_path}: {response.code}")
                return True
            else:
                logger.warning(f"POST request failed for {resource_path}: {response.code}")
                return False
                
        except Exception as e:
            logger.error(f"Error in sendPostRequest for {resource}: {e}")
            return False
    
    async def sendDeleteRequest(self, 
                              resource: ResourceNameEnum,
                              timeout: int = None) -> bool:
        """
        Async version of sendDeleteRequest
        
        Args:
            resource: ResourceNameEnum specifying the resource path
            timeout: Request timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            resource_path = self._get_resource_path(resource)
            response = await self.client.delete(resource_path)
            
            if response.success:
                logger.info(f"DELETE request successful for {resource_path}: {response.code}")
                return True
            else:
                logger.warning(f"DELETE request failed for {resource_path}: {response.code}")
                return False
                
        except Exception as e:
            logger.error(f"Error in sendDeleteRequest for {resource}: {e}")
            return False
    
    def _get_resource_path(self, resource: ResourceNameEnum) -> str:
        """
        Convert ResourceNameEnum to actual resource path
        
        Args:
            resource: ResourceNameEnum value
            
        Returns:
            Resource path as string
        """
        # Map ResourceNameEnum to actual CoAP resource paths used in CDA
        resource_map = {
            ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE: "PIOT/ConstrainedDevice/SensorMsg",
            ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE: "PIOT/ConstrainedDevice/ActuatorCmd",
            ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE: "PIOT/ConstrainedDevice/ActuatorResponse",
            ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE: "PIOT/ConstrainedDevice/MgmtStatusMsg",
            ResourceNameEnum.CDA_MGMT_STATUS_CMD_RESOURCE: "PIOT/ConstrainedDevice/MgmtStatusCmd",
            ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE: "PIOT/ConstrainedDevice/SystemPerfMsg",
            ResourceNameEnum.CDA_REGISTRATION_REQUEST_RESOURCE: "PIOT/ConstrainedDevice/RegistrationRequest",
            ResourceNameEnum.CDA_UPDATE_NOTIFICATIONS_RESOURCE: "PIOT/ConstrainedDevice/UpdateNotifications",
        }
        
        # Return the mapped path
        if resource in resource_map:
            return resource_map[resource]
        else:
            # Fallback: convert enum name to path by removing "CDA_" and "RESOURCE", then convert to path
            enum_name = str(resource).split('.')[-1]  # Get just the enum value name
            # Remove CDA_ and _RESOURCE, then convert to path
            path_name = enum_name.replace('CDA_', '').replace('_RESOURCE', '')
            return f"PIOT/ConstrainedDevice/{path_name}"
    
    async def connect(self):
        """Connect to CoAP server"""
        if self.client:
            await self.client.connect()
    
    async def disconnect(self):
        """Disconnect from CoAP server"""
        if self.client:
            await self.client.disconnect()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()


# Test all available resources
async def test_all_resources():
    """Test all available ResourceNameEnum values"""
    import logging
    logging.basicConfig(level=logging.INFO)

    print("=== Testing All ResourceNameEnum Values ===")
    
    # Get all ResourceNameEnum values
    resources = [
        ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
        ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,
        ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE,
        ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE,
        ResourceNameEnum.CDA_MGMT_STATUS_CMD_RESOURCE,
        ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE,
        ResourceNameEnum.CDA_REGISTRATION_REQUEST_RESOURCE,
        ResourceNameEnum.CDA_UPDATE_NOTIFICATIONS_RESOURCE,
    ]
    
    async with AsyncCoapClientConnectorCDA() as client:
        for resource in resources:
            try:
                resource_path = client._get_resource_path(resource)
                print(f"\nTesting {resource} -> {resource_path}")
                
                # Test PUT with this resource
                test_data = {"test": "data", "resource": str(resource)}
                result = await client.sendPutRequest(resource, test_data)
                print(f"  PUT result: {result}")
                
            except Exception as e:
                print(f"  Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_all_resources())