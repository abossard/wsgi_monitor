from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from werkzeug.wrappers import Request, Response
from werkzeug.debug import DebuggedApplication
import os

from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"


class MonitorMiddleware(object):
    "Example middleware that appends a message to all 200 html responses"
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

app = MonitorMiddleware(app)

httpd = make_server(os.environ['IP'], int(os.environ['PORT']), app)

httpd.handle_request()
