import time
import tinydb
from db import users
#expecting user instance and group name
def new_group(db, user, group):
    groups = db.table('groups')
    users = db.table('users')
    Group = tinydb.Query()
    if groups.get(Group.name == group):
        return None
    group_records = {
            'name':group,
            'owner': user['username'],
            'members':[user['username']],
            
            }
    user['group'] = group
    users.upsert(user, (Group.username == user['username']) &
                    (Group.password == user['password']))
    return groups.insert(group_records)

def get_group (db,group_name):

    groups = db.table('groups')
    Group = tinydb.Query()
    return groups.get(Group.name == group_name)

    
def get_members(db,group):
    return group['members']


def get_group_posts(db, group:dict,):
    posts = db.table('posts')
    Post = tinydb.Query()
    post=None
    for recipiant in group['members']:
        post=(posts.search(Post.user == recipiant))
    return post

def get_group_messages(db, sender, receiver):
    group = db.table('group_messages')
    Message = tinydb.Query()
    
    all_messages = []  # To store the results
    print(receiver)
    print('group search')
    print(group.search(
            (Message.receiver == receiver['members'])
    ))
    return group.search(
            (Message.receiver == receiver['members'])
    )

def group_message(db, sender, receiver, text):
    messages = db.table('group_messages')
    table = db.table('users')
    User = tinydb.Query()
    print(text)
    members = []
    # Send the message to each recipiant in the group
    for recipiant_name in receiver['members']:
        recipiant = users.get_user_by_name(db, recipiant_name)  # Get the user object
        if sender == recipiant:
            continue 
        # Add an alert for each recipiant
        recipiant['alerts'].append([sender['username'], 'message'])
        table.upsert(recipiant,(User.username == recipiant['username']))
        # Insert the message into the database
    return messages.insert({
        'sender': sender['username'],
        'receiver': receiver['members'],
        'text': text,
        'time': time.time()
    })

#expecting the group and the user instance
def add_member(db,user,group):
    groups = db.table('groups')
    users = db.table('users')
    Group = tinydb.Query()
    request = [group['name'],'group invite']
    if request not  in user['alerts']:
        
        user['group'] = group['name']

        users.upsert(user, (Group.username == user['username']) &
                    (Group.password == user['password']))
        group['members'].append(user)
        return '{} added to group!'.format(user['username']), 'success'
    
    return '{} pending invite group {}!'.format(user['username'],group['name']), 'success'

def remove_member(db, user,group):
    groups = db.table('groups')
    querys = tinydb.Query()
    if groups.get(not querys.name == group['name']):
        return None
    return group['members'].remove(user)
def change_owner(db, user,group):
    groups = db.table('groups')
    querys = tinydb.Query()
    if groups.get(not querys.name == group['name']):
        return None
    return group['owner']==user['username']

    