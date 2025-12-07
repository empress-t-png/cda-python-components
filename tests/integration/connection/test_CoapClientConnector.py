"""
CoapClientConnectorTest.py
Integration tests for CoapClientConnector covering Discovery, Observe, GET, POST, PUT, DELETE, SystemPerf, and ActuatorCmd.
"""

import unittest
import logging
from time import sleep
import json

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector

class CoapClientConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s:%(module)s:%(levelname)s:%(message)s")
        logging.info("Testing CoapClientConnector class...")

    def setUp(self):
        self.cfg = ConfigUtil()
        self.ccc = CoapClientConnector()
        self.ccc.setDataMessageListener(DefaultDataMessageListener())

    def tearDown(self):
        pass

    def testDiscovery(self):
        """
        Test CoAP discovery (.well-known/core).
        """
        response = self.ccc.sendDiscoveryRequest()
        logging.info("DISCOVERY response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testActuatorCmdObserve(self):
        """
        Subscribe to ActuatorCmd and print Observe notifications.
        """
        self.ccc.sendObserveRequest(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
        sleep(15)
        self.ccc.cancelObserveRequest(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)
        sleep(2)

    def testGetSensorData(self):
        response = self.ccc.sendGetRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)
        logging.info("GET SensorMsg response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testPostSensorData(self):
        payload = json.dumps({"msg": "hello"})
        response = self.ccc.sendPostRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, payload=payload)
        logging.info("POST SensorMsg response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testPostSensorMessageCon(self):
        """
        POST SensorData with Confirmable request.
        """
        data = SensorData()
        jsonData = DataUtil().sensorDataToJson(data)
        response = self.ccc.sendPostRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
                                            payload=jsonData, enableCON=True, timeout=5)
        logging.info("POST SensorMsg (CON) response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testPostSensorMessageNon(self):
        """
        POST SensorData with Non‑Confirmable request.
        """
        data = SensorData()
        jsonData = DataUtil().sensorDataToJson(data)
        response = self.ccc.sendPostRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
                                            payload=jsonData, enableCON=False, timeout=5)
        logging.info("POST SensorMsg (NON) response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testPutSensorData(self):
        payload = json.dumps({"updated": True})
        response = self.ccc.sendPutRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, payload=payload)
        logging.info("PUT SensorMsg response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testDeleteMgmtStatus(self):
        response = self.ccc.sendDeleteRequest(ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
        logging.info("DELETE MgmtStatus response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testDeleteSensorMessageCon(self):
        """
        DELETE SensorData with Confirmable request.
        """
        response = self.ccc.sendDeleteRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            enableCON=True, timeout=5)
        logging.info("DELETE SensorMsg (CON) response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testDeleteSensorMessageNon(self):
        """
        DELETE SensorData with Non‑Confirmable request.
        """
        response = self.ccc.sendDeleteRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            enableCON=False, timeout=5)
        logging.info("DELETE SensorMsg (NON) response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testGetSystemPerfMsg(self):
        response = self.ccc.sendGetRequest(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE)
        logging.info("GET SystemPerfMsg response: %s", response)
        self.assertTrue(response)
        sleep(2)

    def testSendActuatorCommand(self):
        """
        Send actuator command (HVAC ON at 50%) to trigger Observe notifications.
        """
        actuatorData = ActuatorData(typeID=ActuatorData.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(50)

        payload = DataUtil().actuatorDataToJson(actuatorData)
        response = self.ccc.sendPostRequest(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, payload=payload)
        logging.info("POST ActuatorCmd response: %s", response)
        self.assertTrue(response)
        sleep(2)

if __name__ == "__main__":
    unittest.main()
