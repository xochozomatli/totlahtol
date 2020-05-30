import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess' # Should change these....
    ### To connect to a postgresql database, create a db called "totlahtol".
    ### Next create a .env file in this diretory with the line:
    ### DATABASE_URL="postgresql+psycopg2://yourdatabaseusername:yourdatabasepassword@localhost:5432/totlahtol"
    ### Finally, run flask db init, and you're all set.
    ### If you choose not to connect to postgres or mysql, flask creates a sqlite database in this directory.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['aavillaverde11@gmail.com']
    # POSTS_PER_PAGE = 3
    # LANGUAGES = ['en', 'es']
    # MS_TRANSLATOR_KEY=os.environ.get('MS_TRANSLATOR_KEY')