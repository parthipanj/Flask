from base import response
from .not_found import NotFoundException
from .validation import ValidationException


def handle_validation_exception(error):
    return response(errors=error.errors, status_code=error.status_code)


def handle_not_found_exception(error):
    return response(message=error.message, status_code=error.status_code)


def register_exceptions(app):
    app.register_error_handler(ValidationException, handle_validation_exception)
    app.register_error_handler(NotFoundException, handle_not_found_exception)
