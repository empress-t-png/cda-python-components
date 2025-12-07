import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
    """
    Shell representation of class for student implementation.
    """

    # --- Actuator type constants ---
    HVAC_ACTUATOR_TYPE = 1
    HUMIDIFIER_ACTUATOR_TYPE = 2
    LED_ACTUATOR_TYPE = 3

    # --- Command constants ---
    COMMAND_OFF = 0
    COMMAND_ON = 1

    def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name = ConfigConst.NOT_SET, d = None):
        super(ActuatorData, self).__init__(name = name, typeID = typeID, d = d)
        self.command = ConfigConst.DEFAULT_COMMAND
        self.value = 0.0
        self.stateData = ""
        self.isResponse = False

    def getCommand(self) -> int:
        return self.command

    def getStateData(self) -> str:
        return self.stateData

    def getValue(self) -> float:
        return self.value

    def isResponseFlagEnabled(self) -> bool:
        return self.isResponse

    def setCommand(self, command: int):
        self.command = command

    def setAsResponse(self):
        self.isResponse = True

    def setStateData(self, stateData: str):
        self.stateData = stateData

    def setValue(self, val: float):
        self.value = val

    def _handleUpdateData(self, data):
        if data and isinstance(data, ActuatorData):
            self.command = data.getCommand()
            self.value = data.getValue()
            self.stateData = data.getStateData()
