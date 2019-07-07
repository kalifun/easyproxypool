import jwt,datetime
from flask import jsonify
from Proxy.model.models import User
from Proxy.config.config import Config

class Auth():
    @staticmethod
    def encode_auth_token(user_id):
        try:
            headers = {
                "typ": "JWT",
                "alg": "HS256",
                "user_id": user_id
            }

            payload = {
                "headers": headers,
                "iss": 'ly',
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=0, minutes=2, seconds=0),
                "iat": datetime.datetime.utcnow()
            }
            signature = jwt.encode(payload,Config.SECRET_KEY,algorithm='HS256')
            return signature
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token,Config.SECRET_KEY,options={'verify_exp':False})
            if payload:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
            # return jsonify({"message":"Token过期"}),401
        except jwt.InvalidTokenError:
            return '无效Token'
            # return jsonify({"message":"无效Token"}),401

    @staticmethod
    def put_user_role(auth_token):
        try:
            payload = jwt.decode(auth_token,Config.SECRET_KEY,options={'verify_exp':False})
            if payload:
                user_id = payload['headers']['user_id']
                userinfo = User.get(user_id)
                role = userinfo.role_id
                print(role,user_id)
                return role,user_id
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return False
            # return jsonify({"message":"Token过期"}),401
        except jwt.InvalidTokenError:
            return False
            # return jsonify({"message":"无效Token"}),401
