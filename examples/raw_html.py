import requests
from requests.exceptions import HTTPError
import json

# ----------------------------------------------------------------

RECEIVER_EMAIL = ""   # FILL ME
BRAND_NAME = ""       # FILL ME
SERVER_INSTANCE = ""  # FILL ME (eg. http://localhost:8080)

# ----------------------------------------------------------------

resp = requests.get(SERVER_INSTANCE, params={
    'subject': 'Please validate your email address',
    'receiver': [RECEIVER_EMAIL],
    'html': f'<h1>Hello from {BRAND_NAME}!</h1>',
})
try:
    resp.raise_for_status()
    print(resp.json())
except HTTPError:
    raise ValueError(str(json.dumps(resp.json(), indent=4)))
