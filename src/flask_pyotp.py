import pyotp
from src.exceptions import InvalidTOTP
from flask import request


class PyOTP():
    def __init__(self, app):
        secret_key = pyotp.random_base32()
        print(f'Your secret key: {secret_key}')
        self.app = app
        self.totp = pyotp.TOTP(secret_key)
        self.tokens = []

        print('here')

        def check_totp():
            token = request.args.get('totp')
            if not token or not self.totp.verify(token):
                raise InvalidTOTP

        app.before_request(check_totp)
