import logging
import unittest
import time

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.CoapServerAdapter import CoapServerAdapter
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener

class CoapServerAdapterTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
                            level=logging.DEBUG)

    def setUp(self):
        self.coapClient = CoapClientConnector()
        self.coapServer = CoapServerAdapter()
        self.coapClient.setDataMessageListener(DefaultDataMessageListener())

    def tearDown(self):
        self.coapServer.stopServer()

    def testConnectAndDisconnect(self):
        self.coapServer.startServer()
        time.sleep(2)  # short wait
        self.coapServer.stopServer()
        time.sleep(2)

    def testGetSensorData(self):
        self.coapServer.startServer()
        time.sleep(2)
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        self.coapClient.sendGetRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE)
        time.sleep(2)
        self.coapServer.stopServer()

    def testPostSensorData(self):
        self.coapServer.startServer()
        time.sleep(2)
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        self.coapClient.sendPostRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, payload)
        time.sleep(2)
        self.coapServer.stopServer()

    def testPutSensorData(self):
        self.coapServer.startServer()
        time.sleep(2)
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        self.coapClient.sendPutRequest(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, payload)
        time.sleep(2)
        self.coapServer.stopServer()

    def testDeleteMgmtStatus(self):
        self.coapServer.startServer()
        time.sleep(2)
        self.coapClient.sendDeleteRequest(ResourceNameEnum.CDA_MGMT_STATUS_MSG_RESOURCE)
        time.sleep(2)
        self.coapServer.stopServer()

if __name__ == "__main__":
    unittest.main()
