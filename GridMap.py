
import numpy as np

class GridMap():
    """
    Map class 
	"""
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.cellSize = size
        self.__map = np.zeros((self.width,self.heigh))
        
    def update(self, x, y):
        self.__map[x][y] = 1