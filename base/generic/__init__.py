import uuid
from datetime import datetime

from flask import jsonify


def response(**kwargs):
    response_dict = {
        'data': kwargs.get('data'),
        'errors': kwargs.get('errors'),
        'message': kwargs.get('message')
    }
    return jsonify(response_dict), kwargs.get('status_code', 200)


def generate_id() -> uuid.UUID:
    return uuid.uuid4()


def date_fields(create_at=None) -> dict:
    return {
        'created_at': create_at or datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
