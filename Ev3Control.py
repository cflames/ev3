import socket
import pygame, sys
import time
from SimpleSocket import SimpleSocket    

conn = SimpleSocket()
conn.connect("192.168.0.16", 5001)
conn.sock.setblocking(0)

pygame.init()
pygame.display.set_caption('Ev3 Keyboard Control')
size = [400, 400]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
 
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # check if key is pressed
        # if you use event.key here it will give you error at runtime
        if event.type == pygame.KEYUP:
            conn.mysend("stop\n")
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:             
                conn.mysend("turnleft\n")
            if event.key == pygame.K_RIGHT:                
                conn.mysend("turnright\n")
            if event.key == pygame.K_UP:
                conn.mysend("up\n")
            if event.key == pygame.K_a:
                conn.mysend("measure\n")      
            if event.key == pygame.K_q:
                conn.mysend("quit\n")            
            # checking if left modifier is pressed
            
    clock.tick(20)