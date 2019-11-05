from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    games = db.relationship('Game', backref='player', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.Integer)
    stage = db.Column(db.Integer) #注意这里的stage记录的是最大值
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_time = db.Column(db.DateTime, default=datetime.utcnow)
    ps = db.Column(db.String(140))
    # 创建时间，上次时间，备注信息, 隶属班级
    decision1 = db.relationship('Decision1', backref='game', lazy='dynamic')
    decision2 = db.relationship('Decision2', backref='game', lazy='dynamic')
    result1 = db.relationship('Result1', backref='game', lazy='dynamic')
    state = db.Column(db.Integer)  # 是否已删除 0删除 1正常
    #增加备注，删除功能

"""
class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    adminid = db.relationship('user', backref='admin', lazy='dynamic')
    gid = db.Column(db.Integer)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.Column(db.Integer)  # 是否已删除 0删除 1正常
    #增加备注，删除功能

groups = db.Table(
    'followers',
    db.Column('group_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

还要在game中添加属性，表明此game是否属于团队模式，如果是，值为团队id，如果否则为0

"""



class Decision1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock = db.Column(db.String(140))
    contract = db.Column(db.String(140))
    quality = db.Column(db.String(140))
    batch = db.Column(db.Integer)
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))


class Decision2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dc = db.Column(db.String(140))
    location = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 只需要game id就能够定位到用户和game
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))


class Result1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    revenue = db.Column(db.DECIMAL(10, 2), default=0.0)
    sales = db.Column(db.DECIMAL(10, 2), default=0.0)
    penalty = db.Column(db.DECIMAL(10, 2), default=0.0)
    salvage = db.Column(db.DECIMAL(10, 2), default=0.0)
    procure = db.Column(db.DECIMAL(10, 2), default=0.0)
    manage = db.Column(db.DECIMAL(10, 2), default=0.0)
    # 以后可以加一个state，用于表示是否计算完成。在计算完成后更新为1，此时展示计算结果
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

