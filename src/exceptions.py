from werkzeug.exceptions import HTTPException


class TemplateNotFound(HTTPException):
    code = 404
    description = 'Template not found in "templates".'


class MissingArguments(HTTPException):
    code = 400
    description = 'Some expected arguments are missing.'
