from flask import Blueprint,jsonify,request,abort,url_for
from Proxy.model.models import db,User,Permission,Role,Iplist
from Proxy.utils.auth import Auth
from Proxy.utils.Decorator import is_login
from flask_cors import *
from Proxy.utils.avatar import get_pic
from Proxy.apiblueprint.Batchprocessing import UserAuthentication

api = Blueprint('api',__name__)

@api.route('/',methods=['GET','POST'])
def hello():
    if request.method == 'GET':
        return jsonify({'message':'Hello'})

@api.route('/regist',methods=['GET','POST'])
@cross_origin()
def regist():
    if request.method == 'GET':
        return url_for('/regist')
    if request.method == 'POST':
        username = request.json.get("username")
        password = request.json.get("password")
        password1 = request.json.get("password1")
        if not all([username,password,password1]):
            return jsonify({"message":"参数不完整"}),401
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"message":"用户已经存在"}),401
        elif password == password1:
            User(username=username,password=password).save()
            return jsonify({"message":"创建成功"})
        else:
            return jsonify({"message":"密码不同"}),401

@api.route('/login',methods=['GET','POST'])
@cross_origin()
def getusers():
    if request.method == 'POST':
        username = request.json.get("username")
        password = request.json.get("password")
        print(username,password)
        if not all([username,password]):
            abort(401)
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password) & bool(1- (user.locked)):
                token = Auth.encode_auth_token(user_id=user.id)
                return jsonify({"Authorization":token.decode()})
            elif bool(user.locked):
                return jsonify({'message':"账号已锁定"}),401
            else:
                return jsonify({'message':"账号密码不存在"}),401
        else:
            abort(401)

@api.route('/userlist',methods=['GET','POST'])
@cross_origin()
@is_login
def userlist():
    if request.method == 'GET':
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        role = tokeninfo[0]
        user_id = tokeninfo[1]
        if role == 1 or role == 2:
            result = UserAuthentication.Get_User_List(3)
            return jsonify({"data": result})
        else:
            return jsonify({"message":"无权限"}),403
        # if role == 3:
        #     result = UserAuthentication.Get_User(user_id)
        #     return jsonify({"data":result})

@api.route('/adminlist',methods=['GET','POST'])
@cross_origin()
@is_login
def adminlist():
    if request.method == 'GET':
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        role = tokeninfo[0]
        user_id = tokeninfo[1]
        if role == 1:
            result = UserAuthentication.Get_User_List(2)
            return jsonify({"data": result})
        elif role == 2:
            # result = UserAuthentication.Get_User(user_id)
            # return jsonify({"data": result})
            return jsonify({"message": "无权访问"}), 403
        else:
            return jsonify({"message":"无权访问"}),403

@api.route('/adduser',methods=['GET','POST'])
@cross_origin()
@is_login
def adduser():
    username = request.json.get('username')
    password = request.json.get('password')
    usertype = request.json.get('usertype')
    Authorization = request.headers.get("Authorization")
    tokeninfo = Auth.put_user_role(Authorization)
    role = tokeninfo[0]
    user_id = tokeninfo[1]
    if request.method == 'POST':
        print(username,password,usertype)
        if not all([username,password,usertype]):
            return jsonify({"message": "参数不完整"}),403
        elif int(usertype) == 1:
            return jsonify({"message": "无权限创建"}), 403
        elif role == int(usertype):
            return jsonify({"message": "无权限创建"}), 403
        elif role == 3:
            return jsonify({"message": "无权限访问"}), 403
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"message": "用户已经存在"}),403
        else:
            User(username=username, password=password).save()
            check = User.query.filter(User.username == username).first()
            check.addrole(usertype)
            return jsonify({"message": "创建成功"})


@api.route('/delete',methods=['GET','POST'])
@cross_origin()
@is_login
def deluser():
    if request.method == 'POST':
        username = request.json.get('username')
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        user_id = tokeninfo[1]
        result = UserAuthentication.Delete_user(user_id,username)
        if result == True:
            return jsonify({"message": "用户已删除"})
        else:
            return jsonify({"message": "无权限删除"}), 403

@api.route('/upwd',methods=['GET','POST'])
@cross_origin()
@is_login
def updatepwd():
    username = request.json.get("username")
    oldpwd = request.json.get("oldpwd")
    newpwd = request.json.get('newpwd')
    Authorization = request.headers.get("Authorization")
    tokeninfo = Auth.put_user_role(Authorization)
    user_id = tokeninfo[1]
    if request.method == 'POST':
        print(username,oldpwd,newpwd)
        if not all([username,oldpwd,newpwd]):
            return jsonify({"message": "参数不完整"}),401
        result = UserAuthentication.Upwd_user(user_id,username,oldpwd,newpwd)
        if result == True:
            return jsonify({"message": "修改成功"})
        else:
            return jsonify({"message": "修改失败"}),403

@api.route('/admin/upwd',methods=['GET','POST'])
@cross_origin()
@is_login
def admin_upwd():
    if request.method == 'POST':
        username = request.json.get("username")
        newpwd = request.json.get('newpwd')
        oldpwd = ""
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        role = tokeninfo[0]
        user_id = tokeninfo[1]
        if role == 1 or role == 2:
            result = UserAuthentication.Upwd_user(user_id,username,oldpwd,newpwd)
        else:
            abort(401)
        if result == True:
            return jsonify({"message": "修改成功"})
        else:
            return jsonify({"message": "修改失败"}), 403

@api.route('/lock',methods=['GET','POST'])
@cross_origin()
@is_login
def lockuser():
    username = request.json.get('username')
    userlock = request.json.get('userlock')
    print(username,userlock)
    if request.method == 'POST':
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        user_id = tokeninfo[1]
        if not all([username,str(userlock)]):
            abort(401)
        result = UserAuthentication.Locked_user(user_id,username,userlock)
        if result == True:
            return jsonify({"message": "执行完成"})
        else:
            return jsonify({"message": "无权限执行"}),404

@api.route('/iplist',methods=['GET','POST'])
@cross_origin()
@is_login
def iplist():
    if request.method == 'GET':
        getlist = Iplist.query.all()
        result = []
        for newlist in getlist:
            result.append(newlist.to_json())
        return jsonify({"data":result})

@api.route('/about',methods=['GET','POST'])
@cross_origin()
@is_login
def about():
    if request.method == 'GET':
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        s_role = tokeninfo[0]
        user_id = tokeninfo[1]
        result = UserAuthentication.Get_about(user_id,s_role)
        return jsonify({"data":result})

@api.route('/upavatar',methods=['GET','POST'])
@cross_origin()
@is_login
def upavatar():
    Authorization = request.headers.get("Authorization")
    tokeninfo = Auth.put_user_role(Authorization)
    user_id = tokeninfo[1]
    user = User.query.filter(User.id == user_id).first()
    src = get_pic()
    user.uppic(src)
    return jsonify({"message":src})

@api.route('/description',methods=['GET','POST'])
@cross_origin()
@is_login
def description():
    if request.method == 'POST':
        username = request.json.get("username")
        des = request.json.get("description")
        Authorization = request.headers.get("Authorization")
        tokeninfo = Auth.put_user_role(Authorization)
        user_id = tokeninfo[1]
        user = User.query.filter(User.id == user_id).first()
        if username == user.username:
            user.updesc(des)
            return jsonify({"message":"修改成功"})
        else:
            return jsonify({"message":"修改失败"}),403