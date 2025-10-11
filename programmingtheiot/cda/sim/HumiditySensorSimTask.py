#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

class HumiditySensorSimTask(BaseSensorSimTask):
    """
    Humidity sensor simulation task.
    """
    
    def __init__(self, dataSet=None):
        super(HumiditySensorSimTask, self).__init__(
            name=ConfigConst.HUMIDITY_SENSOR_NAME,
            typeID=ConfigConst.HUMIDITY_SENSOR_TYPE,
            dataSet=dataSet
        )
