#!/user/bin/env python
#coding=utf-8

# @project : ipaddpool
# @author  : kalifun
# @file   : Batchprocessing.py
# @ide    : PyCharm
# @time   : 2019/7/8 10:36
from Proxy.model.models import User,Role,Permission

class UserAuthentication():
    @staticmethod
    def Get_User_List(s_role):
        user = User.query.filter(User.role_id == s_role).all()
        result = []
        for newlist in user:
            dic = {}
            userjson = newlist.to_json()
            id = userjson['id']
            username = userjson["username"]
            createtime = userjson["createtime"]
            locked = bool(userjson['locked'])
            role = Role.query.filter(Role.r_id == s_role).first()
            rolename = role.r_name
            if s_role == 2:
                permission = ["添加", "改", "查"]
            elif s_role == 3:
                permission = ["改"]
            dic['id'] = id
            dic['username'] = username
            dic['createtime'] = createtime
            dic['status'] = locked
            dic['permission'] = permission
            dic['role'] = rolename
            result.append(dic)
        return result
    @staticmethod
    def Get_User(user_id):
        user = User.query.filter(User.id == user_id).first()
        result = []
        dic = {}
        userjson = user.to_json()
        id = userjson['id']
        username = userjson["username"]
        createtime = userjson["createtime"]
        locked = bool(userjson['locked'])
        s_role = user.role_id
        role = Role.query.filter(Role.r_id == s_role).first()
        rolename = role.r_name
        if s_role == 2:
            permission = ["添加", "改", "查"]
        elif s_role == 3:
            permission = ["改"]
        dic['id'] = id
        dic['username'] = username
        dic['createtime'] = createtime
        dic['status'] = locked
        dic['permission'] = permission
        dic['role'] = rolename
        result.append(dic)
        return result

    @staticmethod
    def Delete_user(user_id, deluser):
        Impuser = User.query.filter(User.id == user_id).first()
        Impname = Impuser.username
        role = Impuser.role_id
        user = User.query.filter_by(username=deluser).first()
        if Impname == user.username:
            return False
        if role == 1:
            user.deluser()
            return True
        elif role == 2:
            U_role = user.role_id
            if U_role == 1:
                return False
            elif U_role == 2:
                return False
            else:
                user.deluser()
                return True
        else:
            return False

    @staticmethod
    def Locked_user(user_id,username,lock):
        Impuser = User.query.filter(User.id == user_id).first()
        Impname = Impuser.username
        role = Impuser.role_id
        user = User.query.filter_by(username=username).first()
        if Impname == username:
            return False
        if role == 1:
            user.lockuser(bool(lock))
            return True
        if role == 2:
            u_role = user.role_id
            if role == u_role:
                return False
            elif u_role == 1:
                return False
            else:
                user.lockuser(bool(lock))
                return True
        if role == 3:
            return False

    @staticmethod
    def Upwd_user(user_id,username,oldpwd,newpwd):
        Impuser = User.query.filter(User.id == user_id).first()
        Impname = Impuser.username
        role = Impuser.role_id
        user = User.query.filter_by(username=username).first()
        if username == Impname:
            if user:
                if user.check_password(oldpwd):
                    user.updatepwd(newpwd)
                    return True
                else:
                    return False
            else:
                return False
        elif role == 1:
            if user:
                user.updatepwd(newpwd)
                return True
            else:
                return False
        elif role == 2:
            u_role = user.role_id
            if u_role == 1:
                return False
            elif u_role == 2:
                return False
            elif u_role == 3:
                if User:
                    user.updatepwd(newpwd)
                    return True
                else:
                    return False
        else:
            return False

    @staticmethod
    def Get_about(user_id,s_role):
        result = {}
        if s_role == 1:
            permission = ["添加", "改", "查", "删"]
        elif s_role == 2:
            permission = ["添加", "改", "查"]
        elif s_role == 3:
            permission = ["改"]
        Impuser = User.query.filter(User.id == user_id).first()
        Impname = Impuser.username
        role = Role.query.filter(Role.r_id == s_role).first()
        rolename = role.r_name
        result["username"] = Impname
        result["role"] = rolename
        result["permission"] = permission
        result['avatar'] = Impuser.avatar
        result['description'] = Impuser.description
        return result