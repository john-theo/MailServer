import atexit
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from email.mime.base import MIMEBase
from email import encoders
from dataclasses import dataclass
from typing import Optional, List
import os
from src.providers import get_provider_args


@dataclass
class Attachment:
    filename: str
    content: bytes

    @property
    def mime(self):
        mime = MIMEBase("application", "octet-stream")
        mime.set_payload(self.content)
        encoders.encode_base64(mime)
        mime.add_header("Content-Disposition", f"attachment; filename={self.filename}")
        return mime


class Mail:
    def __init__(self, app):
        self.app = app
        self.service = smtplib.SMTP_SSL(
            *get_provider_args(), context=ssl.create_default_context())
        self.sender_mail = self.login()
        name = os.environ.get('NAME')
        self.sender_name = f'{name} ({self.sender_mail})' if name else self.sender_mail
        atexit.register(lambda: self.close())

    def login(self):
        username = os.environ.get('EMAIL')
        assert username, 'Missing environment variable EMAIL'
        password = os.environ.get('PASSWORD')
        assert password, 'Missing environment variable PASSWORD'
        self.service.login(username, password)
        print('Login success!')
        return username

    def close(self):
        self.service.quit()

    def send(self, receivers:List[str], subject:str, content_html:str, attachments:Optional[List[Attachment]]=None, isolate_receivers:Optional[bool]=True):
        mail = MIMEMultipart('alternative')
        mail['Subject'] = subject
        mail['From'] = self.sender_name
        mail.attach(MIMEText(BeautifulSoup(content_html, "html.parser").get_text().strip(), 'plain'))
        mail.attach(MIMEText(content_html, 'html'))
        [mail.attach(x.mime) for x in attachments]
        if isolate_receivers:
            results = {}
            for email in receivers:
                mail['To'] = email
                error = self.service.sendmail(self.sender_mail, email, mail.as_string())
                results[email] = error or 'success'
        else:
            errors = self.service.sendmail(self.sender_mail, receivers, mail.as_string())
            results = {x: errors.get(x, 'success') for x in receivers}
        return results
