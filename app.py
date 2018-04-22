import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()
from nanpy import (ArduinoApi, SerialManager)
from time import sleep
from flask import Flask, request, Response, render_template
from flask_cors import CORS
from sense_hat import SenseHat
from sseclient import SSEClient
import forwardsarrow
import backwardsarrow

app = Flask(__name__)

# Allow CORS for client to access server sent events
CORS(app)

Motor1A = 2
Motor1B = 3
Motor2A = 4
Motor2B = 5

# Using distance sensor

TrigPin = 9
EchoPin = 10

# Init vars for distance sensing


# Connecting to the Arduino
try:
    connection = SerialManager()
    arduino = ArduinoApi(connection = connection)
except:
    print("Failed to connect to the arduino")

# Motors set up
arduino.pinMode(Motor1A,arduino.OUTPUT)
arduino.pinMode(Motor1B,arduino.OUTPUT)
arduino.pinMode(Motor2A,arduino.OUTPUT)
arduino.pinMode(Motor2B,arduino.OUTPUT)

# Sensor set up
arduino.pinMode(TrigPin,arduino.OUTPUT)
arduino.pinMode(EchoPin,arduino.INPUT)

def sensor_distance():
    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)
    forwardsarrow.forwards()
    count = 0
    messages = SSEClient('http://192.168.1.67/my_event_source')

    # TODO evaluate messages inside the loop
    for msg in messages:
        if msg < 5:
            # Stop
            arduino.digitalWrite(Motor1A,arduino.LOW)
            arduino.digitalWrite(Motor2A,arduino.LOW)
            arduino.digitalWrite(Motor1B,arduino.LOW)
            arduino.digitalWrite(Motor2B,arduino.LOW)

            # Move right
            arduino.digitalWrite(Motor1A,arduino.LOW)
            arduino.digitalWrite(Motor1B,arduino.HIGH)
            arduino.digitalWrite(Motor2A,arduino.HIGH)
            arduino.digitalWrite(Motor2B,arduino.LOW)

            sleep(0.5)

            # Stop
            arduino.digitalWrite(Motor1A,arduino.LOW)
            arduino.digitalWrite(Motor2A,arduino.LOW)
            arduino.digitalWrite(Motor1B,arduino.LOW)
            arduino.digitalWrite(Motor2B,arduino.LOW)

        gevent.sleep(0.01)
        print(msg)
        arduino.digitalWrite(Motor1A,arduino.HIGH)
        arduino.digitalWrite(Motor1B,arduino.LOW)
        arduino.digitalWrite(Motor2A,arduino.HIGH)
        arduino.digitalWrite(Motor2B,arduino.LOW)
        yield 'data: %s\n\n' % count
        count = messages

def kill_motors():
    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)

def event_stream():
    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)
    forwardsarrow.forwards()
    count = 0
    while True:
        gevent.sleep(0.01)
        arduino.digitalWrite(Motor1A,arduino.HIGH)
        arduino.digitalWrite(Motor1B,arduino.LOW)
        arduino.digitalWrite(Motor2A,arduino.HIGH)
        arduino.digitalWrite(Motor2B,arduino.LOW)
        yield 'data: %s\n\n' % count
        count += 1

def move_backwards():
    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)
    backwardsarrow.backwards()
    count = 0
    while True:
        gevent.sleep(0.01)
        arduino.digitalWrite(Motor1A,arduino.LOW)
        arduino.digitalWrite(Motor1B,arduino.HIGH)
        arduino.digitalWrite(Motor2A,arduino.LOW)
        arduino.digitalWrite(Motor2B,arduino.HIGH)
        yield 'data: %s\n\n' % count
        count += 1

def move_right():
    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)
    count = 0
    while True:
        gevent.sleep(0.01)
        arduino.digitalWrite(Motor1A,arduino.LOW)
        arduino.digitalWrite(Motor1B,arduino.HIGH)
        arduino.digitalWrite(Motor2A,arduino.HIGH)
        arduino.digitalWrite(Motor2B,arduino.LOW)
        yield 'data: %s\n\n' % count
        count += 1

def move_left():
    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)
    count = 0
    while True:
        gevent.sleep(0.01)
        arduino.digitalWrite(Motor1A,arduino.HIGH)
        arduino.digitalWrite(Motor1B,arduino.LOW)
        arduino.digitalWrite(Motor2A,arduino.LOW)
        arduino.digitalWrite(Motor2B,arduino.HIGH)
        yield 'data: %s\n\n' % count
        count += 1

def event_end():
    count = 0
    while True:
        gevent.sleep(0.1);
        yield 'data: %s\n\n' % count
        count = 0

@app.route('/my_event_source')
def sse_request():
    return Response(
            event_stream(),
            mimetype='text/event-stream')

@app.route('/backwards')
def sse_backwards():
    return Response(
            move_backwards(),
            mimetype='text/event-stream')

@app.route('/right')
def sse_right():
    return Response(
            move_right(),
            mimetype='text/event-stream')

@app.route('/left')
def sse_left():
    return Response(
            move_left(),
            mimetype='text/event-stream')

@app.route('/end_motor_source')
def event_end():
    arduino.pinMode(Motor1A,arduino.OUTPUT)
    arduino.pinMode(Motor1B,arduino.OUTPUT)
    arduino.pinMode(Motor2A,arduino.OUTPUT)
    arduino.pinMode(Motor2B,arduino.OUTPUT)

    arduino.digitalWrite(Motor1A,arduino.LOW)
    arduino.digitalWrite(Motor2A,arduino.LOW)
    arduino.digitalWrite(Motor1B,arduino.LOW)
    arduino.digitalWrite(Motor2B,arduino.LOW)
    kill_motors()
    sense = SenseHat()
    sense.clear()
    print('entered!!')
    return 'end'

@app.route('/')
def page():
    return render_template('index.html')

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()