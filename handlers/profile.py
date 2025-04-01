import flask
from handlers import copy
from db import posts, users, helpers
UPLOAD_FOLDER = 'static/uploads'
blueprint = flask.Blueprint("profile", __name__)

@blueprint.route('/profileScreen')
def profileScreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()
    # First check if already logged in
    fullName = flask.request.cookies.get('fullName')
    age = flask.request.cookies.get('age')
    instrument = flask.request.cookies.get('instrument')
    experience = flask.request.cookies.get('experience')
    genre = flask.request.cookies.get('genre')
    covers = flask.request.cookies.get('covers')
    location = flask.request.cookies.get('location')
    travel = flask.request.cookies.get('travel')
'''   
    if username is not None and password is not None:
        if users.get_user(db, username, password):
            # If they are logged in, redirect them to the feed page
            flask.flash('You are already logged in.', 'warning')
            return flask.redirect(flask.url_for('login.index'))

    return flask.render_template('login.html', title=copy.title,
            subtitle=copy.subtitle)
''' 

@blueprint.route('/profile', methods=['POST'])
def profile():

    """Create the user profile."""
    db = helpers.load_db()
    #getting username
    fullName = flask.request.form.get('fullName')
    age = flask.request.form.get('age')
    instrument = flask.request.form.get('instrument')
    experience = flask.request.form.get('experience')
    genre = flask.request.form.get('genre')
    covers = flask.request.form.get('covers')
    location = flask.request.form.get('location')
    travel = flask.request.form.get('travel')

    #creating a response for login,index
    resp = flask.make_response(flask.redirect(flask.url_for('login.index')))
    # making sure the name section is not empty
    if fullName is "":
        flask.flash("Enter your name (this field is required)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('fullName', fullName)
    
    # making sure the age section is not empty
    if age is "":
        flask.flash("Enter your age (this field is required)", 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    resp.set_cookie('age', age)

    # making sure the instrument section is not empty
    if instrument is "":
        flask.flash("Enter your instrument (you can list more than 1!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('instrument', instrument)

    # making sure the experience section is not empty
    if experience is "":
        flask.flash("Enter your experience (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('experience', experience)

    # making sure the genre section is not empty
    if genre is "":
        flask.flash("Enter your genre (you can list more than 1!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('genre', genre)

    # making sure the covers section is not empty
    if covers is "":
        flask.flash("Select covers or create (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('covers', covers)

    # making sure the location section is not empty
    if location is "":
        flask.flash("Enter your location (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('location', location)

    # making sure the travel section is not empty
    if travel is "":
        flask.flash("Select Yes or No (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('travel', travel)
    
    # Save the profile information to the database
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
        flask.flash("Invalid credentials. If you're new, click the sign up button to become a member.", 'danger')
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