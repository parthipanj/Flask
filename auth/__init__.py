import functools

from flask import Blueprint, request, session, g

from base.db import get_db
from base.generic.exceptions import NotFoundException
from user.service import UserService
from .service import AuthService

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        user_service = UserService(db)
        g.user = user_service.retrieve_user(user_id, False)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return NotFoundException(message='User not found.')

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=['POST'])
def register():
    request_json = request.get_json()
    db = get_db()
    auth_service = AuthService(db)

    return auth_service.register(request_json)


@bp.route('/login', methods=['POST'])
def login():
    request_json = request.get_json()
    db = get_db()
    auth_service = AuthService(db)

    return auth_service.login(request_json)


@bp.route('/logout', methods=['POST'])
def logout():
    db = get_db()
    auth_service = AuthService(db)

    return auth_service.logout()
