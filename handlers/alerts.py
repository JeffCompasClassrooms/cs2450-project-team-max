import flask
import tinydb
from handlers import copy
from db import posts, users, helpers
blueprint = flask.Blueprint("alerts", __name__)
@blueprint.route('/request', methods=['POST'])
def alerts():
    db = helpers.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')
    submit =flask.request.form.get('type')
    name = flask.request.form.get('name')
    message = flask.request.form.get('alert')

    if username is None and password is None:
        print('in')
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    user = users.get_user(db, username, password)
    if not user:
        flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    table = db.table('users')
    User = tinydb.Query()
    print(name)
    print('before')
    friend = users.get_user_by_name(db,name)
    request = [name ,message]
    print(request)
    if submit =='accept':
        print(user)
        print(friend)
        
        user['friends'].append(friend['username'])
        friend['friends'].append(user['username'])

        user['pending-friends'].remove(friend['username'])
        if request not in user['alerts']:
            return flask.redirect(flask.url_for('login.index'))
        user['alerts'].remove(request)
        table.upsert(user, (User.username == user['username']) &
                    (User.password == user['password']))
        table.upsert(friend,(User.username == friend['username']) &
                    (User.password == friend['password']))
        
        flask.flash('New friend','success`')
    elif submit =='decline':
        print(user)
        print(friend)
        user['pending-friends'].remove(name)
        user['alerts'].remove(request)
        table.upsert(user, (User.username == user['username']) &
                        (User.password == user['password']))
        table.upsert(friend,(User.username == friend['username']) &
                        (User.password == friend['password']))
    return flask.render_template('feed.html',title=copy.title,
            subtitle=copy.subtitle, user=user, username=username, alerts=user['alerts'], friends= users.get_user_friends(db,user))

        