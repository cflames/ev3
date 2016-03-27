from SimpleSocket import SimpleSocket
from Message import RobotMessage

class RobotConnection():
    """
    Inherit from SimpleSocket, implement connection to Ev3, receive message and decode it in json format
    """
    def __init__(self):
        super().__init__()
        self.remoteIp = ""
        self.remotePort = 5000
        self.socket = SimpleSocket()
        # buffer to receive messages from Ev3
        self.__buffer = ""
        # filename to save raw data
        self.rawDataFileName = ""
        self.__rawFile = None
          
    def connectToEv3(self):
        # Do not consider exception because it's very simple network environment
        self.socket.connect(self.remoteIp, self.remotePort)
        self.__rawFile = self.__openDataFile("w")
        
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
        if self.__rawFile is not None:
            self.__rawFile.write(message)

    def readDataFileToBuffer(self):
        """
        read raw data from file and save to buffer
        """
        self.__openDataFile("r")
        self.__buffer = self.__rawFile.read()
        self.__rawFile.close()        
            
    def __readFromSocket(self):
        """
        Read all contents from socket and put it into self.buffer
        """
        while True:
            message = self.socket.receiveMessage()
            # read all untile there is ""
            if message == "":
                break
            self.__writeDataFile(message)
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
        message.leftMotorTacho = int(counters[0])
        message.rightMotorTacho = int(counters[1])      
        message.leftSensor = [float(item) for item in counters[2].strip(" ").split(" ")]       
        # now there is only one sample (distance, middle motor tacho count)
        message.frontSensor = [float(item) for item in counters[3].strip(" ").split(" ")] 
        
        return message
        
    def readMessage(self):
        """
        External interface, other modules call this to read message 
        """
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