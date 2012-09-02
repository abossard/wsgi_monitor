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

data = list()
monitor_url = 'http://wsgi_monitor.abossard.c9.io/new?_skip_monitor=true'

def add_data_to_list(entry):
    #req = urllib2.Request(url=monitor_url,data=json.dumps(entry))
    #urllib2.urlopen(req)
    data.append(entry)

@app.route("/")
def index():
    #Thread(target=add_data_to_list, args=["Thread",]).start()
    return render_template('layout.haml', title="Geroge", data=data)

@app.route('/new', methods=['POST','GET'])
def new():
    if request.method == 'GET':
        pass #return redirect(url_for('index'))
    data.append(str(request.form))
    return data
    #return redirect(url_for('index'))

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

from threading import Thread

class MonitorMiddleware(object):
    "Example middleware that appends a message to all 200 html responses"

    def __init__(self, myapp):
        self.app = myapp
    def __call__(self, environ, start_response):
        #qs = parse_qs(environ['QUERY_STRING'])
        response = self.app(environ, start_response)
        if environ['PATH_INFO'] != '/new':
            entry = dict((k, v) for k, v in environ.items() if isinstance(v, str))
            entry['RESPONSE']=response
            Thread(target=add_data_to_list, args=[entry,]).start()
        return response

    def post(self, data):
        req = urllib2.Request(url=self.monitor_url,
                data=json.dumps(data))
        urllib2.urlopen(req)

app.wsgi_app = MonitorMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)