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
from arduino_slave.arduino_slave import ArduinoSlave
# import forwardsarrow
# import backwardsarrow

app = Flask(__name__)

# Allow CORS for client to access server sent events
CORS(app)

# research slave connection!
arduino_slave = ArduinoSlave('/dev/ttyACM0')

# Init vars for distance sensing



# Sensor set up
# arduino.pinMode(TrigPin,arduino.OUTPUT)
# arduino.pinMode(EchoPin,arduino.INPUT)

# Move the sensor forwards
# def sensor_distance():

#     # For automatic mode
#     messages = SSEClient('http://192.168.1.83/my_event_source')

#     arduino.digitalWrite(Motor1A,arduino.LOW)
#     arduino.digitalWrite(Motor2A,arduino.LOW)
#     arduino.digitalWrite(Motor1B,arduino.LOW)
#     arduino.digitalWrite(Motor2B,arduino.LOW)
#     # forwardsarrow.forwards()
#     count = 0

#     for msg in messages:
#         print('automatic message?')
#         print(msg)
#         messageString = str(msg)

#         if float(messageString) < 16:
#             # Move Right
#             arduino.digitalWrite(Motor1A,arduino.LOW)
#             arduino.digitalWrite(Motor1B,arduino.HIGH)
#             arduino.digitalWrite(Motor2A,arduino.HIGH)
#             arduino.digitalWrite(Motor2B,arduino.LOW)
#             gevent.sleep(0.2)
#             yield 'data: %s\n\n' % msg
#             count += 1

#         else:
#             # Forwards
#             arduino.digitalWrite(Motor1A,arduino.HIGH)
#             arduino.digitalWrite(Motor1B,arduino.LOW)
#             arduino.digitalWrite(Motor2A,arduino.HIGH)
#             arduino.digitalWrite(Motor2B,arduino.LOW)
#             gevent.sleep(0.2)
#             yield 'data: %s\n\n' % msg
#             count += 1


def event_end():
    count = 0
    while True:
        gevent.sleep(0.1)
        yield 'data: %s\n\n' % count
        count = 0

@app.route('/distance')
def sse_sensor_distance():
    return Response(
            sensor_distance(),
            mimetype='text/event-stream')

@app.route('/my_event_source')
def sse_request():
    return Response(
            arduino_slave.event_stream(),
            mimetype='text/event-stream')

@app.route('/backwards')
def sse_backwards():
    return Response(
            arduino_slave.move_backwards(),
            mimetype='text/event-stream')

@app.route('/right')
def sse_right():
    return Response(
            arduino_slave.move_right(),
            mimetype='text/event-stream')

@app.route('/left')
def sse_left():
    return Response(
            arduino_slave.move_left(),
            mimetype='text/event-stream')

@app.route('/end_motor_source')
def event_end():
    arduino_slave.kill_motors()
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
