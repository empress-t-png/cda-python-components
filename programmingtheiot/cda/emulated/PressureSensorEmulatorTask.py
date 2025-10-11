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

class PressureSensorEmulatorTask(BaseSensorSimTask):
    """
    Pressure sensor emulator that generates simulated pressure data.
    """
    
    def __init__(self, dataSet=None):
        super(PressureSensorEmulatorTask, self).__init__(
            name=ConfigConst.PRESSURE_SENSOR_NAME,
            typeID=ConfigConst.PRESSURE_SENSOR_TYPE,
            dataSet=dataSet,
            minVal=990.0,
            maxVal=1010.0
        )