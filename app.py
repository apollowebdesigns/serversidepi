import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer
gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template

app = Flask(__name__)

def event_stream():
    count = 0
    while True:
        gevent.sleep(0.1)
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

@app.route('/end_motor_source')
def event_end():
    #kill gipo
    print('entered!!')

    return 'end'

@app.route('/')
def page():
    return render_template('index.html')

if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 8001), app)
    http_server.serve_forever()