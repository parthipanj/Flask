from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

from base.db.mongodb import DocumentService
from base.generic import response, generate_id, date_fields
from base.generic.validation import Validation
from user.service import UserService


class AuthService(object):

    def __init__(self, db):
        self.document_service = DocumentService(db, collection='users')
        self.validation = Validation(self.document_service)
        self.user_service = UserService(db)

    def register(self, request_data) -> dict:
        rules = {'first_name': 'required|max:50', 'last_name': 'max:50',
                 'email': ['required', 'email', 'unique:users'], 'password': {'required', 'min:5'}, 'dob': 'date'}
        self.validation.validate(rules, request_data)

        request_data['_id'] = generate_id()
        request_data['password'] = generate_password_hash(request_data.get('password'))
        request_data['status'] = True
        request_data.update(date_fields())

        return_document = self.user_service.save(request_data)

        return response(data=return_document)

    def login(self, request_data) -> dict:
        rules = {'email': ['required', 'email'], 'password': {'required', 'min:5'}}
        self.validation.validate(rules, request_data)

        user = self.user_service.retrieve_user_by_email(request_data.get('email'), False)

        if not user:
            return response(message='Incorrect email.', status_code=401)
        elif not check_password_hash(user['password'], request_data.get('password')):
            return response(message='Incorrect password.', status_code=401)

        session.clear()
        session['user_id'] = user['_id']
        del user['password']

        return response(data=user)

    def logout(self):
        session.clear()
        return response()
