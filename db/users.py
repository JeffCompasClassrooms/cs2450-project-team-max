import tinydb
def update_location(db,user,location):
    table = db.table('users')
    User = tinydb.Query()
    user['location']=location
    return table.upsert(user,(User.username==user['username']))
    
def new_user(db, username, password,lat, long):
    users = db.table('users')
    User = tinydb.Query()
    if users.get((User.username == username)):
        return None
    user_record = {
            'username': username,
            'password': password,
            'friends': [],
            'pending-friends':[],
            'alerts':[],
            'group':None,
            'latitude': lat,
            'longitude': long,
            }
    return users.insert(user_record)
def get_all_users(db,user):
    users = db.table('users')
    User = tinydb.Query()
    all_users = users.search(User.username != user['username'])    
    return all_users
def get_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.get((User.username == username) &
            (User.password == password))

def get_user_by_name(db, username):
    users = db.table('users')
    User = tinydb.Query()
    return users.get(User.username == username)

def delete_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    return users.remove((User.username == username) &
            (User.password == password))

def add_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == friend['username']):
        if friend not in user['friends'] and friend['username'] is not user['username']:
            friend['alerts'].append([ user['username'],'friend request'])
            users.upsert(user, (User.username == user['username']) &
                    (User.password == user['password']))
            users.upsert(friend,(User.username == friend['username']) &
                    (User.password == friend['password']))
            return 'Friend {} added successfully!'.format(friend['username']), 'success'
        return 'User {} does not exist.'.format(friend['username']), 'danger'
    return 'You are already friends with {}.'.format(friend['username']), 'warning'

def remove_user_friend(db, user, friend):
    users = db.table('users')
    User = tinydb.Query()
    if friend in user['friends']:
        user['friends'].remove(friend)
        users.upsert(user, (User.username == user['username']) &
                (User.password == user['password']))
        return 'Friend {} successfully unfriended!'.format(friend), 'success'
    elif friend in user['pending-friends']:
        user['pending-friends'].remove(friend)
        users.upsert(user, (User.username == user['username']) &
        (User.password == user['password']))
        return '{}s Friend request denied!'.format(friend), 'success'
    return 'You are not friends with {}.'.format(friend), 'warning'

def get_user_friends(db, user):
    users = db.table('users')
    User = tinydb.Query()
    friends = []
    for friend in user['friends']:
        friends.append(users.get(User.username == friend))
    return friends
