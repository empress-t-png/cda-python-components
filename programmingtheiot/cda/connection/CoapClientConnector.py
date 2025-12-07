import logging
import asyncio

from aiocoap import *

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient
from programmingtheiot.data.DataUtil import DataUtil   # ✅ FIXED import path

class CoapClientConnector(IRequestResponseClient):
    """
    CoAP client connector for CDA.
    """
    
    def __init__(self):
        self.config = ConfigUtil()
        self.dataMsgListener = None
        
        self.host = self.config.getProperty(
            ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
        
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_COAP_PORT)
        
        self.url = "coap://" + self.host + ":" + str(self.port) + "/"
        logging.info("CoAP client configured for host: " + self.url)
    
    async def sendRequest(self, resource: str, payload: str = None, method: Code = Code.GET, observe: bool = False):
        try:
            protocol = await Context.create_client_context()
            uri = self.url + resource
            request = Message(code=method, uri=uri)
            
            if payload:
                request.payload = payload.encode('utf-8')
            if observe:
                request.opt.observe = 0
            
            logging.debug(f"Sending CoAP {method} request to: {uri} (observe={observe})")
            requester = protocol.request(request)
            
            if observe:
                async for response in requester.observation:
                    msg = response.payload.decode('utf-8')
                    logging.info(f"Received actuator command response to resource {resource}: {msg}")
                    if self.dataMsgListener:
                        self.dataMsgListener.handleIncomingMessage(msg)
            else:
                response = await requester.response
                if response.payload:
                    msg = response.payload.decode('utf-8')
                    if resource == ".well-known/core":
                        self._onDiscoveryResponse(response)
                    elif method == Code.PUT:
                        self._onPutResponse(response)
                    elif method == Code.POST:
                        self._onPostResponse(response)
                    elif method == Code.DELETE:
                        self._onDeleteResponse(response)
                    else:
                        self._onGetResponse(response, resource)
            return True
        except Exception as e:
            logging.error(f"CoAP request failed: {e}")
            return False
    
    def _createResourcePath(self, resource: ResourceNameEnum = None, name: str = None) -> str:
        resourcePath = ""
        if resource:
            resourcePath += resource.value
        if name:
            if resourcePath:
                resourcePath += "/"
            resourcePath += name
        return resourcePath
    
    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        logging.info("Sending CoAP discovery request")
        return asyncio.run(self.sendRequest(".well-known/core", method=Code.GET))
    
    def _onDiscoveryResponse(self, response):
        if not response or not response.payload:
            logging.warning("DISCOVERY response invalid. Ignoring.")
            return
        msg = response.payload.decode('utf-8')
        logging.info(f"DISCOVERY response received: {msg}")
    
    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None,
                          enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        resourcePath = self._createResourcePath(resource, name)
        logging.info(f"Sending CoAP DELETE request to: {resourcePath}")
        return asyncio.run(self.sendRequest(resourcePath, method=Code.DELETE))
    
    def _onDeleteResponse(self, response):
        if not response or not response.payload:
            logging.warning("DELETE response invalid. Ignoring.")
            return
        msg = response.payload.decode('utf-8')
        logging.info(f"DELETE response received: {msg}")
    
    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None,
                       enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        resourcePath = self._createResourcePath(resource, name)
        logging.info(f"Sending CoAP GET request to: {resourcePath}")
        return asyncio.run(self.sendRequest(resourcePath, method=Code.GET))
    
    def _onGetResponse(self, response, resourcePath: str = None):
        if not response or not response.payload:
            logging.warning("GET response invalid. Ignoring.")
            return
        msg = response.payload.decode('utf-8')
        logging.info(f"GET response from {resourcePath}: {msg}")
        try:
            ad = DataUtil().jsonToActuatorData(msg)
            if self.dataMsgListener:
                self.dataMsgListener.handleActuatorCommandMessage(ad)
        except Exception:
            logging.warning(f"Failed to decode actuator data. Payload: {msg}")
    
    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, payload: str = None,
                        enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        resourcePath = self._createResourcePath(resource, name)
        logging.info(f"Sending CoAP POST request to: {resourcePath}")
        logging.info(f"Payload: {payload}")
        return asyncio.run(self.sendRequest(resourcePath, payload, Code.POST))
    
    def _onPostResponse(self, response):
        if not response or not response.payload:
            logging.warning("POST response invalid. Ignoring.")
            return
        msg = response.payload.decode('utf-8')
        logging.info(f"POST response received: {msg}")
    
    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, payload: str = None,
                       enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        resourcePath = self._createResourcePath(resource, name)
        logging.info(f"Sending CoAP PUT request to: {resourcePath}")
        return asyncio.run(self.sendRequest(resourcePath, payload, Code.PUT))
    
    def _onPutResponse(self, response):
        if not response or not response.payload:
            logging.warning("PUT response invalid. Ignoring.")
            return
        msg = response.payload.decode('utf-8')
        logging.info(f"PUT response received: {msg}")
    
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        if listener:
            self.dataMsgListener = listener
            return True
        return False
    
    def sendObserveRequest(self, resource: ResourceNameEnum = None, name: str = None) -> bool:
        resourcePath = self._createResourcePath(resource, name)
        logging.info(f"Sending CoAP Observe request to: {resourcePath}")
        return asyncio.run(self.sendRequest(resourcePath, method=Code.GET, observe=True))
    
    def cancelObserveRequest(self, resource: ResourceNameEnum = None, name: str = None) -> bool:
        resourcePath = self._createResourcePath(resource, name)
        logging.info(f"Canceling CoAP Observe request for: {resourcePath}")
        # aiocoap doesn't expose a direct cancel here; typically handled by requester.observation.cancel()
        return True
