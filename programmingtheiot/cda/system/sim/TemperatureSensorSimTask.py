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

class TemperatureSensorSimTask(BaseSensorSimTask):
    """
    Temperature sensor simulator task.
    """
    
    def __init__(self, dataSet=None):
        super(TemperatureSensorSimTask, self).__init__(
            name=ConfigConst.TEMP_SENSOR_NAME,
            typeID=ConfigConst.TEMP_SENSOR_TYPE,
            dataSet=dataSet,
            minVal=ConfigConst.DEFAULT_TEMP_MIN_VAL if hasattr(ConfigConst, 'DEFAULT_TEMP_MIN_VAL') else 0.0,
            maxVal=ConfigConst.DEFAULT_TEMP_MAX_VAL if hasattr(ConfigConst, 'DEFAULT_TEMP_MAX_VAL') else 50.0
        )