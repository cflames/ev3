package test;


/*
 * Copyright (c) 1995, 2014, Oracle and/or its affiliates. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 *   - Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *
 *   - Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 *   - Neither the name of Oracle or the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */
 
import java.net.*;

import test.WorkerRunnable;

import java.io.*;
 
import test.Robot;

public class server {
    public static void main(String[] args) throws IOException {
       
    	
        int portNumber = 5000;
        int controlNumber = 5001;
        InetAddress addr = InetAddress.getByName("192.168.0.16");
        ServerSocket serverSocket = new  ServerSocket(portNumber, 50, addr);
        ServerSocket controlSocket = new  ServerSocket(controlNumber, 50, addr);
        System.out.println("Wait for connection on port " + Integer.toString(portNumber));
        
        Robot  robot = new Robot();
        //Init Robot
        System.out.println("Running...");
		robot.printToLCD("EV3-Remote");
		robot.leftMotor.setSpeed(100);
		robot.rightMotor.setSpeed(100);
		robot.servo1.setSpeed(70);
		robot.leftMotor.resetTachoCount();
        robot.rightMotor.resetTachoCount();
        robot.servo1.resetTachoCount();
		
        while(true){
            Socket clientSocket = null;
            Socket controlClient = null;
            
            try {
            	 clientSocket = serverSocket.accept();
            	 new Thread(
                         new WorkerRunnable(
                             clientSocket, "Multithreaded Server", robot)
                     ).start();
            	 controlClient = controlSocket.accept();
            	 new Thread(
                         new WorkerRunnable2(
                        		 controlClient, "Multithreaded Server", robot)
                     ).start();
            } catch (IOException e) {
                System.out.println("Exception caught when trying to listen on port "
                    + portNumber + " or listening for a connection");
                System.out.println(e.getMessage());
            }
            
         
           
        }
    }
}