#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask

class PressureSensorSimTask(BaseSensorSimTask):
    """
    Pressure sensor simulation task.
    """
    
    def __init__(self, dataSet=None):
        super(PressureSensorSimTask, self).__init__(
            name=ConfigConst.PRESSURE_SENSOR_NAME,
            typeID=ConfigConst.PRESSURE_SENSOR_TYPE,
            dataSet=dataSet
        )
