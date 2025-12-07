import unittest
import logging
from time import sleep

from programmingtheiot.cda.connection.AsyncCoapClientConnector import AsyncCoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

class CoapAsyncClientConnectorTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s:%(module)s:%(levelname)s:%(message)s")
        logging.info("Testing AsyncCoapClientConnector class...")

    def setUp(self):
        # Use coap.me as a public test server
        self.coapClient = AsyncCoapClientConnector(base_url="coap://coap.me")

    def tearDown(self):
        pass

    def testDeleteSensorMessageCon(self):
        """
        DELETE SensorData with Confirmable request.
        """
        result = self.coapClient.sendDeleteRequest(
            resource="test",
            enableCON=True,
            timeout=5
        )
        logging.info("DELETE SensorMsg (CON) result: %s", result)
        self.assertTrue(result)

    def testDeleteSensorMessageNon(self):
        """
        DELETE SensorData with Non‑Confirmable request.
        """
        result = self.coapClient.sendDeleteRequest(
            resource="test",
            enableCON=False,
            timeout=5
        )
        logging.info("DELETE SensorMsg (NON) result: %s", result)
        self.assertTrue(result)

    def testActuatorCommandObserve(self):
        """
        Start and stop an Observe request for ActuatorCmd.
        """
        logging.info("Starting ActuatorCmd Observe test...")
        self._startObserver()
        sleep(20)  # wait for notifications
        self._stopObserver()
        logging.info("ActuatorCmd Observe test complete.")

    def _startObserver(self):
        self.coapClient.startObserver(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)

    def _stopObserver(self):
        self.coapClient.stopObserver(resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE)


if __name__ == "__main__":
    unittest.main()
