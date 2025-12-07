import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil

class MqttClientConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing MqttClientConnector class...")
        self.cfg = ConfigUtil()
        self.mcc = MqttClientConnector()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Test connect/disconnect
    def testConnectAndDisconnect(self):
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE,
                                    ConfigConst.KEEP_ALIVE_KEY,
                                    ConfigConst.DEFAULT_KEEP_ALIVE)
        self.mcc.connectClient()
        sleep(delay + 5)
        self.mcc.disconnectClient()

    # Test pub/sub for CDA management status
    def testConnectAndCDAManagementStatusPubSub(self):
        qos = 1
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE,
                                    ConfigConst.KEEP_ALIVE_KEY,
                                    ConfigConst.DEFAULT_KEEP_ALIVE)
        self.mcc.setDataMessageListener(DefaultDataMessageListener())
        self.mcc.connectClient()
        self.mcc.subscribeToTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE, qos=qos)
        sleep(5)
        self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE,
                                msg="TEST: This is the CDA message payload.", qos=qos)
        sleep(5)
        self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
        sleep(5)
        sleep(delay)
        self.mcc.disconnectClient()

    # Test actuator command pub/sub
    def testActuatorCmdPubSub(self):
        qos = 1
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE,
                                    ConfigConst.KEEP_ALIVE_KEY,
                                    ConfigConst.DEFAULT_KEEP_ALIVE)

        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.COMMAND_ON)
        actuatorData.setStateData("Test actuator command")

        payload = DataUtil().actuatorDataToJson(actuatorData)

        self.mcc.setDataMessageListener(DefaultDataMessageListener())
        self.mcc.connectClient()
        sleep(5)
        self.mcc.publishMessage(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,
                                msg=payload, qos=qos)
        sleep(delay)
        self.mcc.disconnectClient()

    # Test sensor message publishing
    def testSensorMsgPub(self):
        qos = 0
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE,
                                    ConfigConst.KEEP_ALIVE_KEY,
                                    ConfigConst.DEFAULT_KEEP_ALIVE)
        sensorData = SensorData()
        sensorData.setValue(22.0)
        payload = DataUtil().sensorDataToJson(sensorData)

        self.mcc.setDataMessageListener(DefaultDataMessageListener())
        self.mcc.connectClient()
        sleep(5)
        self.mcc.publishMessage(resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
                                msg=payload, qos=qos)
        sleep(delay + 5)
        self.mcc.disconnectClient()

    # Test CDA management status publishing only
    def testCDAManagementStatusPublish(self):
        qos = 1
        delay = self.cfg.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE,
                                    ConfigConst.KEEP_ALIVE_KEY,
                                    ConfigConst.DEFAULT_KEEP_ALIVE)
        self.mcc.connectClient()
        self.mcc.publishMessage(resource=ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE,
                                msg="TEST: This is the CDA message payload.", qos=qos)
        sleep(delay)
        self.mcc.disconnectClient()

if __name__ == "__main__":
    unittest.main()
