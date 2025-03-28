import flask
from handlers import copy
from db import posts, users, helpers
UPLOAD_FOLDER = 'static/uploads'
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
    if username is "":
        flask.flash("invalid username", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    resp.set_cookie('username', username)
    if password is "":
        flask.flash("Invalid password", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    resp.set_cookie('password', password)
    submit = flask.request.form.get('type')
    if submit == 'Sign Up':
        if users.get_user(db, username, password) is None:
            for i in username:
                #checking if username is a character or a number
                if not i.isalpha() and not i.isdigit() and not i=='_':
                    print(i)
                    resp.set_cookie('username', '', expires=0)
                    resp.set_cookie('password', '', expires=0)
                    flask.flash('Username not valid'.format(username), 'danger')
                    return flask.redirect(flask.url_for('login.loginscreen'))
           
            flask.flash('User {} created successfully!'.format(username), 'success')
            users.new_user(db,username,password)
            resp.set_cookie('password',password)
            resp.set_cookie('username',password)
            return flask.redirect(flask.url_for('login.loginscreen'))
        else:
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('Username is taken'.format(username), 'danger')
            return flask.redirect(flask.url_for('login.loginscreen'))
    

    elif submit == 'Delete':
        if users.delete_user(db, username, password):
            resp.set_cookie('username', '', expires=0)
            resp.set_cookie('password', '', expires=0)
            flask.flash('User {} deleted successfully!'.format(username), 'success')

    return resp

@blueprint.route('/logout', methods=['POST'])
def logout():
    """Log out the user."""
    db = helpers.load_db()

    resp = flask.make_response(flask.redirect(flask.url_for('login.loginscreen')))
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('password', '', expires=0)
    return resp

@blueprint.route('/')
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
        flask.flash('Invalid credentials. Please try again.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # get the info for the user's feed
    
    friends = users.get_user_friends(db, user)
    all_posts = []
    for friend in friends + [user]:
        all_posts += posts.get_posts(db, friend)
    # sort posts
    sorted_posts = sorted(all_posts, key=lambda post: post['time'], reverse=True)

    return flask.render_template('feed.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friends=friends, posts=sorted_posts, alerts=user['alerts'],)
@blueprint.route('/static/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded media files."""

    return flask.send_from_directory(UPLOAD_FOLDER, filename)