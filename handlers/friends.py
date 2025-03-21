import flask

from handlers import copy
from db import posts, users, helpers, messages

blueprint = flask.Blueprint("friends", __name__)

@blueprint.route('/addfriend', methods=['POST'])
def addfriend():
    """Adds a friend to the user's friends list."""
    db = helpers.load_db()

    # make sure the user is logged in
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    if username is None and password is None:
        return flask.redirect(flask.url_for('login.loginscreen'))

    user = users.get_user(db, username, password)
    if not user:
        flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    # add the friend
    name = flask.request.form.get('name')
    if name =="":
        flask.flash("Enter name",'danger')
        return flask.redirect(flask.url_for('login.index'))
    if name== user['username']:
        flask.flash("cannot add self",'danger')
        return flask.redirect(flask.url_for('login.index'))
    if name in user['pending-friends']:
        flask.flash("friend request pending",'danger')
        return flask.redirect(flask.url_for('login.index'))
    if name in user['friends']:
        flask.flash("already friends",'danger')
        return flask.redirect(flask.url_for('login.index'))
    friend = users.get_user_by_name(db,name)
    print("friend is " )
    print(friend)
    print("done")
    
    msg, category = users.add_user_friend(db, user, friend)
    
    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/unfriend', methods=['POST'])
def unfriend():
    """Removes a user from the user's friends list."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    name = flask.request.form.get('name')
    msg, category = users.remove_user_friend(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/friend/<fname>')
def view_friend(fname):
    """View the page of a given friend."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    friend = users.get_user_by_name(db, fname)
    print(friend)
    all_posts = posts.get_posts(db, friend) # reverse order
    all_message =messages.get_messages(db,user,friend)

    return flask.render_template('friend.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            friend=friend['username'],
            friends=users.get_user_friends(db, user), posts=all_posts, all_messages=all_message)
@blueprint.route('/friend/<fname>/message',methods=['POST'])
def send_message(fname):
    db =helpers.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    friend = users.get_user_by_name(db, fname)
    text= flask.request.form.get('send_message')
    all_message =messages.get_messages(db,user,friend)
    if text == "":
        flask.flash('Must have a message to send', 'danger')
        return flask.redirect(flask.url_for('friends.view_friend',fname = fname))
    print(text)
    print(all_message)
    messages.message(db,user,friend,text)
    return flask.render_template('friend.html', title=copy.title,
        subtitle=copy.subtitle, user=user, username=username,
        friend=friend['username'],
        friends=users.get_user_friends(db, user), all_messages=all_message)
    
