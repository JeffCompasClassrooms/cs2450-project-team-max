# std imports
import time

# installed imports
import flask
import timeago
 #import tinydb

# handlers
from handlers.profile import blueprint as profile_blueprint
app.register_blueprint(profile_blueprint)
from handlers import profile
import os

# app imports
app = flask.Flask(__name__)
UPLOAD_FOLDER = 'static/profile'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# db imports
from db import users, helpers
@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())
app.register_blueprint(profile.blueprint)
#app.register_blueprint(login.blueprint)
#app.register_blueprint(alerts.blueprint)

app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.run(debug=True, host='0.0.0.0')
