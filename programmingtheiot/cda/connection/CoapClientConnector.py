"""
This module provides CoAP client connectivity using the CoAPthon3 library.

"""

import logging

from coapthon.client.helperclient import HelperClient

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient

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
		
		logging.info("CoAP client configured for host: %s, port: %d", self.host, self.port)
		
		self._initClient()
	
	def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		"""
		Sends a discovery request to the CoAP server.
		
		"""
		logging.info("Discovering remote resources at URL: %s", self.url)
		
		try:
			client = HelperClient(server=(self.host, self.port))
			response = client.discover()
			
			if response:
				logging.info("Discovery response: %s", response)
				return True
			else:
				logging.warning("No discovery response received.")
				return False
		except Exception as e:
			logging.warning("Failed to discover resources: %s", str(e))
			return False
	
	def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		"""
		Sends a DELETE request to the CoAP server.
		
		"""
		if not resource:
			logging.warning("No resource specified for DELETE request.")
			return False
		
		resourcePath = resource.getResourceName()
		url = self.url + resourcePath
		
		logging.info("Sending DELETE request to URL: %s", url)
		
		try:
			client = HelperClient(server=(self.host, self.port))
			response = client.delete(resourcePath)
			
			if response:
				logging.info("DELETE response: %s", response.pretty_print())
				return True
			else:
				logging.warning("No DELETE response received.")
				return False
		except Exception as e:
			logging.warning("Failed to send DELETE request: %s", str(e))
			return False
	
	def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		"""
		Sends a GET request to the CoAP server.
		
		"""
		if not resource:
			logging.warning("No resource specified for GET request.")
			return False
		
		resourcePath = resource.getResourceName()
		url = self.url + resourcePath
		
		logging.info("Sending GET request to URL: %s", url)
		
		try:
			client = HelperClient(server=(self.host, self.port))
			response = client.get(resourcePath)
			
			if response:
				logging.info("GET response: %s", response.pretty_print())
				
				# Pass payload to listener if available
				if self.dataMsgListener and response.payload:
					self.dataMsgListener.handleIncomingMessage(resource, response.payload)
				
				return True
			else:
				logging.warning("No GET response received.")
				return False
		except Exception as e:
			logging.warning("Failed to send GET request: %s", str(e))
			return False
	
	def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		"""
		Sends a POST request to the CoAP server.
		
		"""
		if not resource:
			logging.warning("No resource specified for POST request.")
			return False
		
		resourcePath = resource.getResourceName()
		url = self.url + resourcePath
		
		logging.info("Sending POST request to URL: %s with payload: %s", url, payload)
		
		try:
			client = HelperClient(server=(self.host, self.port))
			response = client.post(resourcePath, payload)
			
			if response:
				logging.info("POST response: %s", response.pretty_print())
				return True
			else:
				logging.warning("No POST response received.")
				return False
		except Exception as e:
			logging.warning("Failed to send POST request: %s", str(e))
			return False
	
	def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		"""
		Sends a PUT request to the CoAP server.
		
		"""
		if not resource:
			logging.warning("No resource specified for PUT request.")
			return False
		
		resourcePath = resource.getResourceName()
		url = self.url + resourcePath
		
		logging.info("Sending PUT request to URL: %s with payload: %s", url, payload)
		
		try:
			client = HelperClient(server=(self.host, self.port))
			response = client.put(resourcePath, payload)
			
			if response:
				logging.info("PUT response: %s", response.pretty_print())
				return True
			else:
				logging.warning("No PUT response received.")
				return False
		except Exception as e:
			logging.warning("Failed to send PUT request: %s", str(e))
			return False
	
	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		"""
		Sets the data message listener.
		
		"""
		if listener:
			self.dataMsgListener = listener
			return True
		return False
	
	def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
		"""
		Starts observing a resource on the CoAP server.
		
		"""
		# TODO: Implement OBSERVE functionality in a future lab
		logging.info("OBSERVE functionality not yet implemented.")
		return False
	
	def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
		"""
		Stops observing a resource on the CoAP server.
		
		"""
		# TODO: Implement OBSERVE functionality in a future lab
		logging.info("OBSERVE functionality not yet implemented.")
		return False
	
	def _initClient(self):
		"""
		Initializes the CoAP client.
		
		"""
		logging.info("CoAP client initialized for URL: %s", self.url)
