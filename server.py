from flask import Flask
from database import Database

# Web Server Application and Database Manager
app = Flask(__name__)
db = Database()


@app.route('/sign_in/<username>/')
def sign_in(username):
    if not db.username_exist(username):
        db.add_username(username)
        return '{"Status" : "Ok."}'
    else:
        return '{"Status" : "Error!", "Description" : "Username exist."}'


@app.route('/sign_out/<username>/')
def sign_out(username):
    if db.username_exist(username):
        db.remove_username(username)
        return '{"Status" : "Ok."}'
    else:
        return '{"Status" : "Error!", "Description" : "Username does not exist."}'


@app.route('/send/<sender>/<receiver>/<message>')
def send(sender, receiver, message):
    if db.username_exist(sender):
        if db.username_exist(receiver):
            db.send_message(sender, receiver, message)
            return '{"Status" : "Ok."}'
        else:
            return '{"Status" : "Error!", "Description" : "Receiver username does not exist."}'
    else:
        return '{"Status" : "Error!", "Description" : "Sender username does not exist."}'


@app.route('/get_mates/<username>')
def get_mates(username):
    if db.username_exist(username):
        mates = db.get_mates(username)
        return '{{"Status" : "Ok.", "Mates" : {}}}'.format(list(mates))
    else:
        return '{"Status" : "Error!", "Description" : "Username does not exist."}'


@app.route('/get_messages/<mate1>/<mate2>')
def get_messages(mate1, mate2):
    if db.username_exist(mate1) and db.username_exist(mate2):
        messages = db.get_messages(mate1, mate2)
        return '{{"Status" : "Ok.", "Messages" : {}}}'.format(messages)
    else:
        return '{"Status" : "Error!", "Description" : "Username does not exist."}'


@app.route('/debug')
def debug():
    users = db.get_all_usernames()
    messages = db.get_all_messages()
    return 'users: {} <br> <br> messages: {}'.format(users, messages)


app.run('127.0.0.1', 5000)
