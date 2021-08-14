class NotFoundException(Exception):

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
        self.status_code = 404
