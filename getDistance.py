#!/usr/bin/python

import RPi.GPIO as GPIO
import os
import time

def sensorInit(TRIG, ECHO):
        # Initialize GPIO pins
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        # Wait for sensor to settle
        GPIO.output(TRIG, False)
        time.sleep(0.5)

def sensorDeinit():
        GPIO.cleanup()

def getDist(TRIG, ECHO):
        # Trigger a measurement
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        start_time = time.time()
        pulse_start = start_time

        # Time the pulse on echo, but return 0 on timeout
        while GPIO.input(ECHO)==0 and (pulse_start - start_time):
                pulse_start = time.time()

        if (pulse_start - start_time >= 500):
                return 0
        start_time = time.time()
        pulse_end = start_time

        while GPIO.input(ECHO)==1 and (pulse_end - start_time) < 500:
                pulse_end = time.time()

        if (pulse_end - start_time >= 500):
                return 0
        pulse_length = pulse_end - pulse_start

        # Multiply by ratio of cm to pulse length
        return round(pulse_length * 17150, 3)

# BEGIN MAIN
# Set GPIO pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# TRIG = GPIO 2
TRIG = 14
# ECHO = GPIO 3
ECHO = 15
# Set sensitivity from 0-1
# Set sensitivity from 0-1
SENSITIVITY = 0.8

sensorInit(TRIG, ECHO)

while 1:
#       time.sleep(10)
        os.system('omxplayer -o local /home/pi/seinfeld/seinfeld.mp3')
        print getDist(TRIG,ECHO), "cm"
        time.sleep(10)

# Establish a baseline measurement
meas = queue.Queue()
meas.put(getDist(TRIG, ECHO))

# Variables used for debouncing
mode = 0

# Only play seinfeld once every timeWait seconds
timeWait = 10
timeDelay = 0.02
timeCountMax = timeWait / timeDelay
timeCount = timeCountMax

compare = regDist * SENSITIVITY
try:
        while 1:
                dist = getDist(TRIG, ECHO)
                if ((dist < compare and lastDist < compare and lastLastDist < compare)) and mode==1:
                        # play seinfeld, not ok to play seinfeld again
                        # print "This is where seinfeld is played"

                        # Command is omxplayer -o local seinfeld.mp3
                        os.system('omxplayer -o local /home/pi/seinfeld/seinfeld.mp3')
                        # Reset time counter
                        timeCount = 0
                        mode = 0
                elif dist > compare and lastDist > compare and lastLastDist > compare and mode==0 and timeCount > timeCountMax:
                        # Now its ok to play seinfeld again, time permitting
                        mode = 1

                lastLastDist = lastDist
                lastDist = dist

                timeCount = timeCount + 1
                time.sleep(timeDelay)

finally:
        sensorDeinit()
        GPIO.cleanup()
# END OF MAIN