class ValidationException(Exception):

    def __init__(self, errors):
        Exception.__init__(self)
        self.errors = errors
        self.status_code = 422
