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
    decision1 = db.relationship('Decision1', backref='game', lazy='dynamic')
    decision2 = db.relationship('Decision2', backref='game', lazy='dynamic')

class Decision1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(140))
    workers = db.Column(db.Integer)
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))


class Decision2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dc = db.Column(db.String(140))
    location = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 只需要game id就能够定位到用户和game
    gameid = db.Column(db.Integer, db.ForeignKey('game.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

