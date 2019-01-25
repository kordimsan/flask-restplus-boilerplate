import uuid
import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from app.main import db
from app.main.model.user import User
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)


def save_new_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=User.generate_hash(data['password'])
        )
        new_user.save_to_db()
        access_token = create_access_token(identity=data['username'])

        return {
            'message': 'User {} was created'.format(data['username']),
            'access_token': 'Bearer ' + access_token,
        }
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def get_all_users():
    return User.query.all()


def get_a_user(username):
    return User.query.filter_by(username=username).first()

# def generate_token(user):
#     try:
#         # generate the auth token
#         auth_token = User.encode_auth_token(user.id)
#         response_object = {
#             'status': 'success',
#             'message': 'Successfully registered.',
#             'Authorization': auth_token.decode()
#         }
#         return response_object, 201
#     except Exception as e:
#         response_object = {
#             'status': 'fail',
#             'message': 'Some error occurred. Please try again.'
#         }
#         return response_object, 401
