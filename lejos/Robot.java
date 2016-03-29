package test;


import java.io.*;
import java.net.Socket;
import java.net.ServerSocket;
import java.util.Scanner;
import lejos.hardware.Button;
import lejos.hardware.lcd.LCD;
import lejos.hardware.port.MotorPort;
import lejos.robotics.RegulatedMotor;
import lejos.hardware.motor.EV3LargeRegulatedMotor;
import lejos.hardware.motor.EV3MediumRegulatedMotor;
import lejos.hardware.Sound;
import lejos.hardware.Battery;
import lejos.utility.Delay;
import test.RangeSensor;

import java.net.InetAddress;

class Robot {
	
	static Boolean toLCD = false;  //Printing to screen as is interferes with the new screen UI
	
	static RegulatedMotor leftMotor = new EV3LargeRegulatedMotor(MotorPort.C);
	static RegulatedMotor rightMotor = new EV3LargeRegulatedMotor(MotorPort.A);
	static RegulatedMotor servo1 = new EV3MediumRegulatedMotor(MotorPort.D);
	static RangeSensor sensor = new RangeSensor();
	static IRSensor irSensor = new IRSensor();
	static boolean smooth = false;
    public  volatile boolean sample = false;
    static  String irDistance = " ";
    public volatile String sampleString = "";
	//static RegulatedMotor servo2 = new EV3MediumRegulatedMotor(MotorPort.D);
	
	public static void printToLCD(String txt) {
		LCD.clear();
		LCD.drawString(txt , 0 , 0);
	}
	
	//Controls main/movement motors. Direction = "Forward" || "Backward" || "Left" || "Right"
	//New positions are both calculated early to minimize lag time between motor A init and motor B init
	public static boolean Move(String direction) {

		if (direction.equals("Stop")) {
			rightMotor.stop(true);
			leftMotor.stop(true);
			
			return true;
		}
		if (direction.equals("Forward")) {
			leftMotor.forward();
			rightMotor.forward();
			return true;
		}

		if (direction.equals("Right")) {
			rightMotor.backward();
			leftMotor.forward();
			return true;
		}
		if (direction.equals("Left")) {
			rightMotor.forward();
			leftMotor.backward();
			return true;
		}		
		return true;

	}

	public String getSample() {
		int wheelA = this.leftMotor.getTachoCount();
		int wheelB = this.rightMotor.getTachoCount();

		return wheelA + "," + wheelB;
	}
	
	public void setLeftSpeed(int speed){
		this.leftMotor.setSpeed(speed);
	}
	
	public void setRightSpeed(int speed){
		this.rightMotor.setSpeed(speed);
	}
	
	public String getDistance() {
		
		int dist = (int) this.sensor.getRange();
		int sensor = this.servo1.getTachoCount();
		return  this.getSample() + "," + this.irDistance + "," + dist + " "  + sensor;
	}
	
	public String getIrDistance() {
	     float dist = this.irSensor.getRange();
	     return dist + " ";
	}
	
	public void resetWallSample(){
		this.irDistance = " ";
	}
	
	public boolean getSampleStatus(){
	    return this.sample;
	}
	
	public void setSampleStatus(Boolean status){
		this.sample = status;
	}
	
	public boolean turnLeft(int degrees){
	     this.rightMotor.rotate(degrees, true);
	     this.leftMotor.rotate(-degrees);
	     return true;
	}
	public boolean turnRight(int degrees){
	     this.leftMotor.rotate(degrees, true);
	     this.rightMotor.rotate(-degrees);
	     return true;
	}
	
    public boolean rotateLeftMotor(int degrees){
    	
    	this.rightMotor.rotate(degrees);
    	return true;
    }
	
    public boolean moveFowardMotor(int degrees){
    	this.irDistance = " " + this.irSensor.getRange();
    	this.rightMotor.rotate(degrees, true);
    	this.leftMotor.rotate(degrees);
    	//System.out.println("rotate finished");
    	this.irDistance = this.irDistance + "," +  this.irSensor.getRange();
    	return true;
    }
	//Controls non-movement motor. Unit can be + or -
	public boolean Servo() {
 
        
        try{
            Thread.sleep(300);
        }catch (Exception e) {}
        
		servo1.rotate(30);
		servo1.rotate(-60);
		servo1.rotate(30);
		servo1.resetTachoCount();
		servo1.stop();
		

		
		return true;
		
	}
	

}
