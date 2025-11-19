"""
This module provides CoAP client connectivity using the CoAPthon3 library.

"""

import logging

from coapthon.client.helperclient import HelperClient

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

class HandleActuatorEvent:
    """
    Handler class for actuator event responses from observed resources.
    """
    
    def __init__(self, 
            listener: IDataMessageListener = None, 
            resource: ResourceNameEnum = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,
            requests = None):
        
        self.listener = listener
        self.resource = resource
        self.observeRequests = requests
        
        if not self.resource:
            self.resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
            
    def handleActuatorResponse(self, response):
        """
        Handle actuator response from observed resource.
        
        Args:
            response: The CoAP response containing actuator data
        """
        if response:
            jsonData = response.payload
            
            if self.observeRequests is not None:
                self.observeRequests[self.resource] = response
            
            logging.info(f"Received actuator command response to resource {self.resource}: {jsonData}")
            
            if self.listener:
                try:
                    data = DataUtil().jsonToActuatorData(jsonData = jsonData)
                    self.listener.handleActuatorCommandMessage(data = data)

                except Exception as e:
                    logging.warning(f"Failed to decode actuator data. Ignoring: {jsonData}")
                    logging.debug(f"Error details: {e}")


class CoapClientConnector(IRequestResponseClient):
    """
    CoAP client implementation using CoAPthon3 library.
    
    """
    
    def __init__(self):
        """
        Constructor.
        
        """
        self.config = ConfigUtil()
        self.dataMsgListener = None
        
        self.host = self.config.getProperty(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
        self.port = self.config.getInteger(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_COAP_PORT)
        
        self.url = "coap://" + self.host + ":" + str(self.port) + "/"
        
        logging.info("CoAP client configured for host: %s, port: %d" % (self.host, self.port))
        
        self._initClient()
    
    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a discovery request to the CoAP server.
        
        """
        logging.info("Discovering remote resources at URL: %s" % self.url)
        
        try:
            client = HelperClient(server=(self.host, self.port))
            response = client.discover()
            
            if response:
                logging.info("Discovery response: %s" % response.pretty_print())
                return True
            else:
                logging.warning("No discovery response received.")
                return False
                
        except Exception as e:
            logging.warning("Failed to discover resources: %s" % str(e))
            return False
    
    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a DELETE request to the CoAP server.
        
        """
        logging.info("DELETE functionality not yet implemented.")
        return False
    
    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a GET request to the CoAP server.
        
        """
        logging.info("GET functionality not yet implemented.")
        return False
    
    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a POST request to the CoAP server.
        
        """
        logging.info("POST functionality not yet implemented.")
        return False
    
    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Sends a PUT request to the CoAP server.
        
        """
        logging.info("PUT functionality not yet implemented.")
        return False
    
    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        """
        Sets the data message listener instance.
        
        """
        if listener:
            self.dataMsgListener = listener
            return True
        
        return False
    
    def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        """
        Starts observing a resource on the CoAP server.
        
        Args:
            resource: The resource to observe
            name: Additional name for the resource path
            ttl: Time to live for the observation
            
        Returns:
            bool: True if observation started successfully, False otherwise
        """
        if resource or name:
            if resource in self.observeRequests:
                logging.warning(f"Already observing resource {resource}. Ignoring start observe request.")
                return False
            
            self.observeRequests[resource] = None
            
            resourcePath = self._createResourcePath(resource, name)
            
            observeActuatorCmdHandler = \
                HandleActuatorEvent( \
                    listener = self.dataMsgListener, resource = resource, requests = self.observeRequests)
            
            try:
                self.coapClient.observe(path = resourcePath, callback = observeActuatorCmdHandler.handleActuatorResponse)
                logging.info(f"Started observing resource: {resourcePath}")
                return True
                
            except Exception as e:
                logging.warning(f"Failed to observe path: {resourcePath}. Error: {e}")
                return False
        else:
            logging.warning("Can't start observation - no resource provided.")
            return False
    
    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Stops observing a resource on the CoAP server.
        
        Args:
            resource: The resource to stop observing
            name: Additional name for the resource path
            timeout: Timeout for the stop operation
            
        Returns:
            bool: True if observation stopped successfully, False otherwise
        """
        if resource or name:
            if not resource in self.observeRequests:
                logging.warning(f"Resource {resource} not being observed. Ignoring stop observe request.")
                return False
            
            response = self.observeRequests[resource]
            
            if response:
                logging.info(f"Cancelling observe for resource {resource}.")
                
                try:
                    self.coapClient.cancel_observing(response = response, send_rst = True)
                    
                    del self.observeRequests[resource]
                    
                    logging.info(f"Cancelled observe for resource {resource}.")
                    return True

                except Exception as e:
                    logging.warning(f"Failed to cancel observe for resource {resource}. Error: {e}")
                    return False
            else:
                logging.warning(f"No response yet for observed resource {resource}. Attempting to stop anyway.")
                
                try:
                    self.coapClient.cancel_observing(response = None, send_rst = True)
                    
                    if resource in self.observeRequests:
                        del self.observeRequests[resource]
                        
                    logging.info(f"Canceled observe for resource {resource}.")
                    return True

                except Exception as e:
                    logging.warning(f"Failed to cancel observe for resource {resource}. Error: {e}")
                    return False
        else:
            logging.warning("Can't stop observation - no resource provided.")
            return False
    
    def _initClient(self):
        """
        Initializes the CoAP client.
        
        """
        self.coapClient = HelperClient(server=(self.host, self.port))
        self.observeRequests = {}
        logging.info("CoAP client initialized for URL: %s" % self.url)
    
    def _createResourcePath(self, resource: ResourceNameEnum, name: str = None) -> str:
        """
        Creates a resource path from the given resource and name.
        
        """
        if not resource:
            return ""
        
        resourcePath = resource.value
        
        if name:
            resourcePath = resourcePath + "/" + name
            
        return resourcePath
