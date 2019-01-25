from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('User', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
    })


class AuthDto:
    api = Namespace('', description='Authentication')
    user_auth = api.model('Authentication', {
        'username': fields.String(required=True, description='The user name'),
        'password': fields.String(required=True, description='The user password '),
    })
