import flask
from handlers import copy
from db import posts, users, helpers, groups
import os
import requests
import math
UPLOAD_FOLDER = os.path.abspath('static/uploads/')
blueprint = flask.Blueprint("signup", __name__)
@blueprint.route("/signup")
def signup():
    db = helpers.load_db()
    username= flask.request.cookies.get('username')
    password= flask.request.cookies.get('password')
    user= users.get_user(db,username,password)
    if user is not None:
        flask.flash('Must have an account', 'danger')
        return flask.redirect(flask.url_for('signup.signup'))
    return flask.render_template('create_account.html', title=copy.title,username =username )

@blueprint.route('/create', methods=['post'])
def create():
    db = helpers.load_db()
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if username =="" or username ==None:
        flask.flash('Username must be valid', 'danger')
        return flask.redirect(flask.url_for('signup.signup'))
    if password =="" or password ==None:
        flask.flash('Password must be valid', 'danger')
        return flask.redirect(flask.url_for('signup.signup'))
    resp = flask.make_response(flask.redirect(flask.url_for('profile.profileScreen')))
    if users.get_user(db, username, password) is None:
            for i in username:
                #checking if username is a character or a number
                if not i.isalpha() and not i.isdigit() and not i=='_':
                    resp.set_cookie('username', '', expires=0)
                    resp.set_cookie('password', '', expires=0)
                    flask.flash('Username not valid'.format(username), 'danger')
                    return flask.redirect(flask.url_for('signup.signup'))
            flask.flash('User {} created successfully!'.format(username), 'success')
            users.new_user(db,username,password)
            resp.set_cookie('password',password)
            resp.set_cookie('username',password)
            return resp
    flask.flash("username taken", 'danger')
    return flask.redirect(flask.url_for('login.login'))