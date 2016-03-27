package test;

import java.io.*;
import java.net.Socket;

import test.Robot;
/**

 */
public class WorkerRunnable2 implements Runnable{

    protected Socket clientSocket = null;
    protected String serverText   = null;
    protected Robot  robot        = null;
    private  long currentTime = 0;

    
    public WorkerRunnable2(Socket clientSocket, String serverText, Robot robot) {
        this.clientSocket = clientSocket;
        this.serverText   = serverText;
        this.robot        = robot;
        
    }

    public void run() {
    	while(true){
	        try {
				BufferedReader in = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
				PrintWriter out = new PrintWriter(this.clientSocket.getOutputStream(),true);
		
				
				if (in.ready()) {
					String stringIn = in.readLine();
	 
					if (stringIn == null) {
						System.out.println("\nClient is disconnect");
						break;
					}
				    
					//System.out.println("\nreceived: " + stringIn);
					String[] cmd = stringIn.split(" ");
					switch (cmd[0]) {
					    case "left":
					    	 //System.out.println("\nturn " + cmd[1]);
					    	 this.robot.setSampleStatus(true);
					    	 if(this.robot.turnLeft(Integer.parseInt(cmd[1])))
					    	 {
						    		this.robot.setSampleStatus(false);
						    		//out.println(this.robot.getDistance() + ","+ currentTime + " end");
						    		this.robot.sampleString = (this.robot.getDistance() + ","+ currentTime + " end");
						    		this.robot.resetWallSample();
						    		//out.flush();
					    	 }
					    	 break;
					    case "foward":
					    	this.robot.setSampleStatus(true);
					    	if(this.robot.moveFowardMotor(Integer.parseInt(cmd[1]))){
					    		//System.out.println("\nmove finished ");
					    		this.robot.setSampleStatus(false);
					    		//out.println(this.robot.getDistance() + ","+ currentTime + " end");
					    		this.robot.sampleString = (this.robot.getDistance() + ","+ currentTime + " end");
					    		this.robot.resetWallSample();
					    		//out.flush();
					    	}
					    	break;
					    case "speed":
					    	 //System.out.println("\n " + cmd[1] +" " + cmd[2]);
					    	 this.robot.setLeftSpeed(Integer.parseInt(cmd[1]));
					    	 this.robot.setRightSpeed(Integer.parseInt(cmd[2]));
					    	 break;					    	
					    case "right":
					    	 //System.out.println("\nturn " + cmd[1]);
					    	 this.robot.setSampleStatus(true);
					    	 if(this.robot.turnRight(Integer.parseInt(cmd[1])))
					    	 {
						    		this.robot.setSampleStatus(false);
						    		//out.println(this.robot.getDistance() + ","+ currentTime + " end");
						    		this.robot.sampleString = (this.robot.getDistance() + ","+ currentTime + " end");
						    		this.robot.resetWallSample();
						    		//out.flush();
					    	 }
					    	 break;
					    case "up":
					    	 this.robot.setSampleStatus(true);
					    	 this.robot.Move("Forward");
					    	 break;				 
					    case "stop":
					    	 this.robot.setSampleStatus(false);
					    	 this.robot.Move("Stop");
					    	 this.robot.sampleString = (this.robot.getDistance() + ","+ currentTime + " end");			    	 
					    	 break;
					    case "turnleft":
					    	 this.robot.setSampleStatus(true);
					    	 this.robot.Move("Left");			    	 
					    	 break;	
					    case "turnright":
					    	 this.robot.setSampleStatus(true);
					    	 this.robot.Move("Right");			    	 
					    	 break;							    	 
					    case "measure":
					    	 this.robot.Servo();
					    	 break;
					    	 
					    case "quit":
					    	 System.exit(0);
					}
					
				}
		        } catch (IOException e) {
		            //report exception somewhere.
		            e.printStackTrace();
		        }
	 
    	}
    }
}