import math
from sklearn import linear_model
import numpy as np

class Line():
    def __init__(self, start=(0,0), end=(0,0)):
        self.startPoint = start
        self.endPoint = end
        self.xList = []
        self.yList = []


class Linear():
    """
    receive continues points(x,y), if sample is stoped, make a line1, then move, get another sample, make line2
    calculate if there is intersection for line1 and line2, (valid intersection in the axis scope), if there is valid
    intersect for line1 and line2, get the angle between two lines, check the angle, if it's less than 45 degree, merge these two lines 
    (use those points of line1 and line2), save result into line list
    repeat it
    """
    def __init__(self):
        self.__lines = []
        self.__interSectList = []
        self.__lastTheta = 255
        self.__degreeThreshhold = 30
        self.__InvalidPoint = 10000
        self.__tempLine = Line()
        self.__linearThreshhold = 6
        
    def getLines(self):
        return self.__lines
    
    def getInterSectList(self):
        return self.__interSectList
        
    def update(self, x, y, theta):     
        if self.__lastTheta == 255:
            self.__lastTheta = theta
            return 
        if theta == self.__lastTheta:
            print("theta same ", str(theta))
            self.__tempLine.xList.append(x)
            self.__tempLine.yList.append(y)
        else:
            print(self.__interSectList)
            print("theta update ", str(theta))
            if len(self.__tempLine.xList) < self.__linearThreshhold:
                self.__tempLine = Line()
                self.__tempLine.xList.append(x)
                self.__tempLine.yList.append(y)
                self.__lastTheta = theta
                return
            # there is theta change,  linear the saved samples        
            line = self.__linear(self.__tempLine)
            # a new line is generated, update lines
            self.__updateLines(line)
            print(self.__lines)
            # clear current data
            self.__tempLine = Line()
            self.__tempLine.xList.append(x)
            self.__tempLine.yList.append(y)
            self.__lastTheta = theta
        return 
     
    def __mergeTwoLines(self, srcLine, dstLine):
        xList = srcLine.xList + dstLine.xList
        yList = srcLine.yList + dstLine.yList
        tempLine = Line()
        tempLine.xList = xList
        tempLine.yList = yList
        return self.__linear(tempLine)         
        
    def __linear(self, tempLine):
        """
        Get line based on the theta, this function is called after sample finished
        """
        model = linear_model.LinearRegression()
        pointsX = np.array(tempLine.xList).reshape((len(tempLine.xList), 1))
        pointsY = np.array(tempLine.yList).reshape((len(tempLine.yList), 1))
        model.fit(pointsX[:], pointsY[:])
        
        # Predict data of estimated models
        lineX = np.arange(min(pointsX) -1, max(pointsX) +1)
        lineY = model.predict(lineX[:, np.newaxis])

        line = Line((lineX[0], int(lineY[0][0])), (lineX[len(lineX)-1], int(lineY[len(lineY)-1][0])))
        line.xList = tempLine.xList
        line.yList = tempLine.yList
        
        return line
    
    def __updateLines(self, line):
        """
        check if a new line should be inserted to lines or merged with existing line
        """
        # check the len of self.__lines
        if len(self.__lines) < 1:
            self.__lines.append(line)
            return 0  
        
        previousLine = self.__lines[-1]
        
        degree = self.__getLinesAngle(line, previousLine)
        if degree < self.__degreeThreshhold:
            print("angle %s degree less than %s merge with previous line" %(str(degree), self.__degreeThreshhold))         
            self.__lines[-1] = self.__mergeTwoLines(line, previousLine)
            return 0
                
        x, y = self.__lineIntersection(line, previousLine)        
        self.__interSectList.append((x, y)) 
        self.__lines.append(line)
        return 0

        
    def __getVectorFromLine(self, line):
        return [(line.startPoint[0] - line.endPoint[0]), (line.startPoint[1] - line.endPoint[1])]
        
    def __getLinesAngle(self, lineA, lineB):
        """
        get angle between two line
        http://stackoverflow.com/questions/28260962/calculating-angles-between-line-segments-python-with-math-atan2
        """
        # Get nicer vector form
        vA = self.__getVectorFromLine(lineA)
        vB = self.__getVectorFromLine(lineB)
        
        def dot(vA, vB):
            return vA[0]*vB[0]+vA[1]*vB[1]
        
        # Get dot prod
        dotProd = dot(vA, vB)
        # Get magnitudes
        magA = dot(vA, vA)**0.5
        magB = dot(vB, vB)**0.5
        # Get cosine value
        cos_ = dotProd/magA/magB
        # Get angle in radians and then convert to degrees
        angle = math.acos(dotProd/magB/magA)
        # Basically doing angle <- angle mod 360
        deg = math.degrees(angle)%180
        # just want to get the absolute degree
        return deg   
        
    def __lineIntersection(self, line1, line2):
        """
        http://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines-in-python
        http://blog.csdn.net/yangtrees/article/details/7965983
        """
        xdiff = (line1.startPoint[0] - line1.endPoint[0], line2.startPoint[0] - line2.endPoint[0])
        ydiff = (line1.startPoint[1] - line1.endPoint[1], line2.startPoint[1] - line2.endPoint[1]) #Typo was here

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
           return self.__InvalidPoint, self.__InvalidPoint

        d = (det(line1.startPoint, line1.endPoint), det(line2.startPoint, line2.endPoint))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return (int(x), int(y))
    
    def __getLinePoints(self, theta, dict):
        """
        Go through __thetaDict to get X list or Y list for lines
        """
        return dict[theta]        