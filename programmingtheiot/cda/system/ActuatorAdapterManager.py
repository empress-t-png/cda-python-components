#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask

class ActuatorAdapterManager(object):
	"""
	Manager for actuator adapter tasks.
	"""
	
	def __init__(self):
		self.configUtil = ConfigUtil()
		
		self.useEmulator = \
			self.configUtil.getBoolean(
				section=ConfigConst.CONSTRAINED_DEVICE,
				key=ConfigConst.ENABLE_EMULATOR_KEY)
		
		self.dataMsgListener = None
		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None
		
		if self.useEmulator:
			logging.info("ActuatorAdapterManager will use EMULATORS.")
		else:
			logging.info("ActuatorAdapterManager will use SIMULATORS.")
		
		self._initActuatorTasks()
	
	def _initActuatorTasks(self):
		"""
		Initialize actuator tasks.
		"""
		if not self.useEmulator:
			logging.info("Creating actuator simulator tasks...")
			
			self.humidifierActuator = HumidifierActuatorSimTask()
			self.hvacActuator = HvacActuatorSimTask()
		else:
			logging.info("Creating actuator emulator tasks...")
			
			# Load humidifier actuator emulator
			humidModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask', 'HumidifierEmulatorTask')
			humidClazz = getattr(humidModule, 'HumidifierEmulatorTask')
			self.humidifierActuator = humidClazz()
			
			# Load HVAC actuator emulator
			hvacModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask', 'HvacEmulatorTask')
			hvacClazz = getattr(hvacModule, 'HvacEmulatorTask')
			self.hvacActuator = hvacClazz()
			
			# Load LED display actuator emulator
			ledModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', 'LedDisplayEmulatorTask')
			ledClazz = getattr(ledModule, 'LedDisplayEmulatorTask')
			self.ledDisplayActuator = ledClazz()
	
	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		"""
		Send actuator command.
		"""
		if data:
			logging.info("Actuator command received for location ID %s. Processing...", data.getLocationID())
			
			actuatorType = data.getTypeID()
			
			if actuatorType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
				self.humidifierActuator.updateActuator(data)
				return True
			elif actuatorType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
				self.hvacActuator.updateActuator(data)
				return True
			elif actuatorType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
				self.ledDisplayActuator.updateActuator(data)
				return True
			else:
				logging.warning("No actuator of type %s available.", actuatorType)
				return False
		else:
			logging.warning("Actuator data is None. Ignoring.")
			return False
	
	def setDataMessageListener(self, listener) -> bool:
		"""
		Set the data message listener.
		"""
		if listener:
			self.dataMsgListener = listener
			return True
		return False
