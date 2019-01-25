
from .. import db, flask_bcrypt
from passlib.hash import pbkdf2_sha256 as sha256
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
#import jwt

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "t_users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    
    email = db.Column(db.String(255), unique=True)
    registered_on = db.Column(db.DateTime,default=datetime.datetime.utcnow())
    admin = db.Column(db.Boolean, nullable=False,default=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    area = db.Column(db.Integer, default=30)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    # @property
    # def password(self):
    #     raise AttributeError('password: write-only field')

    # @password.setter
    # def password(self, password):
    #     self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    # def check_password(self, password):
    #     return flask_bcrypt.check_password_hash(self.password_hash, password)

    # @staticmethod
    # def encode_auth_token(user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         payload = {
    #             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
    #             'iat': datetime.datetime.utcnow(),
    #             'sub': user_id
    #         }
    #         return jwt.encode(
    #             payload,
    #             key,
    #             algorithm='HS256'
    #         )
    #     except Exception as e:
    #         return e

    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """
    #     Decodes the auth token
    #     :param auth_token:
    #     :return: integer|string
    #     """
    #     try:
    #         payload = jwt.decode(auth_token, key)
    #         is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
    #         if is_blacklisted_token:
    #             return 'Token blacklisted. Please log in again.'
    #         else:
    #             return payload['sub']
    #     except jwt.ExpiredSignatureError:
    #         return 'Signature expired. Please log in again.'
    #     except jwt.InvalidTokenError:
    #         return 'Invalid token. Please log in again.'

    # def __repr__(self):
    #     return "<User '{}'>".format(self.username)
