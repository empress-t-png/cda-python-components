#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
import logging
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener


class DefaultDataMessageListener(IDataMessageListener):
    """
    Basic (default) implementation of the IDataMessageListener interface.
    """

    def __init__(self):
        """
        Default constructor. This will set remote server information and
        information based on the default configuration file contents.
        """
        pass

    def onActuatorCommand(self, actuatorData: ActuatorData):
        logging.info("Received ActuatorData via Observe: %s", actuatorData)

    def onSensorMessage(self, sensorData: SensorData):
        logging.info("Received SensorData: %s", sensorData)

    def onSystemPerformanceMessage(self, sysPerfData: SystemPerformanceData):
        logging.info("Received SystemPerformanceData: %s", sysPerfData)
