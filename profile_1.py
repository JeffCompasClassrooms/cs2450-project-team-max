import os
import time
import flask
import timeago

from handlers import profile

# app imports
app = flask.Flask(__name__)
app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
UPLOAD_FOLDER = 'static/profile'


os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())

# Register blueprints
app.register_blueprint(profile.blueprint)

# run app
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
