#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.data.SensorData import SensorData

class HumiditySensorEmulatorTask(BaseSensorSimTask):
    """
    Humidity sensor emulator that generates simulated humidity data.
    """
    
    def __init__(self, dataSet=None):
        super(HumiditySensorEmulatorTask, self).__init__(
            name=ConfigConst.HUMIDITY_SENSOR_NAME,
            typeID=ConfigConst.HUMIDITY_SENSOR_TYPE,
            dataSet=dataSet,
            minVal=0.0,
            maxVal=100.0
        )