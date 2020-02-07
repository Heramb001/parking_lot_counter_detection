#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)


#--- parameters
LOT_OPEN = 150
LOT_CLOSE = 5

#--- set GPIO Pins
PIN_TRIGGER = 7 
PIN_ECHO = 11

#--- LED PINS 
RED = 12
GREEN = 13


#--- seting the pins
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
print('waiting for sensor to settle, calculate initial distance ')


def setGreen():
	GPIO.output(GREEN, GPIO.HIGH)
	GPIO.output(RED, GPIO.LOW)

def setRed():
	GPIO.output(GREEN, GPIO.LOW)
	GPIO.output(RED, GPIO.HIGH)

def getDistance():
	#--- set trigger pin to high
	GPIO.output(PIN_TRIGGER, GPIO.HIGH)	
	
	time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER,GPIO.LOW)
	
	pulse_start_time = time.time() 
	
        while GPIO.input(PIN_ECHO) == 0:
		pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
                pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
	
	return distance



if __name__ == '__main__':
	try:
		while True:
			dist = getDistance()
			print('--> Distance : '+str(dist)+' cm')
			time.sleep(0.5)
			if dist >= LOT_OPEN:
				setGreen()
			else:
				setRed()

	except KeyboardInterrupt: 	#--- press ctrl+c to exit the program
		print('Program stopped by user')
		GPIO.cleanup()
