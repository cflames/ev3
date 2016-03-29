import math
import unittest
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch, call
from Robot import Robot
from Message import RobotMessage
from Pose import Pose

helpList = []
def helpMapCallBack(x, y):
    helpList.append((x, y))
    
class RobotTestCase(unittest.TestCase):
    """
    This unit test simulate a environment as following square, four points:(0,0), (0,50), (50,50), (50,0)
    
    ______________
    |             |
    | |           |
    | |           |
    | |           |
    |_|___________|
    """

    def testMotion(self):
        global helpList
        sample = RobotMessage()
        sample.leftMotorTacho = 0
        sample.rightMotorTacho = 0
        sample.leftSensor = [0]
        sample.frontSensor = [43,0]
        sample.timeStamp = 0
        robot = Robot()
        pose = Pose(20, 0, 90*math.pi/180)
        robot.pose = pose
        assert robot.sensorWheelAngle == 90*math.pi/180
        
        robot.motion(sample)
        
        assert robot.poseList[0] == pose
        
        robot.updateMap(sample, helpMapCallBack)
        
        # move forward 
        moveDistance = round(360/360*math.pi*robot.wheelDiameter) #14
        sample.leftMotorTacho = 360
        sample.rightMotorTacho = 360
        sample.leftSensor = [12.3, 12.3, 12.3]
        sample.frontSensor = [43-moveDistance,0]
        sample.timeStamp = 0
        
        robot.motion(sample)
        pose = Pose(20, 14, 90*math.pi/180)
        assert robot.pose == pose
        
        sx, sy, lx, ly, rx, ry = 20, 14+7, round(20-7.7), 14, round(20+7.7), 14
        assert (sx, sy, lx, ly, rx, ry) == robot.getRobotShape(pose)

        robot.updateMap(sample, helpMapCallBack)
        testList = [(0, round(14/3)), (0, round(14/3*2)), (0, round(14/3*3)), (20, 50)]
        assert testList == helpList       
        
        # turn right 45 degree 
        # deltatacho = 45/180*math.pi*robot.TurnRadius)/(robot.wheelDiameter*math.pi)*360
        helpList = []
        sample.leftMotorTacho = 360 + round((45*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.rightMotorTacho = 360 - round((45*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.leftSensor = [12.3, 12.3, 12.3]
        sample.frontSensor = [43,0]
        sample.timeStamp = 0        
        
        robot.motion(sample)
        pose = Pose(20, 14, round((90-45)*math.pi/180, 2))
        robot.pose.theta = round(robot.pose.theta, 2)

        assert robot.pose == pose
        
        moveWheel = round(7.7*math.cos(45/180*math.pi))
        moveSensor = round(7.0*math.cos(45/180*math.pi))
        
        pose = Pose(20, 14, (90-45)*math.pi/180)
        
        sx, sy, lx, ly, rx, ry = 20+moveSensor, 14 + moveSensor, 20 - moveWheel, 14 + moveWheel, 20 + moveWheel, 14 - moveWheel
        assert (sx, sy, lx, ly, rx, ry) == robot.getRobotShape(pose)
        
        testList = []
        robot.updateMap(sample, helpMapCallBack)
        assert testList == helpList
        
        #keep move forward with this angle
        helpList = []
        sample.leftMotorTacho = 360 + round((45*robot.TurnRadius)/(robot.wheelDiameter)*2) + 360
        sample.rightMotorTacho = 360 - round((45*robot.TurnRadius)/(robot.wheelDiameter)*2) + 360
        sample.leftSensor = [20, 20, 20]
        sample.frontSensor = [15]
        sample.timeStamp = 0        
        
        robot.motion(sample)
        pose = Pose(20 + round(14*math.cos(45/180*math.pi)), 14+ round(14*math.cos(45/180*math.pi)), round((90-45)*math.pi/180, 2))
        robot.pose.theta = round(robot.pose.theta, 2)   
        assert robot.pose == pose    
        
        # robot moved 14 again, each distance is 4.6, then, deltaX = sqrt(4.6*4.6/2), the sample point to sensor is 20
        # then, the delta(sensorX, samplepointX) is sqrt(20*20/2), the sampleX = lx + sqrt(4.6*4.6/2) - sqrt(20*20/2)
        # sampleY = ly + sqrt(4.6*4.6/2) + sqrt(20*20/2)
        testList = [(4, 36), (8, 40), (11, 43), (46, 40)]
        robot.updateMap(sample, helpMapCallBack)
        assert testList == helpList
        
        #Robot turn left 180
        sample.leftMotorTacho = 360 + round((45*robot.TurnRadius)/(robot.wheelDiameter)*2) + 360 - round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.rightMotorTacho = 360 - round((45*robot.TurnRadius)/(robot.wheelDiameter)*2) + 360 + round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.leftSensor = [20, 20, 20]
        sample.frontSensor = [15]
        sample.timeStamp = 0        
        
        robot.motion(sample)  
        pose = Pose(pose.x, pose.y, pose.theta + math.pi) 
        assert pose.x == robot.pose.x and pose.y == robot.pose.y and round(pose.theta, 2) == round(robot.pose.theta, 2)
        
        #Robot move 360 count
        helpList = []
        sample.leftMotorTacho = 360 + round((45*robot.TurnRadius)/(robot.wheelDiameter)*2) +720 - round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.rightMotorTacho = 360 - round((45*robot.TurnRadius)/(robot.wheelDiameter)*2) +720  + round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.leftSensor = [20, 20, 20]
        sample.frontSensor = [15]
        sample.timeStamp = 0       

        robot.motion(sample) 
        pose = Pose(20, 14, pose.theta)          
        assert pose.x == robot.pose.x and pose.y == robot.pose.y and round(pose.theta, 2) == round(robot.pose.theta, 2)
        sx, sy, lx, ly, rx, ry = 20-moveSensor, 14 - moveSensor, 20 + moveWheel, 14 - moveWheel, 20 - moveWheel, 14 + moveWheel
        assert (sx, sy, lx, ly, rx, ry) == robot.getRobotShape(pose)        
        
        # turn left 45 degree 
        # deltatacho = 45/180*math.pi*robot.TurnRadius)/(robot.wheelDiameter*math.pi)*360
        sample.leftMotorTacho = 360  +720 - round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.rightMotorTacho = 360  +720  + round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.leftSensor = [12.3, 12.3, 12.3]
        sample.frontSensor = [43,0]
        sample.timeStamp = 0        
        
        robot.motion(sample)
        pose = Pose(20, 14, pose.theta + 45/180*math.pi)
        assert pose.x == robot.pose.x and pose.y == robot.pose.y and round(pose.theta, 2) == round(robot.pose.theta, 2)
        
        sample.leftMotorTacho = 720  +720 - round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.rightMotorTacho = 720  +720  + round((180*robot.TurnRadius)/(robot.wheelDiameter)*2)
        sample.leftSensor = [12.3, 12.3, 12.3]
        sample.frontSensor = [0,0]
        sample.timeStamp = 0           
        pose = Pose(20, 0, pose.theta)
        robot.motion(sample)
        assert pose.x == robot.pose.x and pose.y == robot.pose.y and round(pose.theta, 2) == round(robot.pose.theta, 2)
        
        robot.updateMap(sample, helpMapCallBack)
        testList = [(40, round(14/3*2)), (40, round(14/3)), (40, 0), (20, -7)]
        assert testList == helpList
        
if __name__ == '__main__':
    unittest.main()