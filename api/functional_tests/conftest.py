import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Lesson, Tlahtolli, Review
from config import Config
from selenium.webdriver import Firefox
import time
import datetime as dt
import multiprocessing as mp

basedir = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture(scope="session", autouse=True)
def app():

    _ , db_path = tempfile.mkstemp(suffix='_totlahtol.db')
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///'+db_path

    _app = create_app(config_class=TestConfig)

    def runserver(app):
        app.run(use_reloader=False)

    with _app.app_context():
        db.create_all()
    p=mp.Process(target=(runserver), args=(_app,))
    p.start()

    yield _app

    p.kill()
    db.session.remove()
    os.unlink(db_path)
