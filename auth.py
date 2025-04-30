# auth.py

import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login(users, username, password):
    hashed = hash_password(password)
    if username in users and users[username]['password'] == hashed:
        return users[username]
    else:
        return None

def register(users, username, password):
    if username in users:
        return None  # Username already exists

    users[username] = {
        "username": username,
        "password": hash_password(password),
        "accounts": []
    }
    return users[username]
