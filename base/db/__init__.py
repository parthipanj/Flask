import pymongo

from flask import g


def get_db():
    if 'db' not in g:
        client = pymongo.MongoClient(host='192.168.43.98', port=27017)
        g.db = client.Flask
    return g.db


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    with app.app_context():
        get_db()
