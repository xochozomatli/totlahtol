import os
import tempfile
import pytest
from app import create_app, db
from app.models import User, Lesson, Tlahtolli, Review
from config import Config
from selenium.webdriver import Firefox
from selenium.common.exceptions import WebDriverException
import time
import datetime as dt
import multiprocessing as mp
import json

basedir = os.path.abspath(os.path.dirname(__file__))
root_url = 'http://dev.localhost:3000' 

@pytest.fixture(scope="module", autouse=True)
def app():
    """
    Maybe I can make this more atomic?
    """
    _ , db_path = tempfile.mkstemp(suffix='_totlahtol.db')
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///'+db_path

    _app = create_app(config_class=TestConfig)

    def runserver(app):
        app.run(host='dev.localhost', use_reloader=False)

    with _app.app_context():
        db.create_all()
    p=mp.Process(target=(runserver), args=(_app,))
    p.start()

    yield _app

    p.kill()
    db.session.remove()
    os.unlink(db_path)

@pytest.fixture(scope='function')
def get_driver():
    drivers = []
    def gen():
        d = Firefox()
        nonlocal drivers
        drivers.append(d)
        d.get(root_url)
        return d
    yield gen
    for _driver in drivers:
        _driver.quit()

@pytest.fixture(scope='function')
def get_user():
    users = []
    def gen(**data):
        user = User()
        user.from_dict(data)
        user.get_token()
        db.session.add(user)
        db.session.commit()
        nonlocal users
        users.append(user)
        return user
    yield gen
    for u in users:
        try:
            db.session.delete(u)
            db.session.commit()
        except:
            pass

def set_user(driver, user):
    print(user.to_dict())
    user_json = json.dumps(user.to_dict(include_email=True))
    driver.get(root_url) # Should probably make this a check instead
    localstorage_script = f'localStorage.setItem("totlahtoluser", \'{user_json}\')'
    print(localstorage_script)
    cookie_script = f'document.cookie="refresh_token={user.refresh_token}"'
    driver.execute_script(localstorage_script)
    driver.execute_script(cookie_script)

def unset_user(driver):
    driver.execute_script('''
            window.localStorage.clear();
            window.document.cookie="refresh_token=; max-age=0";
        ''')

@pytest.fixture(scope='function')
def get_lesson():
    lessons = []
    def gen(**data):
        lesson = Lesson()
        lesson.from_dict(data)
        db.session.add(lesson)
        db.session.commit()
        nonlocal lessons
        lessons.append(lesson)
        return lesson
    yield gen
    for l in lessons:
        try:
            db.session.delete(l)
            db.session.commit()
        except:
            pass
