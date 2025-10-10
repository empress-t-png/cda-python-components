import unittest
from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
 
class SystemCpuUtilTaskTest(unittest.TestCase):
    def setUp(self):
        self.task = SystemCpuUtilTask()
 
    def testGetTelemetryValue(self):
        value = self.task.getTelemetryValue()
        print(f"CPU Utilization: {value}")
        self.assertTrue(value >= -1.0 and value <= 100.0)
 
if __name__ == '__main__':
    unittest.main()