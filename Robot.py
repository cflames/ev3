import math

from Pose import Pose
from Message import RobotMessage 
        
class Robot():
    """
    Robot class to get pose of robot.
    Robot control command is not implemented now because manally control so far
    """
    SUCCESS = 0
    ERROR = -1
    
    def __init__(self):
        # Current location, middle point of two wheels, pose record of robot
        self.pose = Pose()
        # pose history list
        self.poseList = []
        # the map of environment
        self.lastLeftTacho = 0
        self.lastRightTacho = 0
        
        #Robot parameters
        self.sensorWheelAngle = 90*math.pi/180
        self.Width = 14.35  #two wheel distnce
        self.TurnRadius = self.Width/2
        self.SensorRadius = 8.0 #Front Sensor to middle point of two wheels
        self.wheelDiameter = 4.32        
        self.SensorLength = 3.0
        
    def getRobotShape(self, pose):
        """
        get sensor, leftwheel, rightWheel coord
        """
        sx, sy = self.__getFrontSensorCoord(pose)
        lx, ly = self.__getLeftWheelCooord(pose)
        rx, ry = self.__getRightWheelCooord(pose)
        return sx, sy, lx, ly, rx, ry
    
    def motion(self, sample):
        """
        From sample to calcluate robot motion
        """
        self.pose = self.__calculateSamples(sample)
        self.poseList.append(Pose(self.pose.x, self.pose.y, self.pose.theta))
        self.lastLeftTacho = sample.leftMotorTacho
        self.lastRightTacho = sample.rightMotorTacho
        
    def updateCorner(self, samples, mapUpdateCallback):
        """
        calcluate x,y from corner sample
        """
        samples = samples.frontSensor
        nx, ny = self.__getFrontSensorCoord(self.pose)
        transAngle = (self.pose.theta - math.pi/2)%(math.pi*2)        
        for sample in samples:        
            # suppose x,y is the 0,0 of new coords, get the new x,y for sample in the new coords
            sx =  round((sample[0] + self.SensorLength)*math.sin(sample[1]*math.pi/180))
            sy =  round((sample[0] + self.SensorLength)*math.cos(sample[1]*math.pi/180))
            # get the x,y for the sample point in origin coords
            mx, my = self.__coordsTrans(sx, sy, transAngle)
            # update map 
            mapUpdateCallback(nx - mx ,ny + my, self.pose.theta)  
        return 0
        
    def updateMap(self, sample, mapUpdateCallback):
        """
        Update map based on samples, this function must be called after motion
        """             
       # print(self.poseList)
        if len(self.poseList) < 2:
            print(" motion function must be called before updateMap")
            return Robot.ERROR

        if self.poseList[len(self.poseList)-2].theta != self.poseList[len(self.poseList)-1].theta:
             print("Do not update map after turn")
             return Robot.ERROR
             
        leftSamples = sample.leftSensor     
        if self.__updateMapFromLeftSensor(leftSamples, mapUpdateCallback) != 0:
            print("Failed to update map based on left sensor samples")
            return Robot.ERROR
        
        #frontSamples = sample.frontSensor
        #self.__updateMapFromFrontSensor(frontSamples, mapUpdateCallback)
        return Robot.SUCCESS

    def __getDeltaTacho(self, sample):
        deltaLeftTacho = sample.leftMotorTacho - self.lastLeftTacho
        deltaRightTacho = sample.rightMotorTacho - self.lastRightTacho
        return deltaLeftTacho, deltaRightTacho
        
    def __calculateSamples(self, sample):
        """
        calcluate new pose based on sample
        1. check if robot is moved forward
        2. check if robot is turned
        """
        deltaLeftTacho, deltaRightTacho  = self.__getDeltaTacho(sample)
        pose = Pose()
        if deltaRightTacho - 10 < deltaLeftTacho < deltaRightTacho + 10:
            # in this case, there is no turn, just move
            pose = self.__calcluateMove(deltaLeftTacho)
        else:
            pose = self.__calcluateTurn(deltaRightTacho)
     
        return pose
        
    def __calcluateWheelMoveDistance(self, tacho):
        """
        If robot is moving forward, the moved distance can be calcluated from tacho count
        """
        return tacho/360*self.wheelDiameter*math.pi
        
    def __calcluateRadianFromMotorTacho(self, tacho):
        """
        Get the radian based on the tacho of one motor
        """        
        return  math.pi*(((tacho)*self.wheelDiameter)/(self.Width))/180
        
    def __calcluateMove(self, tacho):     
        pose = Pose()
        moveDistance = self.__calcluateMoveDistanceFromTacho(tacho)
        pose.x, pose.y = self.__getCoord(self.pose.x, self.pose.y, self.pose.theta, moveDistance)
        pose.theta = self.pose.theta
        return pose
            
    def __getCoord(self, x, y, theta, moveDistance):
        x = round(x + moveDistance*math.cos(theta))
        y = round(y + moveDistance*math.sin(theta)) 
        return x, y         
        
    def __calcluateMoveDistanceFromTacho(self, tacho):
        return tacho/360*self.wheelDiameter*math.pi
        
    def __calcluateTurn(self, tacho):
        pose = Pose()
        # the radian during this turn
        deltaTheta = self.__calcluateRadianFromMotorTacho(tacho)
        self.pose.theta -= deltaTheta
        pose.x = self.pose.x
        pose.y = self.pose.y        
        pose.theta = self.pose.theta%(math.pi*2)
        
        return pose
        
    def __getFrontSensorCoord(self, pose):      
        sx = round(pose.x + self.SensorRadius*math.cos(pose.theta))
        sy = round(pose.y + self.SensorRadius*math.sin(pose.theta)) 
        return sx, sy
        
    def __getLeftWheelCooord(self, pose):
        lx = round(pose.x + self.TurnRadius*math.cos(pose.theta - self.sensorWheelAngle))          
        ly = round(pose.y + self.TurnRadius*math.sin(pose.theta - self.sensorWheelAngle))
        return lx, ly
        
    def __getRightWheelCooord(self, pose):
        rx = round(pose.x + self.TurnRadius*math.cos(pose.theta + self.sensorWheelAngle))          
        ry = round(pose.y + self.TurnRadius*math.sin(pose.theta + self.sensorWheelAngle))
        return rx, ry
        
    def __updateMapFromLeftSensor(self, leftSamples, mapUpdateCallback):
        """
        between two samples, there are measurements from left sensor, check the delta tacho count, if left is not equal
        right, that means there is turn, do not handle turn now, give warning if turn
        if left equal right, because there is not tacho measurement for each left sensor measurement point, we just suppose
        the moved distance between two measure points is: moveDistance/len(leftSensorSamples)
        """
        if len(leftSamples) < 1:
            return 0
        poseNum = len(self.poseList)
        if poseNum < 2:
            print("There is only one pose, robot does not move so far")
            return -1
        theta = self.pose.theta
        x, y = self.poseList[poseNum-2].x, self.poseList[poseNum-2].y
        moveDistance = math.sqrt((self.pose.x - x)**2 + (self.pose.y - y)**2)/len(leftSamples)
        # get the init x,y for left Sensor, in this robot, it' same location as left wheel
        # the theta keeps same after move
        x, y = self.__getLeftWheelCooord(Pose(x, y, theta))
        for index, sample in enumerate(leftSamples):         
            # get x,y for each left sensor
            nx, ny = self.__getCoord(x, y, theta, moveDistance*(index + 1))                 
            # suppose x,y is the 0,0 of new coords, get the new x,y for sample in the new coords
            sx, sy = 0, sample
            # Get the angle between new coords and old coords
            transAngle = (theta)%(2*math.pi)
            # get the x,y for the sample point in origin coords
            mx, my = self.__coordsTrans(sx, sy, transAngle)
            # update map 
            mapUpdateCallback(nx + mx,ny - my, self.pose.theta)  
        return 0
        
    def __updateMapFromFrontSensor(self, frontSamples, mapUpdateCallback):
        """
        """
        # get the init x,y for front sensor
        x, y = self.__getFrontSensorCoord(self.pose)
        # suppose x,y is the 0,0 of new coords, get the new x,y for sample in the new coords
        # in current implementation, front sensor do not turn, so, frontSamples[1] always 0
        sx, sy = 0, frontSamples[0]
        # Get the angle between new coords and old coords
        transAngle = (self.pose.theta-math.pi/2)%(2*math.pi)
        # get the x,y for the sample point in origin coords
        mx, my = self.__coordsTrans(sx, sy, transAngle)
        # update map 
        mapUpdateCallback(x - mx,y + my, self.pose.theta)  
        return 0        
        
    def __coordsTrans(self, mx, my, transAngle):
        nx = round(mx*math.cos(transAngle) + my*math.sin(transAngle))
        ny = round(my*math.cos(transAngle) - mx*math.sin(transAngle)) 
        return nx, ny        
    