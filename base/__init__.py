from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from .generic import response
from .generic.exceptions import ValidationException


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import db
    db.init_app(app)

    from .generic import exceptions
    exceptions.register_exceptions(app)

    from auth import bp as auth_bp
    from user import bp as user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    register_route(app)

    return app


def register_route(app):
    # route to check the service status
    @app.route('/status')
    def hello():
        return 'Service is up and running!'
