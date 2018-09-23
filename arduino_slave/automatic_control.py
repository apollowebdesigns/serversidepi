import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from nanpy import (ArduinoApi, SerialManager, Ultrasonic)
from time import sleep
from sseclient import SSEClient

class AutomaticControl:
    def __init__(self, connection):
        self.ultrasonic = Ultrasonic(arduino_object.echo, arduino_object.trig, False, connection=connection)

    def get_distance(self):
        distance = self.ultrasonic.get_distance()
        print(distance)
        if distance < 5:
            # stop and turn
        else:
            # keep going