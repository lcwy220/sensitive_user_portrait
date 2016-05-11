# -*- coding: utf-8 -*-

from flask import Flask
from elasticsearch import Elasticsearch
from flask_debugtoolbar import DebugToolbarExtension
from sensitive_user_portrait.extensions import admin
from sensitive_user_portrait.jinja import gender, tsfmt, Int2string, gender_text, user_email, user_location, user_birth, user_vertify, weibo_source
from sensitive_user_portrait.social_sensing.views import mod as socialsensingModule
from sensitive_user_portrait.index.views import mod as indexModule
from sensitive_user_portrait.recommentation.views import mod as recommentationModule
from sensitive_user_portrait.group.views import mod as groupModule
from sensitive_user_portrait.tag.views import mod as tagModule
from sensitive_user_portrait.attribute.views import mod as attributeModule
from sensitive_user_portrait.overview.views import mod as overviewModule
from sensitive_user_portrait.imagine.views import mod as imagineModule
from sensitive_user_portrait.manage_sensitive_words.views import mod as wordsmanagementModule
from sensitive_user_portrait.delete_user.views import mod as deleteModule
from sensitive_user_portrait.influence_application.views import mod as influenceModule
from sensitive_user_portrait.user_rank.views import mod as userrankModule
from sensitive_user_portrait.weibo_rank.views import mod as weiborankModule
from sensitive_user_portrait.portrait_search.views import mod as searchModule
from sensitive_user_portrait.detect.views import mod as detectModule
"""
from sensitive_user_portrait.attribute.views import mod as attributeModule
from sensitive_user_portrait.manage.views import mod as manageModule
from sensitive_user_portrait.profile.views import mod as profileModule
from sensitive_user_portrait.overview.views import mod as overviewModule
from sensitive_user_portrait.influence_application.views import mod as influenceModule
from sensitvie_user_portrait.login.views import mod as loginModule
from sensitive_user_portrait.weibo.views import mod as weiboModule
"""

def create_app():
    app = Flask(__name__)

    register_blueprints(app)
    register_extensions(app)
    register_jinja_funcs(app)

    # Create modules

    # the debug toolbar is only enabled in debug mode
    app.config['DEBUG'] = True

    app.config['ADMINS'] = frozenset(['youremail@yourdomain.com'])
    app.config['SECRET_KEY'] = 'SecretKeyForSessionSigning'
    
    '''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://%s:@%s/%s?charset=utf8' % (MYSQL_USER, MYSQL_HOST, MYSQL_DB)
    app.config['SQLALCHEMY_ECHO'] = False
    '''
    app.config['DATABASE_CONNECT_OPTIONS'] = {}

    app.config['THREADS_PER_PAGE'] = 8

    app.config['CSRF_ENABLED'] = True
    app.config['CSRF_SESSION_KEY'] = 'somethingimpossibletoguess'

    # Enable the toolbar?
    app.config['DEBUG_TB_ENABLED'] = app.debug
    # Should intercept redirects?
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
    # Enable the profiler on all requests, default to false
    app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    # Enable the template editor, default to false
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    
    # debug toolbar
    # toolbar = DebugToolbarExtension(app)
    
    return app
   

def register_blueprints(app):
    app.register_blueprint(indexModule)
    app.register_blueprint(recommentationModule)
    app.register_blueprint(groupModule)
    app.register_blueprint(tagModule)
    app.register_blueprint(attributeModule)
    app.register_blueprint(overviewModule)
    app.register_blueprint(imagineModule)
    app.register_blueprint(searchModule)
    app.register_blueprint(wordsmanagementModule)
    app.register_blueprint(deleteModule)
    app.register_blueprint(influenceModule)
    app.register_blueprint(userrankModule)
    app.register_blueprint(weiborankModule)
    app.register_blueprint(socialsensingModule)
    app.register_blueprint(detectModule)
    """
    app.register_blueprint(attributeModule)
    app.register_blueprint(manageModule)
    app.register_blueprint(overviewModule)
    app.register_blueprint(influenceModule)
    app.register_blueprint(loginModule)
    app.register_blueprint(weiboModule)
    """


def register_extensions(app):
    app.config.setdefault('ES_USER_PROFILE_URL', 'http://219.224.135.97:9208/')
    app.extensions['es_user_profile'] = Elasticsearch(app.config['ES_USER_PROFILE_URL'])
    app.config.setdefault('ES_USER_PORTRAIT_URL', 'http://219.224.135.93:9200/')
    app.extensions['es_user_portrait'] = Elasticsearch(app.config['ES_USER_PORTRAIT_URL'])

def register_jinja_funcs(app):
    funcs = dict(gender=gender,
                 tsfmt=tsfmt,
                 int2string=Int2string,
                 gender_text=gender_text,
                 user_email=user_email,
                 user_location=user_location,
                 user_birth=user_birth,
                 user_vertify=user_vertify,
                 weibo_source=weibo_source)
    app.jinja_env.globals.update(funcs)
