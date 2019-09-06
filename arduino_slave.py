import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

import backwardsarrow
import forwardsarrow

gevent.monkey.patch_all()
from nanpy import (ArduinoApi, SerialManager, Ultrasonic)
from time import sleep
from pidata import get_all_data
import json


class ArduinoSlave():
    """Arduino slave construction setup"""
    Motor1A = 2
    Motor1B = 3
    Motor2A = 4
    Motor2B = 5

    TrigPin = 9
    EchoPin = 10

    ultrasonic = ''
    distance = 0

    automatic_mode = False

    def __init__(self, connection_path):
        try:
            connection = SerialManager(connection_path)
            self.arduino = ArduinoApi(connection=connection)
            self.ultrasonic = Ultrasonic(self.EchoPin, self.TrigPin, False, connection=connection)
        except:
            print("Failed to connect to the arduino")

        # Motors set up
        self.arduino.pinMode(self.Motor1A, self.arduino.OUTPUT)
        self.arduino.pinMode(self.Motor1B, self.arduino.OUTPUT)
        self.arduino.pinMode(self.Motor2A, self.arduino.OUTPUT)
        self.arduino.pinMode(self.Motor2B, self.arduino.OUTPUT)

        # Sensor set up
        self.arduino.pinMode(self.TrigPin, self.arduino.OUTPUT)
        self.arduino.pinMode(self.EchoPin, self.arduino.INPUT)

    def startGetDistance(self):
        self.distance = self.ultrasonic.get_distance()
        print(self.distance)
        # if distance < 5:
        #     pass
        # else:
        #     pass

        return float(self.distance)
        # sleep(0.002)

    def automatic_control(self):
        if (self.startGetDistance() < 5):
            self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor1B, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)
            sleep(0.5)
        else:
            self.arduino.digitalWrite(self.Motor1A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)

    def dists(self):
        count = 0
        while True:
            # distance test when moving forwards
            try:
                distance = self.startGetDistance()
                yield 'data: ' + str(distance) + '\n\n'
            except:
                yield 'data: there was an error!\n\n'
            count += 1

    def kill_motors(self):
        self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)

    def move_forwards(self, sense):
        self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)
        forwardsarrow.forwards()
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)

            # distance test when moving forwards
            try:
                distance = self.startGetDistance()
                print('distance retrieved successfully')
                raw_data = get_all_data(sense)
                raw_data['distance'] = distance
                yield 'data: %s\n\n' % json.dumps(raw_data)
            except:
                yield 'data: there was an error!\n\n'
            count += 1

    def move_backwards(self, sense):
        self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)
        backwardsarrow.backwards()
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor1B, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2B, self.arduino.HIGH)
            try:
                distance = self.startGetDistance()
                raw_data = get_all_data(sense)
                raw_data['distance'] = distance
                yield 'data: %s\n\n' % json.dumps(raw_data)
            except:
                yield 'data: there was an error!\n\n'
            count += 1

    def move_right(self, sense):
        self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor1B, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)
            try:
                distance = self.startGetDistance()
                raw_data = get_all_data(sense)
                raw_data['distance'] = distance
                yield 'data: %s\n\n' % json.dumps(raw_data)
            except:
                yield 'data: there was an error!\n\n'
            count += 1

    def move_left(self, sense):
        self.arduino.digitalWrite(self.Motor1A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B, self.arduino.LOW)
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A, self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor1B, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2A, self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2B, self.arduino.HIGH)
            try:
                raw_data = get_all_data(sense)
                distance = self.startGetDistance()
                raw_data['distance'] = distance
                yield 'data: %s\n\n' % json.dumps(raw_data)
            except:
                yield 'data: there was an error!\n\n'
            count += 1
