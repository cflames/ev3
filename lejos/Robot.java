package test;

/*
 * Michael duPont - flyinactor91.com
 * EV3-Remote - https://github.com/flyinactor91/EV3-Remote
 * Generic robot client
 * Lejos 0.8.0-alpha running on EV3
 * 
 * 2014-04-08
 * 
 * Commands recieved from Controller
 *     jrun Robot (-c)
 * Commands recieved from terminal
 *     jrun Robot -t
 * 
 * Commands separated by ';'
 * Available Commands:
 * 		Motors
 * 			Forward: 	F distance<int> (serial<def=Y /N>)
 * 			Backward: 	B distance<int> (serial<def=Y /N>)
 * 			Left:		L degree<int> (serial< def=Y /N>)
 * 			Right:		R degree<int> (serial< def=Y /N>)
 * 			Servo:		S motor<1/2> degree<int +/-> (serial< def=Y /N>)
 * 			MotorSpd:	MS motor<M/S1/S2> speed<int>				#Main (A and B) / Servos (C and D)
 *		Sound
 * 			Volume:		VOL percent<int 0-100>					#Buzzer/TONE doesn't work if volume less than 8%
 * 			Tone:		TONE freq-Hz<int> duration-ms<int>
 * 			Beep:		BEEP pattern<int 1-5>
 * 			Song:		WAV song<*.wav>							#Song.wav location
 *		Utils
 * 			Pause:		P duration-ms<int>
 * 			LED Disp:	LED pattern<int 0-9>
 * 			Battery:	BAT										#Displays the battery level (terminal/LCD)
 * 			Quit:		QUIT
 * 
 * Example: F 1000 N;LED 8;S 1 300;P 2000;L 220;B 300;S 1 -300;BEEP 5;QUIT
 * 
 * Notes:
 * 		LED patterns:
 * 			0 = Off , 1 = Green , 2 = Red , 3 = Orange
 * 			4-6 = Even pulses , 7-9 Heartbeat pulses
 * 		Beep patterns:
 * 			1 = beep , 2 = two beeps , 3 = buzzer
 * 			4 = ascending beeps , 5 = descending beeps
 */

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