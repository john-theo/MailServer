import pyotp
from src.exceptions import InvalidTOTP
from flask import request
from threading import Thread
import atexit
from time import sleep
import os
import signal


signal.signal(signal.SIGINT, lambda _, __: os._exit(0))


class PyOTP():
    def __init__(self, app):
        secret_key = os.environ.get('TOTP_SECRET')
        if not secret_key:
            print(f'"TOTP_SECRET" env variable not found, '
                  'TOTP authentication not activated! '
                  'See https://github.com/john-theo/MailServer#totp for details'
                  )
            return
        self.app = app
        self.totp = pyotp.TOTP(secret_key)
        self.tokens = []
        thread = Thread(target=self.push_token)
        thread.start()
        atexit.register(lambda: thread.join())

        def check_totp():
            token = request.args.get('totp')
            if token not in self.tokens:
                raise InvalidTOTP

        app.before_request(check_totp)

    def push_token(self):
        while True:
            token = self.totp.now()
            if not self.tokens or self.tokens[-1] != token:
                self.tokens.append(token)
            if len(self.tokens) > 3:
                self.tokens.pop(0)
            sleep(5)
