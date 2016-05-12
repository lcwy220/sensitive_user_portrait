# -*- coding: utf-8 -*-

from flask.ext import admin
#新加的from import
from flask.ext.pymongo import PyMongo
from flask import request, redirect, url_for, flash
from flask_admin.contrib import sqla
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin, current_user
#__all__ = ['mongo', 'db', 'admin', 'mongo_engine']

__all__ = ['admin']

#db = SQLAlchemy()
#mongo = PyMongo()
#mongo_engine = MongoEngine()
admin = admin.Admin(name=u'系统 数据库管理')



#新加的：以下
db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    # Required for administrative interface. For python 3 please use __str__ instead.
    def __unicode__(self):
        return self.email

    def __name__(self):
        return u'用户管理'

class Role(db.Model, RoleMixin):
    """用户角色
    """
    id = db.Column(db.Integer(), primary_key=True)
    # 该用户角色名称
    name = db.Column(db.String(80), unique=True)
    chname = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    #column_exclude_list = ['name']

    def __unicode__(self):
        return self.name

    def __name__(self):
        return u'角色管理'


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

# Create admin
#admin = admin.Admin(name=u'权限管理', template_mode='role')
#admin = admin.Admin(name=u'权限管理', base_template='/portrait/role_manage.html')

# Create mongo
mongo = PyMongo()