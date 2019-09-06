import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from time import sleep
from flask import Flask, request, Response, render_template
import json
from flask_cors import CORS
from sense_hat import SenseHat
from arduino_slave import ArduinoSlave
from pidata import get_all_data
import logging
logging.basicConfig(filename='/home/pi/error.log',level=logging.DEBUG)


import forwardsarrow
import backwardsarrow

app = Flask(__name__)

# Allow CORS for client to access server sent events
CORS(app)

# research slave connection!
arduino_slave = ArduinoSlave('/dev/ttyACM0')


@app.route('/distance')
def sse_distance():
    arduino_slave.automatic_mode = True
    print('the endpoint has been called')
    while arduino_slave.automatic_mode:
        print('it is true inside the endpoint')
        arduino_slave.automatic_control()
        sleep(0.002)
    return {}


@app.route('/manual')
def sse_manual():
    arduino_slave.automatic_mode = False
    arduino_slave.kill_motors()
    return {}


@app.route('/forwards')
def sse_forwards():
    sense = SenseHat()
    sense.clear()
    forwardsarrow.forwards()
    return Response(
            arduino_slave.move_forwards(sense),
            mimetype='text/event-stream')


@app.route('/backwards')
def sse_backwards():
    sense = SenseHat()
    sense.clear()
    backwardsarrow.backwards()
    return Response(
            arduino_slave.move_backwards(sense),
            mimetype='text/event-stream')


@app.route('/right')
def sse_right():
    sense = SenseHat()
    sense.clear()
    return Response(
            arduino_slave.move_right(sense),
            mimetype='text/event-stream')


@app.route('/left')
def sse_left():
    sense = SenseHat()
    sense.clear()
    return Response(
            arduino_slave.move_left(sense),
            mimetype='text/event-stream')


@app.route('/end_motor_source')
def event_end():
    arduino_slave.kill_motors()
    logging.debug('hit?')
    sense = SenseHat()
    sense.clear()
    print('entered!!')
    return 'end'


@app.route('/get_pi_temp')
def get_temperature_of_pi():
    sense = SenseHat()
    sense.clear()
    data = get_all_data(sense)
    response = app.response_class(response=json.dumps(data),
                                  status=200,
                                  mimetype='application/json')
    return response


@app.route('/')
def page():
    return render_template('index.html')


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 80), app)
    http_server.serve_forever()
