import flask
import tinydb
from handlers import copy
from db import posts, users, helpers, messages, groups

blueprint = flask.Blueprint("groups", __name__)

@blueprint.route('/makegroup', methods=['POST'])
def makegroup():
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

    # make the group
    gname = flask.request.form.get('gname')
    if gname =="":
        flask.flash("Enter name",'danger')
        return flask.redirect(flask.url_for('login.index'))
    if gname== user['group']:
        flask.flash("already in group",'danger')
        return flask.redirect(flask.url_for('groups.view_group'))
    group = groups.get_group(db,gname)
    if group:
        flask.flash("group name already taken",'danger')
        return flask.redirect(flask.url_for('login.index'))
    groups.new_group(db,user,gname)
    
    return flask.redirect(flask.url_for('login.index'))
@blueprint.route('/add_member', methods=['POST'])
def add_member():
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

    name = flask.request.form.get('iname')
    member = users.get_user_by_name(db,name)
    group = groups.get_group(db,user['group'])
    if(user['username'] == name):
        flask.flash("", "danger")
        return flask.redirect(flask.url_for('login.index'))
    request = [group['name'],'group invite']
    if request not in member['alerts']:
        table = db.table('users')
        User = tinydb.Query()
        member['alerts'].append(request)
        table.upsert(member, (User.username == member['username']))
        msg, category =  groups.add_member(db,member,group)

        flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))



@blueprint.route('/remove_member', methods=['POST'])
def remove_member():
    """Removes a user from the user's friends list."""
    db = helpers.load_db()

    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You need to be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    gname = flask.request.form.get('gname')
    msg, category = groups.remove_member(db, user, name)

    flask.flash(msg, category)
    return flask.redirect(flask.url_for('login.index'))

@blueprint.route('/group/<gname>')
def view_group(gname):
    """View the page of a given friend."""
    db = helpers.load_db()
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    group =groups.get_group(db,gname)
    all_posts = groups.get_group_posts(db, group)[::-1] # reverse order
    all_message =groups.get_group_messages(db,user,group)
    return flask.render_template('group.html', title=copy.title,
            subtitle=copy.subtitle, user=user, username=username,
            posts=all_posts, all_messages=all_message,alerts=user['alerts'], group = group)
    
@blueprint.route('/group/<gname>/message',methods=['POST'])
def send_message(gname):
    db =helpers.load_db()
    
    username = flask.request.cookies.get('username')
    password = flask.request.cookies.get('password')

    user = users.get_user(db, username, password)
    if not user:
        flask.flash('You must be logged in to do that.', 'danger')
        return flask.redirect(flask.url_for('login.loginscreen'))

    group = groups.get_group(db,gname)
    text= flask.request.form.get('send_group_message')
    all_message =groups.get_group_messages(db,user,group)
    if text == "" or text == None:
        flask.flash('Must have a message to send', 'danger')
        
        return flask.redirect(flask.url_for('groups.view_group',gname = gname))

    groups.group_message(db,user,group,text)
    table = db.table('users')
    User = tinydb.Query()
    members = groups.get_members(db,group)
    return flask.redirect(flask.url_for('groups.view_group',gname = gname))
