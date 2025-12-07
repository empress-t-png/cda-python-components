#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 - 2025 by Andrew D. King
# 

import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.ActuatorData import ActuatorData

class DeviceDataManagerCallbackTest(unittest.TestCase):
    """
    This test case class contains very basic unit tests for
    DeviceDataManager callback functionality. It should not be considered complete,
    but serves as a starting point for implementing additional functionality
    within the Programming the IoT environment.
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing DeviceDataManager callback functionality...")

    def testActuatorDataCallback(self):
        # Disable comms for this test (either via PiotConfig.props or constructor)
        ddMgr = DeviceDataManager()  # if you added disableAllComms, use DeviceDataManager(disableAllComms=True)

        actuatorData = ActuatorData(actuatorType=ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.COMMAND_ON)
        actuatorData.setStateData("This is a test.")
        actuatorData.setValue(52)

        ddMgr.handleActuatorCommandMessage(actuatorData)

        # Allow time for actuator manager to process
        sleep(10)

if __name__ == "__main__":
    unittest.main()
