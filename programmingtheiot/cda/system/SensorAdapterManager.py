#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 

import logging

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask

class SensorAdapterManager(object):
    """
    Manager for sensor adapter tasks.
    """
    
    def __init__(self):
        self.configUtil = ConfigUtil()
        
        self.pollRate = \
            self.configUtil.getInteger(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.POLL_CYCLES_KEY, 
                defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)
        
        self.useEmulator = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.ENABLE_EMULATOR_KEY)
        
        self.locationID = \
            self.configUtil.getProperty(
                section=ConfigConst.CONSTRAINED_DEVICE, 
                key=ConfigConst.DEVICE_LOCATION_ID_KEY, 
                defaultVal=ConfigConst.NOT_SET)
        
        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.handleTelemetry, 'interval', seconds=self.pollRate, 
            max_instances=2, coalesce=True, misfire_grace_time=15)
        
        self.dataMsgListener = None
        self.humidityAdapter = None
        self.pressureAdapter = None
        self.tempAdapter = None
        
        if self.useEmulator:
            logging.info("SensorAdapterManager will use EMULATORS.")
        else:
            logging.info("SensorAdapterManager will use SIMULATORS.")
        
        self._initEnvironmentalSensorTasks()
    
    def _initEnvironmentalSensorTasks(self):
        """
        Initialize environmental sensor tasks.
        """
        if not self.useEmulator:
            logging.info("Creating sensor simulator tasks...")
            
            self.humidityAdapter = HumiditySensorSimTask()
            self.pressureAdapter = PressureSensorSimTask()
            self.tempAdapter = TemperatureSensorSimTask()
    
    def handleTelemetry(self):
        """
        Handle telemetry from sensor tasks.
        """
        humidityData = self.humidityAdapter.generateTelemetry()
        pressureData = self.pressureAdapter.generateTelemetry()
        tempData = self.tempAdapter.generateTelemetry()
        
        humidityData.setLocationID(self.locationID)
        pressureData.setLocationID(self.locationID)
        tempData.setLocationID(self.locationID)
        
        logging.debug('Generated humidity data: ' + str(humidityData))
        logging.debug('Generated pressure data: ' + str(pressureData))
        logging.debug('Generated temp data: ' + str(tempData))
        
        if self.dataMsgListener:
            self.dataMsgListener.handleSensorMessage(humidityData)
            self.dataMsgListener.handleSensorMessage(pressureData)
            self.dataMsgListener.handleSensorMessage(tempData)
    
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """
        Set the data message listener.
        """
        if listener:
            self.dataMsgListener = listener
            return True
        return False
    
    def startManager(self) -> bool:
        """
        Start the sensor adapter manager.
        """
        logging.info("Started SensorAdapterManager.")
        
        if not self.scheduler.running:
            self.scheduler.start()
            return True
        else:
            logging.info("SensorAdapterManager scheduler already started. Ignoring.")
            return False
    
    def stopManager(self) -> bool:
        """
        Stop the sensor adapter manager.
        """
        logging.info("Stopped SensorAdapterManager.")
        
        try:
            self.scheduler.shutdown()
            return True
        except:
            logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
            return False