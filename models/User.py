from datetime import date
from os import abort

from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self):
        username: str = None,
        email: str = None,
        firstname: str = None,
        lastname: str = None