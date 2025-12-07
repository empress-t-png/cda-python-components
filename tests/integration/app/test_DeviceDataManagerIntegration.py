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

class DeviceDataManagerIntegrationTest(unittest.TestCase):
    """
    Basic integration tests for DeviceDataManager.
    This is a starting point for validating CDA integration with MQTT or CoAP.
    
    NOTE: This test MAY require the sense_emu_gui to be running,
    depending on whether or not the 'enableEmulator' flag is
    True within the ConstrainedDevice section of PiotConfig.props.
    If so, it must have access to the underlying libraries that
    support the pisense module.
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing DeviceDataManager class...")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDeviceDataMgrTimedIntegration(self):
        """
        Test DeviceDataManager integration with MQTT or CoAP for 5 minutes.
        
        OPTION 1: For MQTT testing - ensure the MQTT client is enabled in PiotConfig.props
                  and your MQTT broker is running.
        OPTION 2: For CoAP testing - ensure the CoAP client is enabled in PiotConfig.props,
                  and your CoAP server is running within your GDA.
        """
        ddMgr = DeviceDataManager()
        ddMgr.startManager()

        logging.info("DeviceDataManager started. Running for 5 minutes (300 seconds)...")
        logging.info("Adjust the SenseHAT emulator temperature slider to test threshold crossing.")

        # Run for 5 minutes to observe sensor/system data publishing and actuator responses
        sleep(300)

        ddMgr.stopManager()
        logging.info("DeviceDataManager stopped.")

if __name__ == "__main__":
    unittest.main()
