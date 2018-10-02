import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from nanpy import (ArduinoApi, SerialManager, Ultrasonic)
from time import sleep
from sseclient import SSEClient
import logging
logging.basicConfig(filename='/home/pi/error.log',level=logging.DEBUG)

class AutomaticControl:
    TrigPin = 9
    EchoPin = 10

    def __init__(self, connection):
        self.ultrasonic = Ultrasonic(self.EchoPin, self.TrigPin, False, connection=connection)

    def get_distance(self):
        distance = self.ultrasonic.get_distance()
        return str(distance)