#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HumidifierActuatorSimTask(BaseActuatorSimTask):
    """
    Humidifier actuator simulation task.
    """
    
    def __init__(self):
        super(HumidifierActuatorSimTask, self).__init__(
            name=ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
            typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE,
            simpleName="Humidifier"
        )
