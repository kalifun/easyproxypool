from functools import wraps
from flask import request,abort,jsonify
from Proxy.utils.auth import Auth
from Proxy.model.models import User

def is_login(func):
    @wraps(func)
    def check_login(*args,**kwargs):
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            print(auth_tokenArr)
            if (not auth_tokenArr or len(auth_tokenArr) != 2):
                return abort(401)
                # return jsonify({}),401
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                print(payload)
                if not isinstance(payload, str):
                    user = User.get(id=payload['headers']['user_id'])
                    if (user is None):
                        return jsonify({"error":"找不到该用户信息"}),401
                    else:
                        return func(*args,**kwargs)
                else:
                    return jsonify({'error':"认证失败"}),401
        else:
            return jsonify({'error':'401'}), 401
            # return redirect(url_for('api.regist'))
    return check_login