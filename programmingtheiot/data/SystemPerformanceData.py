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

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0
	
	def __init__(self, d = None):
		super(SystemPerformanceData, self).__init__(name = ConfigConst.SYSTEM_PERF_MSG, typeID = ConfigConst.SYSTEM_PERF_TYPE, d = d)
		self.cpuUtil = self.DEFAULT_VAL
		self.diskUtil = self.DEFAULT_VAL
		self.memUtil = self.DEFAULT_VAL
	
	def getCpuUtilization(self):
		return self.cpuUtil
	
	def getDiskUtilization(self):
		return self.diskUtil
	
	def getMemoryUtilization(self):
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		self.cpuUtil = cpuUtil
	
	def setDiskUtilization(self, diskUtil):
		self.diskUtil = diskUtil
	
	def setMemoryUtilization(self, memUtil):
		self.memUtil = memUtil
	
	def _handleUpdateData(self, data):
		if data and isinstance(data, SystemPerformanceData):
			self.cpuUtil = data.getCpuUtilization()
			self.diskUtil = data.getDiskUtilization()
			self.memUtil = data.getMemoryUtilization()