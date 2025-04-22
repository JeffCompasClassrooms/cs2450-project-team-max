import flask
from handlers import copy
from db import posts, users, helpers, groups
import os
import requests
import math
UPLOAD_FOLDER = os.path.abspath('static/uploads/')
blueprint = flask.Blueprint("login", __name__)



@blueprint.route('/loginscreen')
def loginscreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()
    # First check if already logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    
    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title,
            subtitle=copy.subtitle)

@blueprint.route('/login', methods=['POST'])
def login():
    """Log in the user.

    Using the username and password fields on the form, create, delete, or
    log in a user, based on what button they click.
    """
    db = helpers.load_db()
    #getting username
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    #creating a response for login,index
    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    #making sure username and password is not empty
    if username == "":
        flask.flash("invalid username", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    resp.set_cookie('username', username)
    if password == "":
        flask.flash("Invalid password", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    resp.set_cookie('password', password)
    submit = flask.request.form.get('type')
    if submit == 'Sign Up':
        if users.get_user(db, username, password) is None:
            for i in username:
                #checking if username is a character or a number
                if not i.isalpha() and not i.isdigit() and not i=='_':
                    resp.set_cookie('username', '', expires=0)
                    resp.set_cookie('password', '', expires=0)
                    flask.flash('Username not valid'.format(username), 'danger')
                    return flask.redirect(flask.url_for('login.loginscreen'))
           
            flask.flash('User {} created successfully!'.format(username), 'success')
            users.new_user(db,username,password)
            resp.set_cookie('password',password)
            resp.set_cookie('username',password)
            return flask.redirect(flask.url_for('profile.profile'))
        else:
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('Username is taken'.format(username), 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
    return resp



@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/index')
def index():
    """Serves the main feed page for the user."""
    db = helpers.load_db()
   
    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username == "" and password == "":
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash("Invalid credentials. If you're new, click the sign up button to become a member.", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

   
    # get the info for the user's feed
    group = groups.get_group(db,user['group'])
    friends = users.get_user_friends(db, user)
    all_posts = []
    all_posts += posts.get_posts(db, user)
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)
    return flask.render_template('feed.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts= sorted_posts, alerts=user['alerts'],group = user['group'])

def is_near(lat1, lon1, lat2, lon2, threshold_meters=1000000000):
    # Radius of Earth in meters
    R = 6371000

    # Convert degrees to radians
    l1 = math.radians(lat1)
    l2 = math.radians(lat2)
    l3 = math.radians(lat2 - lat1)
    l4 = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(l3 / 2)**2 + math.cos(l1) * math.cos(l2) * math.sin(l4 / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    # Debugging: print the distance and threshold
    print(f"Distance between ({lat1}, {lon1}) and ({lat2}, {lon2}) = {distance} meters")
    print(f"Threshold: {threshold_meters} meters")

    return distance <= threshold_meters

@blueprint.route('/static/uploads/<filename>')
def uploaded_file(filename):
    print("in")
    """Serve uploaded media files."""

    return flask.send_from_directory(UPLOAD_FOLDER, filename)

@blueprint.route('/explore')
def explore():
    db = helpers.load_db()
   
    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if username == "" and password == "":
        return flask.redirect(flask.url_for('login.loginscreen'))
    user = users.get_user(db, username, password)
    if not user:
        flask.flash("Invalid credentials. If you're new, click the sign up button to become a member.", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    all_users =users.get_all_users(db,user)
    threshold_meters = 1000000000
    filtered_users = [
        u for u in all_users 
        if is_near(user['latitude'], user['longitude'], u['latitude'], u['longitude'], threshold_meters)
    ]
    
    # Sort the remaining users by distance to the logged-in user
    filtered_sorted_users = sorted(
        filtered_users,
        key=lambda u: is_near(user['latitude'], user['longitude'], u['latitude'], u['longitude'])
    )
 
   
    # sort posts
   
    all_users =filtered_sorted_users
    return flask.render_template('explore.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,all_users = filtered_sorted_users,
            alerts=user['alerts'])
