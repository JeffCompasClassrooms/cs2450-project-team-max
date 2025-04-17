import flask
import tinydb
from handlers import copy
from db import users, helpers
import time
import os
UPLOAD_FOLDER = 'static/uploads/'
blueprint = flask.Blueprint("profile", __name__)
@blueprint.route('/profileScreen')
def profileScreen():
    """Present a form to the user to enter their username and password."""
    db = helpers.load_db()
    # First check if user has already put in their profile information
    fullName = flask.request.cookies.get('fullName')
    age = flask.request.cookies.get('age')
    instrument = flask.request.cookies.get('instrument')
    experience = flask.request.cookies.get('experience')
    genre = flask.request.cookies.get('genre[]')
    covers = flask.request.cookies.get('covers')
    countryLocation = flask.request.form.get('countryLocation')
    state = flask.request.form.get('state')
    city = flask.request.form.get('city')  
    location = f"{city}, {state}, {countryLocation}"
    travel = flask.request.cookies.get('travel')
    
    # if value is not None, then the user has already filled out their profile
    # and we can allow them to edit it

    # If they have already filled out their profile, allow them to make edits
    flask.flash('You can edit your profile below.', 'info')
    return flask.render_template('profile.html', title=copy.title,)
        
    # Otherwise, present the profile creation form   
@blueprint.route('/profile', methods=['POST'])
def profile():
    """Create the user profile."""
    db = helpers.load_db()    
    username= flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    if users.get_user(db,username,password) is None:
        flask.flash("Enter your name (this field is required)", 'danger')
        return flask.redirect(flask.url_for('signup.signup'))
    fullName = flask.request.form.get('Fullname')
    age = flask.request.form.get('age')
    instrument = flask.request.form.get('instrument')
    media = flask.request.files.get("media") 
    experience = flask.request.form.get('experience')
    genre = flask.request.form.get('genre[]')
    covers = flask.request.form.get('covers')
    latitude = flask.request.form.get('latitude')
    longitude = flask.request.form.get('longitude')
    travel = flask.request.form.get('travel')
    longitude =float(longitude)
    latitude = float(latitude)
    
    # making sure the name section is not empty
    if fullName == "":
        flask.flash("Enter your name (this field is required)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the name is not too long
    if len(fullName) > 30:
        flask.flash("Name must be less than 30 characters", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the name is not too short
    if len(fullName) < 2:
        flask.flash("Name must be more than 2 characters", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen')) 
    # making sure the name is a character and not a number or special character
    # for i in fullName:
    #     print(i)
    #     if not i.isalpha() and not i=='_' or not i==' ':
    #         print('ERROR')
    #         print(i)
            
    #         flask.flash("Name not valid. Please don't use numbers or special characters".format(fullName), 'danger')
    #         return flask.redirect(flask.url_for('profile.profileScreen'))
    
    # making sure the age section is not empty
    if age == "":
        flask.flash("Enter your age (this field is required)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the age is a number
    try:
        age = int(age)
    except ValueError:
        flask.flash("Age must be a number", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the age is between 0 and 120
    if age < 0 or age > 100:
        flask.flash("Age must be between 0 and 100", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the age is not a character or a special character
    
    # making sure the instrument section is not empty
    if instrument == []:
        flask.flash("Enter your instrument (you can list more than 1!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the experience section is not empty
    if experience == "":
        flask.flash("Enter your experience (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the experience is a number
    try:
        experience = int(experience)
    except ValueError:
        flask.flash("Experience must be a number", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the experience is not greater than age
    if experience > age:
        flask.flash("Experience must be less than age", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))

    # making sure the genre section is not empty
    if genre == "":
        flask.flash("Enter your genre (you can list more than 1!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))

    # making sure the covers section is not empty
    if covers == "":
        flask.flash("Select covers or create (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))

    # making sure the location section is not empty
    # making sure the travel section is not empty
    if travel == "":
        flask.flash("Select Yes or No (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    
    # make sure travel is either yes or no
    media_filename = None
    media_type = None
    # Store in TinyDB
    media_url= f"static/uploads/{media_filename}" if media_filename else None
    if media:
        file_extension = media.filename.rsplit('.', 1)[1].lower()

        media_filename = f"{'username'}_{time.time()}.{file_extension}"
        media.save(os.path.join(UPLOAD_FOLDER, media_filename))
    # Store in TinyDB
    media_url= f"static/uploads/{media_filename}" if media_filename else None
    
    
    # create the user profile in the database
    users.user_profile(db, username, fullName =fullName, age =age, instrument = instrument, experience =experience, latitude=latitude, longitude= longitude, genre= genre, covers =covers, travel =travel,profile_picture = media_url)
    flask.flash('Profile created successfully!', 'success')
    return flask.redirect(flask.url_for('login.index'))

    # allow the user to cancel the profile creation
@blueprint.route('/cancel', methods=['POST'])
def cancel():
    """Cancel the profile creation."""
    db = helpers.load_db()
    # delete the cookies
    resp = flask.make_response(flask.redirect(flask.url_for('profile.profileScreen')))  # Redirect to the a different page than profile. Possibly the main page
    resp.set_cookie('fullName', '', expires=0)
    resp.set_cookie('age', '', expires=0)
    resp.set_cookie('instrument', '', expires=0)
    resp.set_cookie('experience', '', expires=0)
    resp.set_cookie('genre[]', '', expires=0)
    resp.set_cookie('covers', '', expires=0)
    resp.set_cookie('location', '', expires=0)
    resp.set_cookie('travel', '', expires=0)
    return resp
@blueprint.route('/like', methods=['POST'])
def like():
    liker= flask.request.cookies.get('username')
    data = flask.request.get_json()  # Get data from the request body
    db = helpers.load_db()
    table = db.table('users')
    User = tinydb.Query()
    username = data.get('username')
    print(username)
    request=[liker,'liked']
    likee= users.get_user_by_name(db,username)
   
    if likee:
        likee['alerts'].append(request)
        table.upsert(table.upsert(likee, (User.username == likee['username'])))
        return flask.jsonify({'success': True, 'username': username}), 200
    else:
        return flask.jsonify({'success': False, 'message': 'User already liked or invalid username'}), 400