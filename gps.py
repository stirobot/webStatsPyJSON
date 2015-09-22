#gps sensor 
#for use with the seeed grove gps sensor (SIM28 based)
#uses UART (serial) 9600 8-N-1
import mraa, time, sys, signal, atexit
import pyupm_ublox6 as upmUblox6

def setupGPS(pin):
	gpsSensor = upmUblox6.Ublox6(pin)	
	if (not gpsSensor.setupTty(upmUblox6.cvar.int_B9600)):
		print "Failed to setup tty port parameters"
		sys.exit(0)
	return gpsSensor

def getLocation(gpssensor):
	bufferLength = 256
	nmeaBuffer = upmUblox6.charArray(bufferLength)
	if (gpsSensor.dataAvailable()):
		rv = gpsSensor.readData(nmeaBuffer, bufferLength)

		numlines= 0
		if (rv > 0):
			GPSData = ""
			# read only the number of characters
			# specified by myGPSSensor.readData
			for x in range(rv):
				GPSData += nmeaBuffer.__getitem__(x)

		if (rv < 0): # some sort of read error occured
			print "Port read error."
	return GPSData
