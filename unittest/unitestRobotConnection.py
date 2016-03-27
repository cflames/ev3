import unittest
import socket
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch, call
from RobotConnection import RobotConnection
from Message import RobotMessage

class RobotConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.socketMock = patch("RobotConnection.SimpleSocket").start()
        self.socketMock.return_value.connect = MagicMock()
        self.testConn = RobotConnection()
        self.testConn.remoteIp = "myip"
        self.testConn.remotePort = 5000
        
    def tearDown(self):
        patch.stopall()
        
    def testConnectToEv3(self):       
        self.testConn.connectToEv3()
        self.socketMock.return_value.connect.assert_called_with("myip", 5000)
     
    def testReadDataFileToBuffer(self):
        m = mock_open()
        with patch("builtins.open", m, create=True):
            m.read = MagicMock()
            self.testConn.rawDataFileName="myfile"
            self.testConn.readDataFileToBuffer()
            m.assert_called_once_with("myfile", "r")
        handle = m()
        handle.read.assert_called_once_with()        
        
    def testReadMessage(self):
        testTxt = "100, 100, 30 30 40 41 42, 75 15, 1231231 end"
        testMessage = RobotMessage()
        testMessage.leftMotorTacho = 100
        testMessage.rightMotorTacho = 100
        testMessage.leftSensor = [30,30,40,41,42]
        testMessage.frontSensor = [75,15]
        testMessage.timeStamp = 0
        self.socketMock.return_value.receiveMessage = MagicMock()
        self.socketMock.return_value.receiveMessage.side_effect = [testTxt, ""]
        message = self.testConn.readMessage()

        assert testMessage == message
    
if __name__ == '__main__':
    unittest.main()