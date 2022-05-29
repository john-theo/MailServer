import requests
from requests.exceptions import HTTPError
import json

# ----------------------------------------------------------------

RECEIVER_EMAIL = ""   # FILL ME
BRAND_NAME = ""       # FILL ME
SERVER_INSTANCE = ""  # FILL ME (eg. http://localhost:8080)

# ----------------------------------------------------------------

activation_template_args = {
    'username': 'John Theo',
    'activation_link': 'https://github.com/john-theo',
    'brand_name': BRAND_NAME,
    'contact_email': RECEIVER_EMAIL,

    'brand_logo_src': 'https://avatars.githubusercontent.com/u/36699957?v=4',
    'brand_logo_height': '30px',
    'time_before': 'an hour',
    'font_size': '14px',
    'secondary_font_size': '12px',
    'link_color': 'green',
}


resp = requests.post(SERVER_INSTANCE, data={
    'subject': 'Please validate your email address',
    'receiver': [RECEIVER_EMAIL],
    'template': 'activation',
    **activation_template_args
}, files=[
    ('attachments', ('activation.jinja', open('templates/activation.jinja', 'rb'))),
    ('attachments', ('server.py', open('src/server.py', 'rb')))
])
try:
    resp.raise_for_status()
    print(resp.json())
except HTTPError:
    raise ValueError(str(json.dumps(resp.json(), indent=4)))
