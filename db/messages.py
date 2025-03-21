import time
import tinydb

def message(db, sender,receiver, text):
    messages = db.table('messages')
    messages.insert({'sender': sender['username'],'receiver':receiver['username'], 'text': text, 'time': time.time()})

def get_messages(db, sender, receiver ):
    print('get messages')
    print(sender)
    print(receiver)
    messages = db.table('messages')
    Post = tinydb.Query()
    print(((Post.sender==sender['username'] and Post.receiver == receiver['username'])or
     (Post.sender==receiver['username'] and Post.receiver == sender['username'])))
    return messages.search((
    (Post.sender == sender['username']) & (Post.receiver == receiver['username']) |
    (Post.sender == receiver['username']) & (Post.receiver == sender['username'])
))
