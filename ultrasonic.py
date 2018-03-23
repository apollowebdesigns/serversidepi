import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from nanpy import (ArduinoApi, SerialManager)
from time import sleep
from flask import Flask, request, Response, render_template
from flask_cors import CORS
from sense_hat import SenseHat
import forwardsarrow
import backwardsarrow

# Using distance sensor

TrigPin = 9
EchoPin = 10

try:
    connection = SerialManager()
    arduino = ArduinoApi(connection = connection)
except:
    print("Failed to connect to the arduino")

# Sensor set up
arduino.pinMode(TrigPin,arduino.OUTPUT)
arduino.pinMode(EchoPin,arduino.INPUT)

while True:
    arduino.digitalWrite(TrigPin, arduino.LOW)
    sleep(0.02)
    arduino.digitalWrite(TrigPin, arduino.HIGH)
    sleep(0.1)
    arduino.digitalWrite(TrigPin, arduino.LOW)
    duration = arduino.digitalRead(EchoPin);
    distance = (duration*0.0343)/2;
    print('testing the loop')
    print(duration)
    print(distance)