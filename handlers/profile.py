import flask
from handlers import copy
from db import users, helpers
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
    genre = flask.request.cookies.get('genre')
    covers = flask.request.cookies.get('covers')
    location = flask.request.cookies.get('location')
    travel = flask.request.cookies.get('travel')

    # if value is not None, then the user has already filled out their profile
    # and we can allow them to edit it
    if all(value is not None for value in users.user_profile(db, fullName, age, instrument, experience, genre, covers, location, travel)):
        # If they have already filled out their profile, allow them to make edits
        flask.flash('You can edit your profile below.', 'info')
        return flask.render_template('profile.html', title=copy.title,
            fullName=fullName, age=age,
            instrument=instrument, experience=experience,
            genre=genre, covers=covers, location=location,
            travel=travel)
        
    # Otherwise, present the profile creation form   
@blueprint.route('/profile', methods=['POST'])
def profile():

    """Create the user profile."""
    db = helpers.load_db()    
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
    if fullName == "":
        flask.flash("Enter your name (this field is required)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('fullName', fullName)
    # making sure the name is not too long
    if len(fullName) > 30:
        flask.flash("Name must be less than 30 characters", 'danger')
        resp.set_cookie('fullName', '', expires=0)
        return flask.redirect(flask.url_for('profile.profileScreen'))
    # making sure the name is not too short
    if len(fullName) < 2:
        flask.flash("Name must be more than 2 characters", 'danger')
        resp.set_cookie('fullName', '', expires=0)
        return flask.redirect(flask.url_for('profile.profileScreen')) 
    # making sure the name is a character and not a number or special character
    for i in fullName:
        if not i.isalpha() and not i=='_':
            print(i)
            resp.set_cookie('fullName', '', expires=0)
            flask.flash("Name not valid. Please don't use numbers or special characters".format(fullName), 'danger')
            return flask.redirect(flask.url_for('profile.profileScreen'))
    
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
    resp.set_cookie('age', age)
    # making sure the age is not a character or a special character
    for i in age:
        if not i.isdigit():
            print(i)
            resp.set_cookie('age', '', expires=0)
            flask.flash("Age not valid. Please don't use characters or special characters".format(age), 'danger')
            return flask.redirect(flask.url_for('profile.profileScreen'))

    # making sure the instrument section is not empty
    if instrument == "":
        flask.flash("Enter your instrument (you can list more than 1!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('instrument', instrument)

    # making sure the experience section is not empty
    if experience == "":
        flask.flash("Enter your experience (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('experience', experience)
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
    resp.set_cookie('genre', genre)

    # making sure the covers section is not empty
    if covers == "":
        flask.flash("Select covers or create (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('covers', covers)

    # making sure the location section is not empty
    if location == "":
        flask.flash("Enter your location (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('location', location)

    # making sure the travel section is not empty
    if travel == "":
        flask.flash("Select Yes or No (this field is not required, but it will help you find matches!)", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
    resp.set_cookie('travel', travel)
    # make sure travel is either yes or no
    if travel != "Yes" and travel != "No":
        flask.flash("Please enter Yes or No", 'danger')
        return flask.redirect(flask.url_for('profile.profileScreen'))
 
    
    # create the user profile in the database
    users.user_profile(db, fullName, age, instrument, experience, genre, covers, location, travel)
    flask.flash('Profile created successfully!', 'success')
    return resp 

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
    resp.set_cookie('genre', '', expires=0)
    resp.set_cookie('covers', '', expires=0)
    resp.set_cookie('location', '', expires=0)
    resp.set_cookie('travel', '', expires=0)
    return resp
