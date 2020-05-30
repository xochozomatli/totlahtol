from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from flask_cors import CORS

db = SQLAlchemy() # SQLAlchemy is a wonderful tool for interacting with the database without having to write SQL queries
migrate = Migrate() # Like git, but for your database schema
mail = Mail() # duh, doesn't actually get used
babel = Babel() # Tool for localization, also doesn't get used
cors = CORS() # Rules to prevent (or allow, rip) cross site scripting

def create_app(config_class=Config):
    """Defines the "app factory" that's run in totlahtol.py to create the app instance. 
       Adds extensions e.g. loads configuration, initializes database, loads flask_migrate, mail, cors policy, and the api blueprint.
       Two thirds of this function is mail and loggin code that isn't even used, so just ignore it.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins":"http://localhost:3000/*"}})

    # app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    ########################################################
    ### Everything below is unused mail and logging code ###
    ########################################################
    # if not app.debug and not app.testing:
    #     if app.config['MAIL_SERVER']:
    #         auth = None
    #         if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #             auth = (app.config['MAIL_USERNAME'],
    #                     app.config['MAIL_PASSWORD'])
    #         secure = None
    #         if app.config['MAIL_USE_TLS']:
    #             secure = ()
    #         mail_handler = SMTPHandler(
    #             mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #             fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #             toaddrs=app.config['ADMINS'], subject='Totlahtol Failure',
    #             credentials=auth, secure=secure)
    #         mail_handler.setLevel(logging.ERROR)
    #         app.logger.addHandler(mail_handler)

    #     if not os.path.exists('logs'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/totlahtol.log',
    #                                     maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s '
    #         '[in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)

    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Totlahtol startup')

    return app

from app import models #This is at the bottom to prevent a circular dependency. It might seems hacky, but it's standard practice in these situations
