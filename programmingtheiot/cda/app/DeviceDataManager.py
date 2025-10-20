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

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
    """
    Central manager for device data coordination.
    """
    
    def __init__(self):
        self.configUtil = ConfigUtil()
        
        self.enableSystemPerf = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.ENABLE_SYSTEM_PERF_KEY)
        
        self.enableSensing = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.ENABLE_SENSING_KEY)
        
        self.enableActuation = True
        
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
        self.coapClient = None
        self.coapServer = None
        
        if self.enableSystemPerf:
            self.sysPerfMgr = SystemPerformanceManager()
            self.sysPerfMgr.setDataMessageListener(self)
            logging.info("Local system performance tracking enabled")
        
        if self.enableSensing:
            self.sensorAdapterMgr = SensorAdapterManager()
            self.sensorAdapterMgr.setDataMessageListener(self)
            logging.info("Local sensor tracking enabled")
        
        if self.enableActuation:
            self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener=self)
            logging.info("Local actuation capabilities enabled")
        
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
    
    def handleActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
        """
        Handle actuator command message.
        """
        logging.info("Actuator data: " + str(data))
        
        if data:
            logging.info("Processing actuator command message.")
            return self.actuatorAdapterMgr.sendActuatorCommand(data)
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