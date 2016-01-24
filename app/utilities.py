import re
import bcrypt
import datetime

def password_is_valid(password):
    if len(password) >= 8 and len(password) <= 12 and \
       ' ' not in password and \
       re.search(r'[A-Z]', password) and \
       re.search(r'[a-z]', password) and \
       re.search(r'[0-9]', password):
        return True
    return False

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    if bcrypt.hashpw(password.encode('utf-8'), hashed_password.encode('utf-8')) == hashed_password:
        return True
    return False