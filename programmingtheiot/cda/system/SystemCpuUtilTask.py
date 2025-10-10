import logging

import psutil
 
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask
 
class SystemCpuUtilTask(BaseSystemUtilTask):

    def __init__(self):

        super(SystemCpuUtilTask, self).__init__(

            name=ConfigConst.CPU_UTIL_NAME,

            typeID=ConfigConst.CPU_UTIL_TYPE

        )
 
    def getTelemetryValue(self) -> float:

        return psutil.cpu_percent()