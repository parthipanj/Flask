from flask import Blueprint, request

from base.db import get_db
from user.service import UserService

bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@bp.route('', methods=['GET', 'POST'])
def users():
    """
    Create a new user

    """
    response = None
    db = get_db()
    user_service = UserService(db)

    if request.method == 'POST':
        request_json = request.get_json()
        response = user_service.create(request_json)
    elif request.method == 'GET':
        page_num = int(request.args.get('page_num', 0))
        page_size = int(request.args.get('page_size', 10))
        response = user_service.list(page_num, page_size)

    return response


@bp.route('/<uuid:user_id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def user(user_id):
    response = None
    db = get_db()
    request_json = request.get_json(silent=True)
    user_service = UserService(db)

    if request.method == 'GET':
        response = user_service.retrieve(user_id)
    elif request.method == 'PUT':
        response = user_service.update(user_id, request_json)
    elif request.method == 'PATCH':
        response = user_service.partial_update(user_id, request_json)
    elif request.method == 'DELETE':
        response = user_service.delete(user_id)

    return response
