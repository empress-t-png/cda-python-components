#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
    """
    Central manager for device data coordination.
    """
    
    def __init__(self):
        self.configUtil = ConfigUtil()
        self.dataUtil = DataUtil()
        self.enableSystemPerf = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.ENABLE_SYSTEM_PERF_KEY)
        
        self.enableSensing = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.ENABLE_SENSING_KEY)
        
        # Temporarily disable actuation to avoid emulator issues
        self.enableActuation = False
        
        self.sysPerfMgr = None
        self.sensorAdapterMgr = None
        self.actuatorAdapterMgr = None
        
        self.enableMqttClient = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE,
                key=ConfigConst.ENABLE_MQTT_CLIENT_KEY)
        
        self.mqttClient = None
        
        if self.enableMqttClient:
            self.mqttClient = MqttClientConnector()
            self.mqttClient.setDataMessageListener(self)
            logging.info("MQTT client enabled")
        
        # CoAP client configuration
        self.enableCoapClient = self.configUtil.getBoolean(
            ConfigConst.COAP_GATEWAY_SERVICE,
            ConfigConst.ENABLE_COAP_KEY,
            False
        )

        self.coapClient = None

        if self.enableCoapClient:
            try:
                self.coapClient = CoapClientConnector()
                logging.info("CoAP client connector created")
            except Exception as e:
                logging.error(f"Failed to create CoAP client: {e}")
        
        if self.enableSystemPerf:
            self.sysPerfMgr = SystemPerformanceManager()
            self.sysPerfMgr.setDataMessageListener(self)
            logging.info("Local system performance tracking enabled")
        
        if self.enableSensing:
            self.sensorAdapterMgr = SensorAdapterManager()
            self.sensorAdapterMgr.setDataMessageListener(self)
            logging.info("Local sensor tracking enabled")
        
        if self.enableActuation:
            try:
                self.actuatorAdapterMgr = ActuatorAdapterManager()
                self.actuatorAdapterMgr.setDataMessageListener(self)
                logging.info("Local actuation capabilities enabled")
            except Exception as e:
                logging.error(f"Failed to initialize actuator manager: {e}")
                self.actuatorAdapterMgr = None
        
        self.handleTempChangeOnDevice = \
            self.configUtil.getBoolean(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
        
        self.triggerHvacTempFloor = \
            self.configUtil.getFloat(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
        
        self.triggerHvacTempCeiling = \
            self.configUtil.getFloat(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)
    
    def _sendCoapRequest(self, resource: str, data: str = None) -> bool:
        """
        Send data via CoAP to the gateway device
        """
        if not self.coapClient:
            logging.warning("CoAP client not enabled or initialized")
            return False
        
        try:
            import asyncio
            from aiocoap import Code
            success = asyncio.run(
               self.coapClient.sendPostRequest(resource=resource, payload=data)
            )
            
            if success:
                logging.debug(f"CoAP request successful for resource: {resource}")
            else:
                logging.warning(f"CoAP request failed for resource: {resource}")
                
            return success
            
        except Exception as e:
            logging.error(f"CoAP transmission error for {resource}: {e}")
            return False
    
    def handleActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
        """
        Handle actuator command message.
        """
        logging.info("Actuator data: " + str(data))
        
        if data:
            logging.info("Processing actuator command message.")
            if self.actuatorAdapterMgr:
                return self.actuatorAdapterMgr.sendActuatorCommand(data)
            else:
                logging.warning("Actuator manager not available")
                return None
        else:
            logging.warning("Incoming actuator command is invalid (null). Ignoring.")
            return None
    
    def handleActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
        """
        Handle actuator command response.
        """
        if data:
            logging.debug("Incoming actuator response received (from actuator manager): " + str(data))
            return True
        else:
            logging.warning("Incoming actuator response is invalid (null). Ignoring.")
            return False
    
    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Handle incoming message.
        """
        logging.info("Incoming message received: " + str(resourceEnum))
        return True
    
    def handleSensorMessage(self, data: SensorData = None) -> bool:
        """
        Handle sensor message.
        """
        if data:
            logging.debug("Incoming sensor data received (from sensor manager): " + str(data))
            
            # Send sensor data via CoAP if enabled
            if self.enableCoapClient and self.coapClient:
                json_data = self.dataUtil.sensorDataToJson(data)
                resource_name = ""
               
                # Determine resource based on sensor type
                if hasattr(data, 'typeID'):
                    if data.typeID == ConfigConst.TEMP_SENSOR_TYPE:
                        resource_name = ConfigConst.TEMPERATURE_RESOURCE
                    elif data.typeID == ConfigConst.HUMIDITY_SENSOR_TYPE:
                        resource_name = ConfigConst.HUMIDITY_RESOURCE
                    elif data.typeID == ConfigConst.PRESSURE_SENSOR_TYPE:
                        resource_name = ConfigConst.PRESSURE_RESOURCE
                
                if resource_name:
                    logging.debug(f"Upstream CoAP transmission: {resource_name}")
                    self._sendCoapRequest(resource_name, json_data)
            
            self._handleSensorDataAnalysis(data=data)
            return True
        else:
            logging.warning("Incoming sensor data is invalid (null). Ignoring.")
            return False
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
        """
        Handle system performance message.
        """
        if data:
            logging.debug("Incoming system performance message received (from sys perf manager): " + str(data))
            
            # Send system performance data via CoAP if enabled
            if self.enableCoapClient and self.coapClient:
                json_data = self.dataUtil.systemPerformanceDataToJson(data)
                logging.debug("Upstream CoAP transmission: systemperf")
                self._sendCoapRequest(ConfigConst.SYSTEM_PERF_RESOURCE, json_data)
            
            return True
        else:
            logging.warning("Incoming system performance data is invalid (null). Ignoring.")
            return False
    
    def startManager(self):
        """
        Start the device data manager.
        """
        logging.info("Starting DeviceDataManager...")
        
        if self.sysPerfMgr:
            self.sysPerfMgr.startManager()
        
        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.startManager()
        
        if self.mqttClient:
            self.mqttClient.connectClient()
            logging.info("MQTT client connected")
        
        if self.coapClient:
            # CoAP client is connectionless, just log that it's ready
            logging.info("CoAP client ready for requests")
        
        logging.info("Started DeviceDataManager.")
    
    def stopManager(self):
        """
        Stop the device data manager.
        """
        logging.info("Stopping DeviceDataManager...")
        
        if self.sysPerfMgr:
            self.sysPerfMgr.stopManager()
        
        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.stopManager()
        
        if self.mqttClient:
            self.mqttClient.disconnectClient()
            logging.info("MQTT client disconnected")
        
        if self.coapClient:
            try:
                self.coapClient.disconnectClient()
                logging.info("CoAP client disconnected")
            except Exception as e:
                logging.error(f"Error disconnecting CoAP client: {e}")
        
        logging.info("Stopped DeviceDataManager.")
    
    def _handleSensorDataAnalysis(self, data: SensorData = None):
        """
        Analyze sensor data and trigger actuation if needed.
        """
        if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
            logging.info("Handle temp change: %s - type ID: %s", str(self.handleTempChangeOnDevice), str(data.getTypeID()))
            
            ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
            
            if data.getValue() > self.triggerHvacTempCeiling:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempCeiling)
            elif data.getValue() < self.triggerHvacTempFloor:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempFloor)
            else:
                ad.setCommand(ConfigConst.COMMAND_OFF)
            
            self.handleActuatorCommandMessage(ad)
    
    def _handleIncomingDataAnalysis(self, msg: str):
        """
        Analyze incoming data message.
        """
        logging.debug("Incoming data analysis: " + msg)
    
    def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
        """
        Handle upstream transmission.
        """
        logging.debug("Upstream transmission: " + str(resourceName))
