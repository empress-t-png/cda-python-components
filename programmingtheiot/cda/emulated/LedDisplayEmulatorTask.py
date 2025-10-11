#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import logging

from programmingtheiot.data.ActuatorData import ActuatorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	"""
	LED Display actuator emulator.
	"""

	def __init__(self):
		super(LedDisplayEmulatorTask, self).__init__(
			actuatorType=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE,
			simpleName="LED_Display"
		)
	
	def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		if cmd == ConfigConst.COMMAND_ON:
			logging.info(f"LED Display turned ON - Message: {stateData if stateData else 'No message'}")
			return 0
		elif cmd == ConfigConst.COMMAND_OFF:
			logging.info("LED Display turned OFF")
			return 0
		else:
			logging.warning(f"LED Display received unknown command: {cmd}")
			return -1