from app.main.model.user import User
from ..service.blacklist_service import save_token
from flask_jwt_extended import create_access_token

class Auth:

    @staticmethod
    def login_user(data):
        username = data.get('username')
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            return {
                       'status': 'success',
                       'message': 'User {} doesn\'t exist'.format(data['username'])
                   }, 401

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return {
                       'message': 'Logged in as {}'.format(current_user.username),
                       'access_token': 'Bearer ' + access_token,
                   }, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'email or password does not match.'
            }
            return response_object, 401
        # try:
        #     # fetch the user data
        #     user = User.query.filter_by(email=data.get('email')).first()
        #     if user and user.check_password(data.get('password')):
        #         #auth_token = User.encode_auth_token(user.id)
        #         auth_token = create_access_token(identity = user.id)
        #         if auth_token:
        #             response_object = {
        #                 'status': 'success',
        #                 'message': 'Successfully logged in.',
        #                 'Authorization': auth_token
        #             }
        #             return response_object, 200
        #     else:
        #         response_object = {
        #             'status': 'fail',
        #             'message': 'email or password does not match.'
        #         }
        #         return response_object, 401

        # except Exception as e:
        #     print(e)
        #     response_object = {
        #         'status': 'fail',
        #         'message': 'Try again',
        #         'exception': e.message
        #     }
        #     return response_object, 500

    @staticmethod
    def logout_user(data):
        print(data)
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
