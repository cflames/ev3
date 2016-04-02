import pygame, sys
import time
import math
from GridMap import GridMap
from Robot import Robot
from RobotConnection import RobotConnection
from Message import RobotMessage 
from Pose import Pose
from Linear import Line
 
def guiInit(width, height):
    pygame.init()
    pygame.display.set_caption('Ev3 Map')
    size = [width, height]
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255))
    
 
if __name__ == '__main__':
    # frame delay ms
    delay = 20
    width = 600
    height = 600
    ev3Ip = "192.168.0.16"
    ev3Port = 5000
    

    
    robot = Robot()
    robot.pose = Pose(500, 100, 90*math.pi/180)
    robot.poseList.append(robot.pose)
    map = GridMap(600, 600, 1)
    robotConn = RobotConnection()
    robotConn.remoteIp = ev3Ip
    robotConn.remotePort = ev3Port
    robotConn.rawDataFileName = "rawdata/data_map3"
    robotConn.connectToEv3(simulate=True)
    
    message = RobotMessage()

    pygame.init()
    pygame.display.set_caption('Ev3 Map')
    size = [width, height]
    screen = pygame.display.set_mode(size)
    screen.fill((255,255,255))
    clock = pygame.time.Clock()
    pygame.display.flip()      
    
    sx, sy, lx, ly, rx, ry = robot.getRobotShape(robot.pose)
    print(sx, sy, lx, ly, rx, ry)
    pygame.draw.polygon(screen,(255,0,0),((rx,ry),(lx,ly),(sx,sy)),2)    
    pygame.display.flip() 
    pygame.event.clear()    
    clock.tick(60)

    lines = []    
    while True:
        pygame.event.clear()
        # get message from robotConnection
        message = robotConn.readMessage(simulate=True)        
            
        if message is None:
            pygame.event.pump()
            clock.tick(20)
            continue
        # make robot motion
        if message.type == "Left":
            robot.motion(message)
            # get sample points after motion
            robot.updateMap(message, map.update)            
        elif message.type == "Corner":
            robot.updateCorner(message, map.update)
        else:
            print("Error message type")
            continue
        # get sample points after motion
        robot.updateMap(message, map.update)
        # Draw Robot
        print(robot.pose)
        sx, sy, lx, ly, rx, ry = robot.getRobotShape(robot.pose)
        pygame.draw.polygon(screen,(255,0,0),((rx,ry),(lx,ly),(sx,sy)),2)
        # Draw map
        points = []
        points = map.getPoints()
        for point in points:
            pygame.draw.circle(screen,(0,0,0),point,2)
        pygame.display.flip()        
        

        pygame.event.pump()
        clock.tick(20)

        
        
  
    
 