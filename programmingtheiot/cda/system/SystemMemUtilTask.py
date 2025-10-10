##
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import psutil

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemMemUtilTask(BaseSystemUtilTask):
    """
    Shell representation of class for student implementation.
    """

    def __init__(self):
        """
        Constructor for SystemMemUtilTask.
        Initializes the task with memory utilization name and type.
        """
        super(SystemMemUtilTask, self).__init__(
            name=ConfigConst.MEM_UTIL_NAME,
            typeID=ConfigConst.MEM_UTIL_TYPE
        )
        logging.info("SystemMemUtilTask instance created.")
    
    def getTelemetryValue(self) -> float:
        """
        Retrieves the current memory utilization percentage.
        
        Returns:
            float: The current memory utilization as a percentage (0-100).
        """
        mem_util = psutil.virtual_memory().percent
        logging.debug(f"Memory utilization: {mem_util}%")
        return mem_util