import logging
import unittest
import time

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData

class CoapClientPerformanceTest(unittest.TestCase):
    
    NS_IN_MILLIS = 1000000
    MAX_TEST_RUNS = 10000
    
    @classmethod
    def setUpClass(self):
        logging.disable(level = logging.WARNING)
        
    def setUp(self):
        self.coapClient = CoapClientConnector()

    def tearDown(self):
        pass
                    
    def testPostRequestCon(self):
        print("Testing POST - CON")
        self._execTestPost(self.MAX_TEST_RUNS, True)

    def testPostRequestNon(self):
        print("Testing POST - NON")
        self._execTestPost(self.MAX_TEST_RUNS, False)

    def _execTestPost(self, maxTestRuns: int, useCon: bool):
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        
        startTime = time.time_ns()
        
        for seqNo in range(0, maxTestRuns):
            self.coapClient.sendPostRequest(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, enableCON = useCon, payload = payload)
            
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        print("POST message - useCON = " + str(useCon) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")

if __name__ == "__main__":
    unittest.main()


