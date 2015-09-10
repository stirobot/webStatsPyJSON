#OBD II data using pyobd
import obd
from obd import OBDCommand
from obd.utils import unhex

#call this from the main program...because we only want to do it once
def setupOBD():
	connection = obd.OBD('/dev/rfcomm0')
	while not(connection.is_connected()):
		connection = obd.OBD('/dev/rfcomm0') 
		#try indefinitely to connect
	return

def rpm():
	response = connection.query(obd.commands.RPM)
	return response.value

def engine_load():
	response = connection.query(obd.commands.ENGINE_LOAD)
	return response.value

def coolant_temp():
	response = connection.query(obd.commands.COOLANT_TEMP)
	return response.value

def intake_pressure():
	response = connection.query(obd.commands.INTAKE_PRESSURE)
	return response.value 

def speed():
	response = connection.query(obd.commands.SPEED)
	return response.value

def timing_advance():
	response = connection.query(obd.commands.TIMING_ADVANCE)
	return response.value

def intake_temp():
	response = connection.query(obd.commands.INTAKE_TEMP)
	return response.value

def throttle_pos():
	response = connection.query(obd.commands.THROTTLE_POS)
	return response.value

def voltage():
	response = connection.query(obd.commands.[1][42])
	readyresponse = unhex(response)
	return readyresponse #needs to be tested with a real car...not sure if this will work