#client
from server import MonitorMiddleware

import urllib2
from urlparse import parse_qs
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from werkzeug.wrappers import Request, Response
from werkzeug.debug import DebuggedApplication
import os
from flask import render_template
from jinja2 import Environment
from jinja2_hamlpy import HamlPyExtension
from flask import Flask, render_template
from werkzeug import ImmutableDict
from jinja2 import nodes
from jinja2.ext import Extension
import json
HOST=os.environ['IP']
PORT=int(os.environ['PORT'])

from flask import Flask
from flask import request, redirect, url_for

app = Flask(__name__)
app.jinja_env.add_extension(HamlPyExtension)
app.debug = True

@app.route("/")
def index():
    return "Well, Hello!"

app.wsgi_app = MonitorMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)