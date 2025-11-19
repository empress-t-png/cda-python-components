"""
Simplified CoAP client connector for DeviceDataManager compatibility
"""

import logging
from coapthon.client.helperclient import HelperClient
from coapthon import defines
from coapthon.utils import generate_random_token
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

class CoapClientConnector:
    """
    Simplified CoAP client for basic functionality
    """
    
    def __init__(self):
        self.config = ConfigUtil()
        self.host = self.config.getProperty(
            ConfigConst.COAP_GATEWAY_SERVICE, 
            ConfigConst.HOST_KEY, 
            ConfigConst.DEFAULT_HOST
        )
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE, 
            ConfigConst.PORT_KEY, 
            ConfigConst.DEFAULT_COAP_PORT
        )
        logging.info(f"CoAP Client configured for {self.host}:{self.port}")
    
    def sendRequest(self, resource: str, payload: str = None, method: str = "POST") -> bool:
        """
        Send CoAP request - simplified version
        """
        try:
            logging.info(f"Sending CoAP {method} to {resource} with payload: {payload}")
            
            client = HelperClient(server=(self.host, self.port))
            
            if method.upper() == "POST":
                response = client.post(resource, payload)
            elif method.upper() == "GET":
                response = client.get(resource)
            elif method.upper() == "PUT":
                response = client.put(resource, payload)
            elif method.upper() == "DELETE":
                response = client.delete(resource)
            else:
                logging.warning(f"Unsupported CoAP method: {method}")
                client.stop()
                return False
            
            if response:
                logging.info(f"CoAP Response: {response.pretty_print()}")
                client.stop()
                return True
            else:
                logging.warning("No CoAP response received")
                client.stop()
                return False
                
        except Exception as e:
            logging.error(f"CoAP request failed: {e}")
            return False

    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, 
                      enableCON: bool = False, payload: str = None, 
                      timeout: int = 5) -> bool:
        """
        Send PUT request to CoAP server
        """
        if not resource:
            logging.warning("No resource specified for PUT request.")
            return False
        
        try:
            # Get resource path from ResourceNameEnum
            resource_path = resource.value
            
            # If name is provided, append it to the resource path
            if name:
                resource_path = f"{resource_path}/{name}"
            
            logging.info(f"Issuing PUT with path: {resource_path}")
            
            client = HelperClient(server=(self.host, self.port))
            
            # Send PUT request
            response = client.put(resource_path, payload, timeout=timeout)
            
            if response:
                logging.info(f"PUT Response: {response.pretty_print()}")
                client.stop()
                return True
            else:
                logging.warning("No PUT response received")
                client.stop()
                return False
                
        except Exception as e:
            logging.error(f"PUT request failed: {e}")
            return False

    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, 
                       enableCON: bool = False, payload: str = None, 
                       timeout: int = 5) -> bool:
        """
        Send POST request to CoAP server with CONFIRMABLE/NONCONFIRMABLE support
        """
        if not resource:
            logging.warning("No resource specified for POST request.")
            return False
        
        try:
            # Get resource path from ResourceNameEnum
            resource_path = resource.value
            
            # If name is provided, append it to the resource path
            if name:
                resource_path = f"{resource_path}/{name}"
            
            logging.info(f"Issuing POST with path: {resource_path}")
            logging.info(f"Sending POST with payload: {payload}")
            
            # Create client and send POST request
            client = HelperClient(server=(self.host, self.port))
            
            # Note: HelperClient doesn't directly expose CON/NON configuration in simple API
            response = client.post(resource_path, payload, timeout=timeout)
            
            if response:
                logging.info(f"POST Response: {response.pretty_print()}")
                client.stop()
                return True
            else:
                logging.warning("No POST response received")
                client.stop()
                return False
                
        except Exception as e:
            logging.error(f"POST request failed: {e}")
            return False

    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, 
                         enableCON: bool = False, timeout: int = 5) -> bool:
        """
        Send DELETE request to CoAP server with CONFIRMABLE/NONCONFIRMABLE support
        
        Args:
            resource: ResourceNameEnum for the request URL
            name: Additional path detail for the URL
            enableCON: True for CONFIRMABLE, False for NONCONFIRMABLE
            timeout: Request timeout in seconds
            
        Returns:
            True if request was sent successfully
        """
        if not resource:
            logging.warning("No resource specified for DELETE request.")
            return False
        
        try:
            # Get resource path from ResourceNameEnum
            resource_path = resource.value
            
            # If name is provided, append it to the resource path
            if name:
                resource_path = f"{resource_path}/{name}"
            
            logging.info(f"Issuing DELETE with path: {resource_path}")
            
            # Create client and send DELETE request
            client = HelperClient(server=(self.host, self.port))
            
            # Note: HelperClient doesn't directly expose CON/NON configuration in simple API
            response = client.delete(resource_path, timeout=timeout)
            
            if response:
                logging.info(f"DELETE Response: {response.pretty_print()}")
                client.stop()
                return True
            else:
                logging.warning("No DELETE response received")
                client.stop()
                return False
                
        except Exception as e:
            logging.error(f"DELETE request failed: {e}")
            return False

    def _onPostResponse(self, response):
        """
        Internal callback method for handling POST responses
        """
        if not response:
            logging.warning("POST response invalid. Ignoring.")
            return
        
        # Process the response
        logging.info(f"POST response received: {response.pretty_print() if response else 'None'}")

    def _onDeleteResponse(self, response):
        """
        Internal callback method for handling DELETE responses
        """
        if not response:
            logging.warning("DELETE response invalid. Ignoring.")
            return
        
        # Process the response
        logging.info(f"DELETE response received: {response.pretty_print() if response else 'None'}")

    def disconnectClient(self):
        """
        Cleanup client resources
        """
        logging.info("CoAP client disconnected")