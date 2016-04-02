import numpy as np
from queue import Queue
import math

from Linear import Linear

class GridMap():
    """
    Map class 
	"""
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.cellSize = size
        self.__map = np.zeros((self.width,self.height))
        self.__drawQueue = Queue()
        
        self.linear = Linear()

        
    def update(self, x, y, theta):
        self.__map[x][y] = 1
        self.__drawQueue.put((x,y))
        
        #theta = round(theta, 2)
        #self.linear.update(x, y, theta)
        
    def getPoints(self):
        points = []
        while not self.__drawQueue.empty():
            points.append(self.__drawQueue.get())
        
        return points
        
    def drawPoints(self, drawFunc):
        """
        draw the points by callback function drawFunc
        """
        if self.__drawQueue.empty():
            return 
        drawFunc(self.__drawQueue.get())
        
