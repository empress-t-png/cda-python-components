#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
from programmingtheiot.data.ActuatorData import ActuatorData

class LedDisplayEmulatorTask(BaseActuatorSimTask):
    """
    LED Display actuator emulator.
    """
    
    def __init__(self):
        super(LedDisplayEmulatorTask, self).__init__(
            name=ConfigConst.LED_ACTUATOR_NAME,
            typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE,
            simpleName="LED_Display"
        )