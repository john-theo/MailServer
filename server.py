from flask import Flask, request
from render_template import render_template
from mail import Attachment, Mail
from werkzeug.exceptions import HTTPException, MissingArguments
import json
import atexit


app = Flask(__name__)
mail = Mail()
atexit.register(lambda _: mail.close())


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


@app.route('/', methods=['GET', 'POST'])
def index():
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
        receivers = [x.strip() for x in receivers]
        subject = kwargs.pop('subject')
    except KeyError:
        raise MissingArguments('Both "receiver" and "subject" must be specified')
    else:
        if not receivers or not subject:
            raise MissingArguments('Both "receiver" and "subject" must be specified')
    if 'template' in kwargs:
        template_name = kwargs.pop('template')
        html = render_template(template_name, kwargs.to_dict())
    elif 'html' in kwargs:
        html = kwargs.pop('html')
    else:
        raise MissingArguments('Either "template" or "html" must be specified')
    return mail.send(receivers, subject, html, attachments=attachments)
