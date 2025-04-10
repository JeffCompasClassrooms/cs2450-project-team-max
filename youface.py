# std imports
import time

# installed imports
import flask
import timeago
import tinydb
import requests
# handlers
from handlers import intro, friends, login, posts, alerts, groups, settings
import os
app = flask.Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.template_filter('get_location')
def getlocation(latlon):
    lat, lon = latlon
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    headers = {'User-Agent': 'MyReverseGeocoderApp/1.0'}  # Required by OpenStreetMap
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("display_name", "Address not found")
    else:
        return f"Error: {response.status_code}"
@app.template_filter('convert_time')
def convert_time(ts):
    """A jinja template helper to convert timestamps to timeago."""
    return timeago.format(ts, time.time())

app.register_blueprint(intro.blueprint)
app.register_blueprint(friends.blueprint)
app.register_blueprint(login.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(alerts.blueprint)
app.register_blueprint(groups.blueprint)
app.register_blueprint(settings.blueprint)
app.secret_key = 'mygroup'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.run(debug=True, host='0.0.0.0', port=5000)
