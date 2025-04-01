import flask
import tinydb
from handlers import copy
from db import posts, users, helpers, groups
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
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    user = users.get_user(db, username, password)
    if not user:
        flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))
    
    table = db.table('users')
    grouptbl = db.table('groups')
    User = tinydb.Query()
    request = [name ,message]
    if request[1] =='friend request':
        friend = users.get_user_by_name(db,name)
        if submit =='accept':
            user['friends'].append(friend['username'])
            friend['friends'].append(user['username'])
            if request not in user['alerts']:
                return flask.redirect(flask.url_for('login.index'))
            user['alerts'].remove(request)
            table.upsert(user, (User.username == user['username']) &
                        (User.password == user['password']))
            table.upsert(friend,(User.username == friend['username']) &
                        (User.password == friend['password']))
            
            flask.flash('New friend','success`')
        elif submit =='decline':
            user['alerts'].remove(request)
            table.upsert(user, (User.username == user['username']) &
                            (User.password == user['password']))
            table.upsert(friend,(User.username == friend['username']) &
                            (User.password == friend['password']))
            return flask.redirect(flask.url_for('login.index'))
    elif request[1] =='message':
        user['alerts'].remove(request)
        table.upsert(user, (User.username == user['username']) &
                            (User.password == user['password']))
    elif request[1]== 'group invite':
        group = groups.get_group(db,name)
        if submit =='accept':
                group['members'].append(user['username'])
                user['group']=group['name'] 
                if request not in user['alerts']:
                    return flask.redirect(flask.url_for('login.index'))
                user['alerts'].remove(request)
                table.upsert(user, (User.username == user['username']) &
                            (User.password == user['password']))
                grouptbl.upsert(group,(User.name == user['group']))
                
                flask.flash('joined group','success`')
        elif submit =='decline':
            user['alerts'].remove(request)
            table.upsert(user, (User.username == user['username']) &
                            (User.password == user['password']))
            return flask.redirect(flask.url_for('login.index'))
    return flask.redirect(flask.url_for('login.index'))