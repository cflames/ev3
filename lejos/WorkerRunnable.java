package test;

import java.io.*;
import java.net.Socket;

import test.Robot;
/**

 */
public class WorkerRunnable implements Runnable{

    protected Socket clientSocket = null;
    protected String serverText   = null;
    protected Robot  robot        = null;
    private  long currentTime = 0;
    private long irtime = 0;
    public  volatile boolean sample = false;
    private String samples = "";
    
    public WorkerRunnable(Socket clientSocket, String serverText, Robot robot) {
        this.clientSocket = clientSocket;
        this.serverText   = serverText;
        this.robot        = robot;
        
    }

    public void run() {
    	while(true){
	        try {
				BufferedReader in = new BufferedReader(new InputStreamReader(this.clientSocket.getInputStream()));
				PrintWriter out = new PrintWriter(this.clientSocket.getOutputStream(),true);
		
	            //Sending the response back to the client.				
				if (this.robot.getSampleStatus())
				{
					if ((System.currentTimeMillis()) - currentTime > 500)
					{
						currentTime = System.currentTimeMillis();
						this.robot.irDistance += this.robot.getIrDistance();
					   // System.out.println(samples);
					}
					
					
				    else{
					
				        try{
				            Thread.sleep(100);
				        }catch (Exception e) {}
				        
				    }
				
				}
				else{  //when robot sample is false, it means robot is not moving
					   //check if there is sample data
					   if ( this.robot.sampleString != "") {
						    out.println(this.robot.sampleString);
						    out.flush();
						    this.robot.sampleString = "";
					   }
					
				}
			
		        } catch (IOException e) {
		            //report exception somewhere.
		            e.printStackTrace();
		        }
	 
    	}
    }
}