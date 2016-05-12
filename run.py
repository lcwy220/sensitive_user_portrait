# -*- coding: utf-8 -*-

from optparse import OptionParser

from sensitive_user_portrait import create_app
#新加的import
from flask_login import current_user
from flask import g, session, flash, redirect, request, render_template
from flask_security.utils import logout_user
from sensitive_user_portrait import create_app
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
            UserMixin, RoleMixin, login_required
from sensitive_user_portrait.extensions import db, user_datastore, mongo

optparser = OptionParser()
optparser.add_option('-p', '--port', dest='port', help='Server Http Port Number', default=9001, type='int')
(options, args) = optparser.parse_args()

app = create_app()
#app.run(host='0.0.0.0', port=options.port) #本来有 先注释掉
#新加的，以下
@app.route('/create_user_role_test')
def create_user_roles():
    db.drop_all()
    try:
        db.create_all()
        role_1 = user_datastore.create_role(name='userrank',chname=u'用户排名' ,description=u'用户排行模块权限')


        user_1 = user_datastore.create_user(email='admin@qq.com', password="Bh123456")

        user_datastore.add_role_to_user(user_1, role_1)

        db.session.commit()
        return "success"
    except:
        db.session.rollback()
        return "failure"

@app.before_request
def before_request():
    g.user = current_user

@app.after_request
def after_request(response):
    return response
 

@app.route('/')
@login_required
def homepage():
    return render_template('/index/overview.html')

# logout
@app.route('/logout/')
@login_required
def logout():        
    logout_user()
    #flash(u'You have been signed out')
    flash(u'登出成功')

    return redirect("/login") #redirect(request.args.get('next', None))

import json
from bson import json_util

@app.route('/testmongo/')
def testmongo():
    result = mongo.db.mrq_jobs.find({"path": "tasks.SocialSensing", "params.task_name": "test1", "params.ts": 1459078200})
    rs = []
    for r in result:
        rs.append(r)

    return json.dumps(rs, default=json_util.default)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=options.port)
    app.run()
