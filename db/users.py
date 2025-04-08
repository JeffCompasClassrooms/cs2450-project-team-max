import tinydb

def new_user(db, username, password):
    users = db.table('users')
    User = tinydb.Query()
    if users.get(User.username == username):
        return None
    user_record = {
            'username': username,
            'password': password,
            'friends': [],
            'pending-friends':[],
            'alerts':[],
            'group':None
            }
    return users.insert(user_record)

def user_profile(db, fullName, age, instrument, experience, genre, covers, location, travel):
    """
    Create a new user profile in the database.
    """
    users = db.table('users')
    User = tinydb.Query()
    
    # Create a new user profile record
    user_profile_record = {
            'fullName': fullName,
            'age': age,
            'instrument': instrument,
            'experience': experience,
            'genre': genre,
            'covers': covers,
            'location': location,
            'travel': travel
            }
    
    # Update the user profile in the database
    return users.upsert(user_profile_record, User.username == fullName)

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
def update_password(db, username, new_password):
    """Updates the password for a user."""
    users_table = db.table('users')
    User = tinydb.Query()

    # Debug: Check if the user exists
    user = users_table.get(User.username == username)
    if not user:
        print(f"User with username '{username}' not found.")
        return 0  # No records updated

    # Perform the update
    result = users_table.update({'password': new_password}, User.username == username)
    print(f"Password update result for username '{username}': {result}")
    return result  # Returns the number of updated records
def update_user(db, user):
    """Updates a user's information in the database."""
    users_table = db.table('users')
    User = tinydb.Query()
    result = users_table.update({'username': user['username']}, User.username == user['old_username'])
    return result  # Returns the number of updated records
def delete_user(db, username):
    """Deletes a user from the database."""
    users_table = db.table('users')
    User = tinydb.Query()
    result = users_table.remove(User.username == username)
    return result  # Returns the number of deleted records