package test;

import lejos.robotics.RangeFinder;
import lejos.hardware.ev3.LocalEV3;
import lejos.hardware.port.Port;
import lejos.hardware.sensor.EV3IRSensor;
import lejos.hardware.sensor.SensorModes;
import lejos.robotics.SampleProvider;

public class IRSensor implements RangeFinder
{

	 private SampleProvider distance;
    /* Constructor
     */
    public IRSensor()
    {
    	Port port = LocalEV3.get().getPort("S3");

    	// Get an instance of the Ultrasonic EV3 sensor
    	SensorModes sensor = new EV3IRSensor(port);

    	// get an instance of this sensor in measurement mode
    	this.distance= sensor.getMode("Distance");
    }

    /**
     * Read a distance from input
     * @return value  to be returned
     */	
    public float getRange()
    {
    	/* Calibrated 2011-12-14 */
    	//return (float) (4.56*getDistance()-0.69);
    	return getDistance();
    }
     
    /**
     * Read a range vector from input
     * @return value to be returned
     * @TODO Implement
     */
    public float[] getRanges()
    {
    	return null;
    }
   
    /**
     * Read a distance from input
     * @return value  to be returned
     */
    public float getDistance()
    {
    	// initialise an array of floats for fetching samples
    	float[] sample = new float[distance.sampleSize()];

    	// fetch a sample
    	this.distance.fetchSample(sample, 0);
    	return sample[0]; //convert to cm
    }
}