#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

class TemperatureSensorSimTask(BaseSensorSimTask):
    """
    Temperature sensor simulation task.
    """
    
    def __init__(self, dataSet=None):
        super(TemperatureSensorSimTask, self).__init__(
            name=ConfigConst.TEMP_SENSOR_NAME,
            typeID=ConfigConst.TEMP_SENSOR_TYPE,
            dataSet=dataSet
        )
