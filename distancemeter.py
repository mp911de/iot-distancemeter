__author__ = 'mp911de'


import RPi.GPIO as GPIO
import time
import numpy as np

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

CM_PER_SEC_AIR = 34300

# Setup GPIO
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
data = []

def percentile_based_outlier(point, threshold=95):

    if len(data) < 3:
        return False

    data.append(point)

    while len(data) < 10:
        data.pop()

    diff = (100 - threshold) / 2.0
    minval, maxval = np.percentile(data, [diff, 100 - diff])
    return (data < minval) | (data > maxval)


def get_distance_value():
    # Trigger High
    GPIO.output(GPIO_TRIGGER, True)
    # Trigger after 0.01ms to low
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    sonicSent = time.time()
    echoReceived = time.time()
    while GPIO.input(GPIO_ECHO) == 0:
        sonicSent = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        echoReceived = time.time()
    elapsed = echoReceived - sonicSent
    distance = (elapsed * CM_PER_SEC_AIR) / 2
    return distance


def get_distance():

    distance = get_distance_value()
    while percentile_based_outlier(distance):
        distance = get_distance_value()

    return distance


def cleanup():
    GPIO.cleanup()