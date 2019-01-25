from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_a_user
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc(security='apikey')
    @jwt_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self):
        """User registration"""
        data = request.json
        return save_new_user(data=data)


@api.route('/<username>')
@api.param('username', 'The user name')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc(security='apikey')
    @jwt_required
    @api.marshal_with(_user)
    def get(self, username):
        """get a user given its identifier"""
        user = get_a_user(username)
        if not user:
            api.abort(404)
        else:
            return user
