from flask import Flask, request
from src.render_template import render_template
from src.mail import Attachment, Mail
from werkzeug.exceptions import HTTPException
from src.exceptions import MissingArguments
import json
from src.flask_pyotp import PyOTP


app = Flask(__name__)
if not app.config['DEBUG']:
    totp = PyOTP(app)
    mail = Mail()


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def parse_request(request):
    kwargs = request.form or request.args
    attachments = [
        Attachment(file_.filename, file_.read())
        for file_ in request.files.getlist('attachments')
    ]
    try:
        receivers = kwargs.getlist('receiver')
        if len(receivers) == 1:
            receiver = receivers[0]
            if ',' in receiver:
                receivers = receiver.split(',')
            elif ' ' in receiver:
                receivers = receiver.split(' ')
        receivers = list({x.strip() for x in receivers})
        kwargs = kwargs.to_dict()
        subject = kwargs.pop('subject')
    except KeyError:
        raise MissingArguments('Both "receiver" and "subject" must be specified')
    else:
        if not receivers or not subject:
            raise MissingArguments('Both "receiver" and "subject" must be specified')
    if 'template' in kwargs:
        template_name = kwargs.pop('template')
        html = render_template(template_name, **kwargs)
    elif 'html' in kwargs:
        html = kwargs.pop('html')
        raise MissingArguments('Either "template" or "html" must be specified')
    return receivers, subject, html, attachments


@app.route('/', methods=['GET', 'POST'])
def index():
    receivers, subject, html, attachments = parse_request(request)
    return mail.send(receivers, subject, html, attachments=attachments)


@app.route('/debug', methods=['GET', 'POST'])
def debug():
    receivers, subject, html, attachments = parse_request(request)
    return {
        'receivers': receivers,
        'subject': subject,
        'html': html,
        'attachments': [{"name": x.filename, "size": len(x.content)} for x in attachments]
    }
