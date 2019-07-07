from flask_script import Command
from Proxy.model.models import db,User,Role,Permission

class drop_db(Command):
    def run(self):
        db.drop_all()
        print("---------清除数据库完成---------")

class init_db(Command):
    def run(self):
        db.create_all()
        print("---------role---------")
        r_name = "超级管理员"
        Role(r_name=r_name).save()
        r_name = "管理员"
        Role(r_name=r_name).save()
        r_name = "普通用户"
        Role(r_name=r_name).save()
        print("---------创建role完成---------")

        print("---------permission---------")
        zhadd = "添加"
        enadd = "add"
        Permission(p_zhname=zhadd, p_enname=enadd).save()
        zhdel = "删除"
        endel = "delete"
        Permission(p_zhname=zhdel, p_enname=endel).save()
        zhupd = "改"
        enupd = "update"
        Permission(p_zhname=zhupd, p_enname=enupd).save()
        zhser = "查"
        enser = "serch"
        Permission(p_zhname=zhser, p_enname=enser).save()
        zhloc = "锁定"
        enloc = "lock"
        Permission(p_zhname=zhloc, p_enname=enloc).save()
        print("---------创建permission完成---------")

        print("---------创建role_permission---------")
        superrole_id = 1
        adminrole_id = 2
        usersrole_id = 3
        p_add = 1
        p_del = 2
        p_upd = 3
        p_ser = 4
        p_loc = 5


        role = Role.query.get(superrole_id)
        peradd = Permission.query.get(p_add)
        peradd.roles.append(role)
        perdel = Permission.query.get(p_del)
        perdel.roles.append(role)
        perupd = Permission.query.get(p_upd)
        perupd.roles.append(role)
        perser = Permission.query.get(p_ser)
        perser.roles.append(role)
        perloc = Permission.query.get(p_loc)
        perloc.roles.append(role)

        role = Role.query.get(adminrole_id)
        peradd = Permission.query.get(p_add)
        peradd.roles.append(role)
        perupd = Permission.query.get(p_upd)
        perupd.roles.append(role)
        perser = Permission.query.get(p_ser)
        perser.roles.append(role)

        role = Role.query.get(usersrole_id)
        perupd = Permission.query.get(p_upd)
        perupd.roles.append(role)
        print("---------创建role_permission完成---------")

        print("---------创建用户---------")
        username = "admin"
        password = "admin"
        User(username=username, password=password).save()
        User.query.filter_by(username=username).update({'role_id':'1'})
        db.session.commit()
        print("---------创建用户完成---------")
        print("---------初始化数据库完成---------")
