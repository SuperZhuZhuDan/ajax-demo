from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import json

pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123@localhost:3306/ajax1'

db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(18), unique=True, nullable=True)
    password = db.Column(db.String(32), nullable=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def mk_dict(self):
        dc = {'id': self.id,
              'username': self.username,
              'password': self.password
              }
        return dc

    def __repr__(self):
        return '<users:%r>' % self.username


class Province(db.Model):
    __tablename__ = 'province'
    id = db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(20), unique=True, nullable=True)
    cities = db.relationship('City', backref='province', lazy='dynamic')

    def __init__(self, id, p_name):
        self.id = id
        self.p_name = p_name

    def mk_dict(self):
        dc = {
            'id': self.id,
            'p_name': self.p_name
        }
        return dc

    def __repr__(self):
        return '<Province:%r>' % self.p_name


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(20), nullable=True)
    p_id = db.Column(db.Integer, db.ForeignKey('province.id'))

    def __init__(self, id, c_name, p_id):
        self.id = id
        self.c_name = c_name
        self.p_id = p_id

    def mk_dict(self):
        dc = {
            'id': self.id,
            'c_name': self.c_name,
            'p_id': self.p_id
        }
        return dc

    def __repr__(self):
        return '<City: %r>' % self.c_name


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/01-server')
def server01():
    tt = request.args.get('tx')
    print(tt)
    return tt


@app.route('/02post')
def post2():
    return render_template('post02.html')


@app.route('/02-post', methods=['POST'])
def post02_server():
    uname = request.form.get('uname')
    print(uname)
    rest = db.session.query(Users).filter_by(username=uname).first()
    print(rest)
    if rest:
        return '用户名已存在'
    else:
        return '用户名不存在'


@app.route('/select01')
def select01():
    return render_template('select01.html')

@app.route('/pclin01')
def pclin01():
    return render_template('pcline.html')


@app.route('/p-server01')
def p_server01():
    p = Province.query.all()
    ls = []
    for i in p:
        pd = i.mk_dict()
        ls.append(pd)
        lsj = json.dumps(ls)
    return lsj


@app.route('/select-server01')
def select_server():
    us = db.session.query(Users).all()
    ls = []
    print(us)
    for i in us:
        ls.append(i.mk_dict())
    lsj = json.dumps(ls)
    print(lsj)
    return lsj


@app.route('/c-server01')
def c_server01():
    pid = request.args.get('p_id')
    cclass = City.query.filter_by(p_id=pid).all()
    print(cclass)
    ls = []
    for i in cclass:
        ls.append(i.mk_dict())
    lsj = json.dumps(ls)
    print(lsj)
    return lsj


if __name__ == '__main__':
    app.run(debug=True)
