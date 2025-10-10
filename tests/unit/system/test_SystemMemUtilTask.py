#####
# 
##
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#import logging
import psutil

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
	def tearDown(self):
		pass

	def testGetTelemetryValue(self):
		val = self.memUtilTask.getTelemetryValue()
		
		self.assertGreaterEqual(val, 0.0)
		logging.info("Virtual memory utilization: %s", str(val))

if __name__ == "__main__":
	unittest.main()
	