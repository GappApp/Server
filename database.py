from sqlite3 import connect


class Database:
    def __init__(self):
        # Our Database of Users
        self.user_db = connect('users.db')
        self.ucur = self.user_db.cursor()
        self.ucur.execute('drop table users')
        self.ucur.execute('create table users (username text)')
        self.user_db.commit()

        # Our Database of Messages
        self.message_db = connect('messages.db')
        self.mcur = self.message_db.cursor()
        self.mcur.execute('drop table messages')
        self.mcur.execute('create table messages '
                          '(sender text, receiver text,'
                          ' message text)')
        self.message_db.commit()

    def username_exist(self, username):
        for row in self.ucur.execute('select * from users'):
            if row[0] == username:
                return True
        return False

    def add_username(self, username):
        self.ucur.execute('insert into users values ("{}")'.format(username))
        self.user_db.commit()

    def remove_username(self, username):
        self.ucur.execute('delete from users where username="{}"'.format(username))

    def get_all_usernames(self):
        self.ucur.execute('select * from users')
        return self.ucur.fetchall()

    def get_all_messages(self):
        self.mcur.execute('select * from messages')
        return self.mcur.fetchall()

    def send_message(self, sender, receiver, message):
        self.mcur.execute('insert into messages values ("{}", "{}", "{}")'.format(sender, receiver, message))
        self.message_db.commit()

    def get_mates(self, username):
        mates = [username]
        for row in self.mcur.execute('select * from messages where sender="{0}" or receiver="{0}"'.format(username)):
            if row[0] not in mates:
                mates.append(row[0])
            if row[1] not in mates:
                mates.append(row[1])
        mates.remove(username)
        return mates

    def get_messages(self, mate1, mate2):
        self.mcur.execute('select * from messages where (sender="{0}" and receiver="{1}") or'
                          ' (receiver="{0}" and sender="{1}")'.format(mate1, mate2))
        return self.mcur.fetchall()
