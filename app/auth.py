# --- FILE: app/auth.py ---
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def get_id(self):
        return self.id

# Hardcoded users (username:password)
users = {
    '1': User('1', 'admin', 'admin'),
    '2': User('2', 'user', 'user')
}

credentials = {
    'admin': 'adminpass',
    'user': 'userpass'
}
