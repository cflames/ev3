import math
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch, call
from GridMap import GridMap

class GridMapTestCase(unittest.TestCase):
    def testUpdate(self):
        gridMap = GridMap(5, 5, 1)
        gridMap.update(2, 2, 90)
        result = []
        def drawFunc(x):
            result.append(x)
        gridMap.drawPoints(drawFunc)
        assert result[0] == (2, 2)
        gridMap.drawPoints(drawFunc)
        assert len(result) == 1
        
if __name__ == '__main__':
    unittest.main()