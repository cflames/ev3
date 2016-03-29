import copy

class RobotMessage():
    """
    This class is for the message from RobotConnection to other modules
    """
    def __init__(self):
        self.leftMotorTacho = 0
        self.rightMotorTacho = 0
        self.leftSensor = []
        self.frontSensor = []
        self.timeStamp = 0
        
    def __str__(self):
        msg = "RobotMessage:\n"
        msg += str(self.leftMotorTacho) + "\n"
        msg += str(self.rightMotorTacho) + "\n"
        msg += str(self.leftSensor) + "\n"
        msg += str(self.frontSensor) + "\n"
        msg += str(self.timeStamp) + "\n"
        return msg
        
    def copy(self):
        return copy.deepcopy(self)
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.leftMotorTacho == other.leftMotorTacho \
               and self.rightMotorTacho == other.rightMotorTacho \
               and self.leftSensor == other.leftSensor \
               and self.frontSensor == other.frontSensor \
               and self.timeStamp == other.timeStamp
        