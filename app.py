from flask import Flask, request, render_template as flask_render_template
from src.render_template import render_template
from src.mail import Attachment, Mail
from werkzeug.exceptions import HTTPException
from src.exceptions import MissingArguments
import json
from src.flask_pyotp import PyOTP


app = Flask(__name__)


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
        raise MissingArguments(
            'Both "receiver" and "subject" must be specified')
    else:
        if not receivers or not subject:
            raise MissingArguments(
                'Both "receiver" and "subject" must be specified')
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
@app.route('/preview', methods=['GET', 'POST'])
def preview():
    """Example:
    http://127.0.0.1:5000/preview?subject=Please%20validate%20your%20email%20address&receiver=zhuangxh.cn@gmail.com&receiver=another@163.com&template=activation&username=John%20Dope&activation_link=https://zxh.cool&brand_name=Mail%20Server&contact_email=zhuangxh.cn@gmail.com&brand_logo_src=https://avatars.githubusercontent.com/u/36699957?v=4&brand_logo_height=30px&time_before=an%20hour&link_color=green&font_size=14px
    """
    receivers, subject, html, attachments = parse_request(request)
    return flask_render_template(
        'preview.jinja', html=html, receivers=receivers, subject=subject,
        attachments=[
            {"name": x.filename, "size": len(x.content)} for x in attachments
        ])


if __name__ == '__main__':
    # app.run(debug=True)
    if not app.config['DEBUG']:
        totp = PyOTP(app)
        mail = Mail()
