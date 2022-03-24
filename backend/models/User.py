from os import abort

from werkzeug.security import generate_password_hash, check_password_hash


class User:
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def get_id(self):
        return self.user_id
