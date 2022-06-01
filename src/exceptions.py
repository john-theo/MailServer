from werkzeug.exceptions import HTTPException


class InvalidTOTP(HTTPException):
    code = 403
    description = 'Invalid TOTP.'


class TemplateNotFound(HTTPException):
    code = 404
    description = 'Template not found in "templates".'


class MissingArguments(HTTPException):
    code = 400
    description = 'Some expected arguments are missing.'
