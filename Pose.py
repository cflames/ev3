
class Pose():
    """
    Save Robot location
    """
    def __init__(self, x=0, y=0, theta=0):
        self.x = x
        self.y = y
        self.theta = theta  
       
    def getPose(self):
        return self.x, self.y, self.theta
        
    def __str__(self):
        return "Pose: %s %s %s"%(self.x, self.y, self.theta)
        
    def __eq__(self, other):
        if other is None:
            return False
        return self.x == other.x \
               and self.y == other.y \
               and self.theta == other.theta    