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
    def __init__(self):
        self.configUtil = ConfigUtil()
        self.dataUtil = DataUtil()

        self.enableSystemPerf = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SYSTEM_PERF_KEY)
        self.enableSensing = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSING_KEY)
        self.enableActuation = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_ACTUATION_KEY)

        self.sysPerfMgr = None
        self.sensorAdapterMgr = None
        self.actuatorAdapterMgr = None

        self.enableMqttClient = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_MQTT_CLIENT_KEY)
        self.mqttClient = None

        if self.enableMqttClient:
            self.mqttClient = MqttClientConnector()
            self.mqttClient.setDataMessageListener(self)
            logging.info("MQTT client enabled")

        self.enableCoapClient = self.configUtil.getBoolean(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.ENABLE_COAP_KEY, False)
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

        self.handleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
        self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
        self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)

        self.lastKnownTemp = None
        self.isHeatingActive = False
        self.isCoolingActive = False

    def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
        if data:
            logging.info("Processing actuator command message.")
            return self.actuatorAdapterMgr.sendActuatorCommand(data)
        else:
            logging.warning("Received invalid ActuatorData command message. Ignoring.")
            return None

    def handleActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
        if data:
            logging.debug("Incoming actuator response received (from actuator manager): " + str(data))
            return True
        else:
            logging.warning("Incoming actuator response is invalid (null). Ignoring.")
            return False

    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        logging.info("Incoming message received: " + str(resourceEnum))
        return True

    def handleSensorMessage(self, data: SensorData = None) -> bool:
        if data:
            logging.info("Incoming sensor data received (from sensor manager): " + str(data))
            self._handleSensorDataAnalysis(data=data)
            jsonData = self.dataUtil.sensorDataToJson(data=data)
            self._handleUpstreamTransmission(resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg=jsonData)
            return True
        else:
            logging.warning("Incoming sensor data is invalid (null). Ignoring.")
            return False

    def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
        if data:
            logging.info("Incoming system performance message received (from sys perf manager): " + str(data))
            jsonData = self.dataUtil.systemPerformanceDataToJson(data=data)
            self._handleUpstreamTransmission(resource=ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, msg=jsonData)
            return True
        else:
            logging.warning("Incoming system performance data is invalid (null). Ignoring.")
            return False

    def startManager(self):
        logging.info("Starting DeviceDataManager...")
        if self.sysPerfMgr: self.sysPerfMgr.startManager()
        if self.sensorAdapterMgr: self.sensorAdapterMgr.startManager()
        if self.mqttClient:
            self.mqttClient.connectClient()
            logging.info("MQTT client connected")
        if self.enableCoapClient and self.coapClient:
            logging.info("CoAP client ready for requests")
        logging.info("Started DeviceDataManager.")

    def stopManager(self):
        logging.info("Stopping DeviceDataManager...")
        if self.sysPerfMgr: self.sysPerfMgr.stopManager()
        if self.sensorAdapterMgr: self.sensorAdapterMgr.stopManager()
        if self.mqttClient:
            self.mqttClient.disconnectClient()
            logging.info("MQTT client disconnected")
        if self.enableCoapClient and self.coapClient:
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

            shouldTriggerActuation = False
            ad = ActuatorData()
            ad.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)

            if currentTemp > self.triggerHvacTempCeiling:
                if not self.isCoolingActive:
                    logging.info(f"Temperature {currentTemp}°C crossed ABOVE ceiling {self.triggerHvacTempCeiling}°C - activating cooling")
                    ad.setCommand(ConfigConst.COMMAND_ON)
                    ad.setValue(self.triggerHvacTempCeiling)
                    ad.setName("HVAC Cooling")
                    self.isCoolingActive = True
                    self.isHeatingActive = False
                    shouldTriggerActuation = True
            elif currentTemp < self.triggerHvacTempFloor:
                if not self.isHeatingActive:
                    logging.info(f"Temperature {currentTemp}°C crossed BELOW floor {self.triggerHvacTempFloor}°C - activating heating")
                    ad.setCommand(ConfigConst.COMMAND_ON)
                    ad.setValue(self.triggerHvacTempFloor)
                    ad.setName("HVAC Heating")
                    self.isHeatingActive = True
                    self.isCoolingActive = False
                    shouldTriggerActuation = True
            else:
                if self.isHeatingActive or self.isCoolingActive:
                    logging.info(f"Temperature {currentTemp}°C returned to normal range ({self.triggerHvacTempFloor}°C - {self.triggerHvacTempCeiling}°C) - deactivating HVAC")
                    ad.setCommand(ConfigConst.COMMAND_OFF)
                    ad.setName("HVAC Off")
                    self.isHeatingActive = False
                    self.isCoolingActive = False
                    shouldTriggerActuation = True

            if shouldTriggerActuation:
                logging.info(f"Triggering actuation: {ad.getName()} - Command: {ad.getCommand()}")
                self.handleActuatorCommandMessage(ad)

            self.lastKnownTemp = currentTemp

    def _handleIncomingDataAnalysis(self, msg: str):
        """
        Analyze incoming data message (placeholder for additional analytics).
        """
        logging.debug("Incoming data analysis: " + msg)

    def _handleUpstreamTransmission(self, resource = None, msg: str = None):
        """
        Handles upstream transmission of data to the GDA using MQTT or CoAP.
        """
        logging.info("Upstream transmission invoked. Checking comm's integration.")

        # MQTT publish
        if self.mqttClient:
            if self.mqttClient.publishMessage(resource=resource, msg=msg):
                logging.debug("Published incoming data to resource (MQTT): %s", str(resource))
            else:
                logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resource))

        # CoAP PUT (optional)
        if self.enableCoapClient and self.coapClient:
            if self.coapClient.sendPutRequest(resource=resource, payload=msg):
                logging.debug("Put incoming message data to resource (CoAP): %s", str(resource))
            else:
                logging.warning("Failed to put incoming message data to resource (CoAP): %s", str(resource))
