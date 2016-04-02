from SimpleSocket import SimpleSocket
from Message import RobotMessage

class RobotConnection():
    """
    Inherit from SimpleSocket, implement connection to Ev3, receive message and decode it in json format
    """
    def __init__(self):
        self.remoteIp = ""
        self.remotePort = 5000
        self.socket = SimpleSocket()
        # buffer to receive messages from Ev3
        self.__buffer = ""
        # filename to save raw data
        self.rawDataFileName = ""
        self.__rawFile = None
          
        self.FrontSensorMax = 200
        self.LeftSensorMax = 70
        self.SensorInValid = ["Infinity", "", " "]
        
    def connectToEv3(self, simulate=False):
        # Do not consider exception because it's very simple network environment
        if not simulate:
            self.socket.connect(self.remoteIp, self.remotePort)
            self.__openDataFile("w")
        else:
            self.__openDataFile("r")
        
    def __openDataFile(self, attribute):
        """
        Open file for write or read
        """
        if self.rawDataFileName != "":
            self.__rawFile = open(self.rawDataFileName, attribute)

    def __writeDataFile(self, message):
        """
        Write message into data file
        """
        if not self.__rawFile is None:
            self.__rawFile.write(message + "\n")
            self.__rawFile.flush()

    def __readDataFileToBuffer(self):
        """
        read raw data from file and save to buffer
        """
        self.__buffer = self.__rawFile.read()
        self.__rawFile.close()        
            
    def __readFromSocket(self):
        """
        Read all contents from socket and put it into self.buffer
        """
        if True:
            message = self.socket.receiveMessage()
            # read all untile there is ""
            if message == "":
                return
           
            self.__writeDataFile(str(message))
            self.__buffer += message
            
    def __readFromBuffer(self, tail="end"):
        """
        Read one message from self.buffer, each message is ended by " end"
        """        
        if tail not in self.__buffer:
            return ""
            
        end = self.__buffer.index(tail)
     
        if end>0:
            message = self.__buffer[:end]
            self.__buffer = self.__buffer[end+len(tail):]
            return message
        return ""
        
    def __encodeMessage(self, rawMessage):
        """
        encode the raw message from Ev3 into json format
        """
        if rawMessage == "":
            return None
        
        counters = rawMessage.strip("\n").split(",")
        
        message = RobotMessage()
        
        if counters[0].strip(" ") == "Left":
            message.type = "Left"
            message.leftMotorTacho = int(counters[1])
            message.rightMotorTacho = int(counters[2])         
            message.leftSensor = [float(item) for item in counters[3].strip(" ").split(" ") \
                                     if item  not in self.SensorInValid and item != "" and float(item) < self.LeftSensorMax]       
            # now there is only one sample (distance, middle motor tacho count)
            message.frontSensor = [float(item) for item in counters[4].strip(" ").split(" ") \
                                     if item  not in self.SensorInValid and item != "" and float(item) < self.FrontSensorMax] 
        
        elif counters[0].strip(" ") == "Corner":
            message.type = "Corner"
            message.leftMotorTacho = int(counters[1])
            message.rightMotorTacho = int(counters[2])     
            message.leftSensor = []
            samples = counters[3].strip(" ").split(" ")
            for index in range(len(samples)):
                if index%2 == 0:
                    message.frontSensor.append((float(samples[index]), int(samples[index + 1]))) 
 
        return message
    
    def __filterInvalidSample(self):
        """
        
        """
    
    def readMessage(self, simulate=False):
        """
        External interface, other modules call this to read message 
        """
        if simulate == True:
            if not self.__rawFile.closed:
                self.__readDataFileToBuffer()
        else:
            self.__readFromSocket()
        rawMessage = self.__readFromBuffer()
        return self.__encodeMessage(rawMessage)
        
    def closeConnection():
        """
        Close socket
        """
        if self.socket is not None:
            self.socket.close()
        if self.__rawFile is not None:
            self.__rawFile.close()