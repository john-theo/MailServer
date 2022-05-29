import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup
from email.mime.base import MIMEBase
from email import encoders
from dataclasses import dataclass
from typing import Optional, List
import os
from dotenv import load_dotenv


if not ('GMAIL_USERNAME' in os.environ and 'SENDER_NAME' in os.environ):
    load_dotenv('.env')
load_dotenv('.env.local')


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
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        username = os.environ.get('GMAIL_USERNAME')
        assert username, 'Missing environment variable GMAIL_USERNAME'
        password = os.environ.get('GMAIL_APP_PASSWORD')
        assert password, 'Missing environment variable GMAIL_APP_PASSWORD'
        name = os.environ.get('SENDER_NAME')
        assert name, 'Missing environment variable SENDER_NAME'
        self.sender_mail = username
        self.sender_name = f'{name} ({username})'
        self.password = password
        ssl_context = ssl.create_default_context()
        self.service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        self.service.login(self.sender_mail, self.password)

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
