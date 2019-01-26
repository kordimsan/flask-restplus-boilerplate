from flask import request
from flask_jwt_extended import (jwt_required)
from flask_restplus import Resource

from ..service.user_service import save_new_user, get_all_users, get_a_user
from ..util.dto import UserDto

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
