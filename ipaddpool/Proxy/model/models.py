from datetime import datetime
from Proxy.utils.avatar import get_pic
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password_hash = db.Column(db.String(128))
    createtime = db.Column(db.DateTime,default=datetime.now)
    locked = db.Column(db.Boolean,default=False)
    description = db.Column(db.String(128),default="我不是英雄，我只做我想做的事，保护我想要保护的人而已。")
    avatar = db.Column(db.String(128),default=get_pic())
    role_id = db.Column(db.Integer,db.ForeignKey('role.r_id'),default=3)

    def __init__(self,username,password):
        self.username = username
        self.generate_password(password=password)

    def generate_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,pasword):
        return check_password_hash(self.password_hash,password=pasword)

    def get(id):
        return User.query.filter_by(id=id).first()

    def deluser(self):
        db.session.delete(self)
        db.session.commit()

    def updatepwd(self,password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def lockuser(self,lock):
        self.locked = lock
        db.session.commit()

    def uppic(self,src):
        self.avatar = src
        db.session.commit()

    def updesc(self,des):
        self.description = des
        db.session.commit()

    def addrole(self,roleid):
        self.role_id = roleid
        db.session.commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def save(self):
        db.session.add(self)
        db.session.commit()


role_permission = db.Table('role_permission',
                           db.Column('role_id',db.Integer,db.ForeignKey('role.r_id'),primary_key=True),
                           db.Column('permission_id',db.Integer,db.ForeignKey('permission.p_id'),primary_key=True)
                           )

class Role(db.Model):
    __tablename__ = 'role'
    r_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    r_name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __init__(self,r_name):
        self.r_name = r_name

    def save(self):
        db.session.add(self)
        db.session.commit()

class Permission(db.Model):
    __tablename__ = 'permission'
    p_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    p_zhname = db.Column(db.String(64),unique=True)
    p_enname = db.Column(db.String(64),unique=True)
    roles = db.relationship('Role',secondary=role_permission,backref=db.backref('permission',lazy='dynamic'))

    def __init__(self,p_zhname,p_enname):
        self.p_zhname = p_zhname
        self.p_enname = p_enname

    def save(self):
        db.session.add(self)
        db.session.commit()

class Iplist(db.Model):
    __tablename__ = 'iplist'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    ip = db.Column(db.String(64))
    port = db.Column(db.Integer)
    httptype = db.Column(db.String(64))
    address = db.Column(db.String(64))
    isp = db.Column(db.String(64))
    spend = db.Column(db.Float)
    createtime = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,ip,port,httptype,address,isp,spend,createtime):
        self.ip = ip
        self.port = port
        self.httptype = httptype
        self.address = address
        self.isp = isp
        self.spend = spend
        self.createtime = createtime

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict