package test;

import lejos.robotics.RangeFinder;
import lejos.hardware.ev3.LocalEV3;
import lejos.hardware.port.Port;
import lejos.hardware.sensor.NXTUltrasonicSensor;
import lejos.hardware.sensor.SensorModes;
import lejos.robotics.SampleProvider;

public class RangeSensor  implements RangeFinder
{
    /** Device address of the chip */
    private SampleProvider distance;

    /* Constructor
     */
    public RangeSensor()
    {
    	Port port = LocalEV3.get().getPort("S1");

    	// Get an instance of the Ultrasonic EV3 sensor
    	SensorModes sensor = new NXTUltrasonicSensor(port);

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
    	return sample[0]*100; //convert to cm
    }
}