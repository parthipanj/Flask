import re
import uuid
from datetime import datetime

from .exceptions import ValidationException


class Validation(object):

    def __init__(self, document_service):
        self.document_service = document_service
        self.errors = dict()

    def _error(self, key, rule, message):
        error = {rule: message}

        if key in self.errors:
            self.errors[key].update(error)
        else:
            self.errors[key] = error

    def required(self, key, value, rule):
        if not value:
            self._error(key, rule, 'The {} field is required.'.format(key))

    def alpha(self, key, value, rule):
        if value and not value.isalpha():
            self._error(key, rule, 'The {} must only contain letters.'.format(key))

    def max(self, key, value, rule):
        if value and len(value) > int(rule[1]):
            self._error(key, rule[0], 'The {} must not be greater than {}.'.format(key, rule[1]))

    def min(self, key, value, rule):
        if value and len(value) < int(rule[1]):
            self._error(key, rule[0], 'The {} must at least {}.'.format(key, rule[1]))

    def email(self, key, value, rule):
        regex = r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
        if value and re.search(regex, value, re.I) is None:
            self._error(key, rule, 'The {} must be a valid email address.'.format(key))

    def date(self, key, value, rule):
        try:
            if value and datetime.strptime(value, '%Y-%m-%d'):
                return
        except ValueError:
            self._error(key, rule, 'The {} is not a valid date.'.format(key))

    def boolean(self, key, value, rule):
        if value and not isinstance(value, bool):
            self._error(key, rule, 'The {} field must be true or false.'.format(key))

    def unique(self, key, value, rule):
        query = {key: value}
        split_rule = rule[1].split(',')

        if len(split_rule) > 1:
            query.update({'_id': {'$ne': uuid.UUID(split_rule[1])}})

        if value and self.document_service.count(query):
            self._error(key, rule[0], 'The {} has already been taken.'.format(key))

    def validate(self, fields_rules: dict, data: dict):
        for key, rules in fields_rules.items():
            if isinstance(rules, str):
                rules = rules.split('|')

            for rule in rules:
                split_rule = rule.split(':')
                if hasattr(self, split_rule[0]):
                    getattr(self, split_rule[0])(key, data.get(key),
                                                 split_rule[0] if len(split_rule) == 1 else split_rule)

        if self.errors:
            raise ValidationException(errors=self.errors)
