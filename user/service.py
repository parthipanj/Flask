from werkzeug.security import generate_password_hash

from base.db.mongodb import DocumentService
from base.generic import generate_id, date_fields, response
from base.generic.exceptions import NotFoundException
from base.generic.validation import Validation


class UserService(object):

    def __init__(self, db):
        self.document_service = DocumentService(db, collection='users')
        self.validation = Validation(self.document_service)

    def retrieve_user(self, user_id, raise_error=True):
        user = self.document_service.find_one({'_id': user_id}, {'password': 0})

        if not user and raise_error:
            raise NotFoundException(message='User not exists.')

        return user

    def retrieve_user_by_email(self, email, raise_error=True):
        user = self.document_service.find_one({'email': email})

        if not user and raise_error:
            raise NotFoundException(message='User not exists.')

        return user

    def save(self, user, user_id=None):
        if user_id:
            return self.document_service.update_one({'_id': user_id}, user)

        return self.document_service.insert_one(user)

    def create(self, request_data) -> dict:
        rules = {
            'first_name': 'required|alpha|max:50',
            'last_name': 'max:50',
            'email': ['required', 'email', 'unique:users'],
            'password': {'min:5'},
            'dob': 'date',
            'status': 'boolean'
        }
        self.validation.validate(rules, request_data)

        request_data['_id'] = generate_id()
        password = request_data.get('password')
        request_data['password'] = generate_password_hash(password) if password else None
        request_data['status'] = request_data.get('status', False)
        request_data.update(date_fields())

        return_document = self.save(request_data)

        return response(data=return_document.inserted_id, status_code=201)

    def list(self, page_num: int, page_size: int):
        user_list = self.document_service.find(projection={'password': 0}, skip=page_num, limit=page_size)
        total_document = self.document_service.count()

        pagination = {
            'result': user_list,
            'next': page_num + 1 if page_num < total_document > page_size else None,
            'previous': page_num - 1 if page_num else None,
            'total': total_document
        }

        return response(data=pagination)

    def retrieve(self, user_id):
        user = self.retrieve_user(user_id)

        return response(data=user)

    def update(self, user_id, request_data, *, partial_update=False):
        if not partial_update:
            rules = {'first_name': 'required|max:50', 'last_name': 'max:50',
                     'email': ['required', 'email', 'unique:users,{}'.format(user_id)],
                     'password': {'min:5'}, 'dob': 'date', 'status': 'boolean'}
        else:
            rules = {'first_name': 'max:50', 'last_name': 'max:50',
                     'email': ['email', 'unique:users,{}'.format(user_id)], 'password': {'min:5'},
                     'dob': 'date', 'status': 'boolean'}
        self.validation.validate(rules, request_data)

        user = self.retrieve_user(user_id)

        password = request_data.get('password')
        if password:
            request_data['password'] = generate_password_hash(password)

        request_data.update(date_fields(request_data.get('create_at')))

        return_document = self.save(request_data, user['_id'])

        return response(data=return_document.upserted_id)

    def partial_update(self, user_id, request_data):
        return self.update(user_id, request_data, partial_update=True)

    def delete(self, user_id):
        user = self.retrieve_user(user_id)

        self.document_service.delete_one({'_id': user['_id']})

        return response(status_code=204)
