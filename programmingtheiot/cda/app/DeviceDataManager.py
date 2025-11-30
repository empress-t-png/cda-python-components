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
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil

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
        
        # Track previous temperature state for threshold crossing detection
        self.lastKnownTemp = None
        self.isHeatingActive = False
        self.isCoolingActive = False
    
    def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
        """
        Callback function to handle an actuator command message packaged as a ActuatorData object.
        
        @param data The ActuatorData message received.
        @return ActuatorData The response from the actuator, or None if invalid.
        """
        if data:
            logging.info("Processing actuator command message.")
            
            # TODO: add further validation before sending the command
            return self.actuatorAdapterMgr.sendActuatorCommand(data)
        else:
            logging.warning("Received invalid ActuatorData command message. Ignoring.")
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
            logging.info("Incoming sensor data received (from sensor manager): " + str(data))
            
            # Perform sensor data analysis (threshold checking)
            self._handleSensorDataAnalysis(data=data)
            
            # Convert SensorData to JSON
            jsonData = self.dataUtil.sensorDataToJson(data=data)
            
            # Send to GDA via upstream transmission
            self._handleUpstreamTransmission(resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg=jsonData)
            
            return True
        else:
            logging.warning("Incoming sensor data is invalid (null). Ignoring.")
            return False
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
        """
        Handle system performance message.
        """
        if data:
            logging.info("Incoming system performance message received (from sys perf manager): " + str(data))
            
            # Convert SystemPerformanceData to JSON
            jsonData = self.dataUtil.systemPerformanceDataToJson(data=data)
            
            # Send to GDA via upstream transmission
            self._handleUpstreamTransmission(resource=ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, msg=jsonData)
            
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
        Only triggers actuation on threshold crossings, not on every reading.
        """
        if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
            currentTemp = data.getValue()
            
            # Determine if we need to trigger actuation based on threshold crossings
            shouldTriggerActuation = False
            ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
            
            # Check if temperature crossed ABOVE ceiling (need cooling)
            if currentTemp > self.triggerHvacTempCeiling:
                if not self.isCoolingActive:
                    # Temperature just crossed above ceiling
                    logging.info(f"Temperature {currentTemp}°C crossed ABOVE ceiling {self.triggerHvacTempCeiling}°C - activating cooling")
                    ad.setCommand(ConfigConst.COMMAND_ON)
                    ad.setValue(self.triggerHvacTempCeiling)
                    ad.setName("HVAC Cooling")
                    self.isCoolingActive = True
                    self.isHeatingActive = False
                    shouldTriggerActuation = True
            
            # Check if temperature crossed BELOW floor (need heating)
            elif currentTemp < self.triggerHvacTempFloor:
                if not self.isHeatingActive:
                    # Temperature just crossed below floor
                    logging.info(f"Temperature {currentTemp}°C crossed BELOW floor {self.triggerHvacTempFloor}°C - activating heating")
                    ad.setCommand(ConfigConst.COMMAND_ON)
                    ad.setValue(self.triggerHvacTempFloor)
                    ad.setName("HVAC Heating")
                    self.isHeatingActive = True
                    self.isCoolingActive = False
                    shouldTriggerActuation = True
            
            # Temperature is within acceptable range
            else:
                if self.isHeatingActive or self.isCoolingActive:
                    # Temperature returned to normal range
                    logging.info(f"Temperature {currentTemp}°C returned to normal range ({self.triggerHvacTempFloor}°C - {self.triggerHvacTempCeiling}°C) - deactivating HVAC")
                    ad.setCommand(ConfigConst.COMMAND_OFF)
                    ad.setName("HVAC Off")
                    self.isHeatingActive = False
                    self.isCoolingActive = False
                    shouldTriggerActuation = True
            
            # Only send actuation command if state changed
            if shouldTriggerActuation:
                logging.info(f"Triggering actuation: {ad.getName()} - Command: {ad.getCommand()}")
                self.handleActuatorCommandMessage(ad)
            
            # Update last known temperature
            self.lastKnownTemp = currentTemp
    
    def _handleIncomingDataAnalysis(self, msg: str):
        """
        Analyze incoming data message.
        """
        logging.debug("Incoming data analysis: " + msg)
    
    def _handleUpstreamTransmission(self, resource = None, msg: str = None):
        """
        Handles upstream transmission of data to the GDA using MQTT or CoAP.
        
        @param resource: The resource name (topic for MQTT, path for CoAP)
        @param msg: The message payload (JSON string)
        """
        logging.info("Upstream transmission invoked. Checking comm's integration.")
        
        # NOTE: If using MQTT, the following will attempt to publish the message to the broker
        if self.mqttClient:
            if self.mqttClient.publishMessage(resource = resource, msg = msg):
                logging.debug("Published incoming data to resource (MQTT): %s", str(resource))
            else:
                logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resource))
        
        # NOTE: If using CoAP, the following will attempt to PUT the message to the server
        if self.coapClient:
            if self.coapClient.sendPutRequest(resource = resource, payload = msg):
                logging.debug("Put incoming message data to resource (CoAP): %s", str(resource))
            else:
                logging.warning("Failed to put incoming message data to resource (CoAP): %s", str(resource))