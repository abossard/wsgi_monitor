from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
from werkzeug.wrappers import Request, Response
from werkzeug.debug import DebuggedApplication
import os
from flask import render_template
from jinja2 import Environment
#from jinja2_hamlpy import HamlPyExtension
from flask import Flask, render_template
from werkzeug import ImmutableDict
from jinja2 import nodes
from jinja2.ext import Extension
from haml_stuff import HamlPyExtension

HOST=os.environ['IP']
PORT=int(os.environ['PORT'])

from flask import Flask
app = Flask(__name__)
app.jinja_env.add_extension(HamlPyExtension)
app.debug = True

@app.route("/")
def index():
    return render_template('layout.haml', title="Geroge")

@app.route('/new', methods=['POST'])
def new():
    return "new"

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

class MonitorMiddleware(object):
    "Example middleware that appends a message to all 200 html responses"
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

app.wsgi_app = MonitorMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)