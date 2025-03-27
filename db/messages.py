import time
import tinydb

def message(db, sender,receiver, text):
    messages = db.table('messages')
    messages.insert({'sender': sender['username'],'receiver':receiver['username'], 'text': text, 'time': time.time()})

def get_messages(db, sender, receiver ):
    messages = db.table('messages')
    Post = tinydb.Query()
    receiver['alerts'].append([ sender['username'],'message'])
    return messages.search((
    (Post.sender == sender['username']) & (Post.receiver == receiver['username']) |
    (Post.sender == receiver['username']) & (Post.receiver == sender['username'])
))
