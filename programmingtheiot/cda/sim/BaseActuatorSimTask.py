#####
# 
# This class is part of the Programming the Internet of Things project.
# 

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
    """
    Base class for simulated actuator tasks.
    """
    
    def __init__(self, name: str = "BaseActuatorSimTask", typeID: int = 0, simpleName: str = "Actuator"):
        self.name = name
        self.typeID = typeID
        self.simpleName = simpleName
        self.latestActuatorData = None
        
        logging.info("Initialized actuator simulation task: " + self.name)
    
    def activateActuator(self, val: float) -> bool:
        """
        Activates the actuator with the given value.
        """
        logging.info("Activating %s actuator with value: %.2f", self.simpleName, val)
        return True
    
    def deactivateActuator(self) -> bool:
        """
        Deactivates the actuator.
        """
        logging.info("Deactivating %s actuator", self.simpleName)
        return True
    
    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        """
        Updates the actuator based on the ActuatorData command.
        """
        if data is not None:
            self.latestActuatorData = data
            
            logging.debug("Updating actuator: %s", data.getName())
            
            if data.getCommand() == ConfigConst.COMMAND_ON:
                self.activateActuator(data.getValue())
            else:
                self.deactivateActuator()
                
        return self.latestActuatorData
    
    def getName(self) -> str:
        """
        Returns the name of this actuator.
        """
        return self.name
    
    def getTypeID(self) -> int:
        """
        Returns the type ID of this actuator.
        """
        return self.typeID
