import config
from etcd3 import client
from flask import Flask
# from flask import config
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from redis import Redis

"""
flask_migrate作用：
1、通过命令的方式创建表
2、修改表的结构
"""
app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)
manager = Manager(app)

# 第一个参数是flask实例，第二个参数SQLAlchemy实例
Migrate(app, db)

# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command("db", MigrateCommand)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    title = db.Column(db.String(128))
    us = db.relationship("User", backref="role")


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))


@app.route("/index", methods=["GET", "POST"])
def index():
    leehom_info = Role.query.filter_by(id=1).first()
    print(leehom_info.name)
    return "index"


def login():
    return 'hello world'


app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])


if __name__ == '__main__':
    r = Redis(host="127.0.0.1", port=6379, password=123456)
    print(bytes.decode(r.get("mykey")))

    e = client(host="127.0.0.1", port=2379)
    etcd_my_key, _ = e.get("mykey")
    print(bytes.decode(etcd_my_key))

    app.run(debug=True, port=5000, host="127.0.0.1")
