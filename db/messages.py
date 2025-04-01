import time
import tinydb
from db import users

def message(db, sender, receiver, text):
    messages = db.table('messages')
    
    # Add alert for the receiver
    request = [sender['username'], 'message']
    if request not in receiver['alerts']:
        receiver['alerts'].append(request)
    # Insert the message into the database
    messages.insert({
        'sender': sender['username'],
        'receiver': receiver['username'],
        'text': text,
        'time': time.time()
    })



def get_messages(db, sender, receiver):
    messages = db.table('messages')
    Post = tinydb.Query()
    
    # Get messages between sender and receiver
    return messages.search(
        (Post.sender == sender['username']) & (Post.receiver == receiver['username']) |
        (Post.sender == receiver['username']) & (Post.receiver == sender['username'])
    )

