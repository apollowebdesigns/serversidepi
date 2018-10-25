import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from nanpy import (ArduinoApi, SerialManager, Ultrasonic)
from time import sleep

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

    def __init__(self, connection_path):
        try:
            connection = SerialManager(connection_path)
            self.arduino = ArduinoApi(connection = connection)
            self.ultrasonic = Ultrasonic(self.EchoPin, self.TrigPin, False, connection=connection)
        except:
            print("Failed to connect to the arduino")

        # Motors set up
        self.arduino.pinMode(self.Motor1A,self.arduino.OUTPUT)
        self.arduino.pinMode(self.Motor1B,self.arduino.OUTPUT)
        self.arduino.pinMode(self.Motor2A,self.arduino.OUTPUT)
        self.arduino.pinMode(self.Motor2B,self.arduino.OUTPUT)

        # Sensor set up
        self.arduino.pinMode(self.TrigPin,self.arduino.OUTPUT)
        self.arduino.pinMode(self.EchoPin,self.arduino.INPUT)

    def startGetDistance(self):
        self.distance = self.ultrasonic.get_distance()
        print(self.distance)
        # if distance < 5:
        #     pass
        # else:
        #     pass
        return self.distance
        # sleep(0.002)


    def dists(self):
        count = 0
        while True:
            # distance test when moving forwards
            try:
                distance = self.startGetDistance()
                yield 'data: ' + distance + '\n\n'
            except:
                yield 'data: there was an error!\n\n'
            count += 1


    def kill_motors(self):
        self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)

    def event_stream(self):
        self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)
        # forwardsarrow.forwards()
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A,self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2A,self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)
            
            # distance test when moving forwards
            try:
                distance = self.startGetDistance()
                yield 'data: ' + distance + '\n\n'
            except:
                yield 'data: there was an error!\n\n'
            count += 1

    def move_backwards(self):
        self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)
        # backwardsarrow.backwards()
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor1B,self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2B,self.arduino.HIGH)
            try:
                distance = self.startGetDistance()
                yield 'data: ' + distance + '\n\n'
            except:
                yield 'data: there was an error!\n\n'
            count += 1

    def move_right(self):
        self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor1B,self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2A,self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)
            yield 'data: %s\n\n' % count
            count += 1

    def move_left(self):
        self.arduino.digitalWrite(self.Motor1A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
        self.arduino.digitalWrite(self.Motor2B,self.arduino.LOW)
        count = 0
        while True:
            gevent.sleep(0.01)
            self.arduino.digitalWrite(self.Motor1A,self.arduino.HIGH)
            self.arduino.digitalWrite(self.Motor1B,self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2A,self.arduino.LOW)
            self.arduino.digitalWrite(self.Motor2B,self.arduino.HIGH)
            yield 'data: %s\n\n' % count
            count += 1