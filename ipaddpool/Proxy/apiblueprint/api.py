from flask import Blueprint,jsonify,request,abort,url_for
from Proxy.model.models import db,User,Permission,Role,Iplist
from Proxy.utils.auth import Auth
from Proxy.utils.Decorator import is_login
from flask_cors import *

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
                # decodtoken = Auth.decode_auth_token(auth_token=token)
                # alluser = User.query.all()
                # result = []
                # for newlist in alluser:
                #     result.append(newlist.to_json())
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
            alluser = User.query.filter(User.role_id == 3).all()
            # print(alluser)
            # alluser = User.query.all()
            result = []
            for newlist in alluser:
                dic = {}
                userjson = newlist.to_json()
                id = userjson['id']
                username = userjson["username"]
                createtime = userjson["createtime"]
                # locked = int(bool(userjson['locked']))
                locked = bool(userjson['locked'])
                role = Role.query.filter(Role.r_id == 3).first()
                rolename = role.r_name
                permission = ["改"]
                dic['id'] = id
                dic['username'] = username
                dic['createtime'] = createtime
                dic['status'] = locked
                dic['permission'] = permission
                dic['role'] = rolename
                result.append(dic)
            return jsonify({"data": result})
        if role == 3:
            alluser = User.query.filter(User.id == user_id).all()
            result = []
            for newlist in alluser:
                dic = {}
                userjson = newlist.to_json()
                id = userjson['id']
                username = userjson["username"]
                createtime = userjson["createtime"]
                locked = bool(userjson['locked'])
                role_id = userjson["role_id"]
                role = Role.query.filter(Role.r_id == role_id).first()
                rolename = role.r_name
                permission = ["改"]
                dic['id'] = id
                dic['username'] = username
                dic['createtime'] = createtime
                dic['status'] = locked
                dic['permission'] = permission
                dic['role'] = rolename
                result.append(dic)
            return jsonify({"data":result})

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
            alluser = User.query.filter(User.role_id == 2).all()
            # alluser = User.query.all()
            result = []
            for newlist in alluser:
                dic = {}
                userjson = newlist.to_json()
                id = userjson['id']
                username = userjson["username"]
                createtime = userjson["createtime"]
                locked = bool(userjson['locked'])
                role = Role.query.filter(Role.r_id == 2).first()
                rolename = role.r_name
                permission = ["添加","改","查"]
                dic['id'] = id
                dic['username'] = username
                dic['createtime'] = createtime
                dic['status'] = locked
                dic['permission'] = permission
                dic['role'] = rolename
                result.append(dic)
            return jsonify({"data": result})
        elif role == 2:
            alluser = User.query.filter(User.id == user_id).all()
            # alluser = User.query.all()
            result = []
            for newlist in alluser:
                dic = {}
                userjson = newlist.to_json()
                id = userjson['id']
                username = userjson["username"]
                createtime = userjson["createtime"]
                locked = bool(userjson['locked'])
                role_id = userjson["role_id"]
                role = Role.query.filter(Role.r_id == role_id).first()
                rolename = role.r_name
                permission = ["添加", "改", "查"]
                dic['id'] = id
                dic['username'] = username
                dic['createtime'] = createtime
                dic['status'] = locked
                dic['permission'] = permission
                dic['role'] = rolename
                result.append(dic)
            return jsonify({"data": result})
        else:
            return jsonify({"message":"无权访问"}),403

@api.route('/adduser',methods=['GET','POST'])
@cross_origin()
@is_login
def adduser():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':
        if not all([username,password]):
            abort(401)
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({"error": "用户已经存在"})
        else:
            User(username=username, password=password).save()
            return jsonify({"success": username})

@api.route('/delete',methods=['GET','POST'])
@cross_origin()
@is_login
def deluser():
    username = request.json.get('username')
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        if user:
            if user.role_id == 1:
                return jsonify({"message": "无权限删除"}), 403
            else:
                user.deluser()
                return jsonify({"message": "用户已删除"})

        else:
            abort(401)

@api.route('/upwd',methods=['GET','POST'])
@cross_origin()
# @is_login
def updatepwd():
    username = request.form.get("username")
    oldpwd = request.form.get("oldpwd")
    newpwd = request.form.get('newpwd')
    if not all([username,oldpwd,newpwd]):
        abort(401)
    user = User.query.filter_by(username=username).first()
    if user:
        if user.check_password(oldpwd):
            print(user.password_hash)
            user.updatepwd(newpwd)
            print(user.password_hash)
            return jsonify({"success":"ssss"})
        else:
            return jsonify({"error":"密码错误"})
    else:
        return jsonify({"error":"用户不存在"})


@api.route('/lock',methods=['GET','POST'])
@cross_origin()
@is_login
def lockuser():
    username = request.json.get('username')
    userlock = request.json.get('userlock')
    print(username,userlock)
    if request.method == 'POST':
        if not all([username,str(userlock)]):
            abort(401)
        user = User.query.filter_by(username=username).first()
        print(type(userlock))
        if type(userlock) == bool:
            user.lockuser(userlock)
            return jsonify({"success":"执行完成"})

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