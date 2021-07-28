import pytest
import time
from .conftest import set_user, unset_user
from app import db
from app.models import User
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

#######################################
######### Register and Login ##########
#######################################
def test_redirect_to_login(get_driver):
    driver = get_driver()
    driver.get('http://dev.localhost:3000')
    WebDriverWait(driver, timeout=5).until(lambda d: d.current_url == 'http://dev.localhost:3000/login')
     
def test_cant_login_unregistered(get_driver):
    driver = get_driver()
    driver.get('http://dev.localhost:3000')
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.send_keys('susan')
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    WebDriverWait(driver, timeout=5).until(lambda d: len(d.find_elements_by_class_name('error')) > 0)
    assert 'The username or password provided were incorrect!' \
            in driver.find_elements_by_class_name('error')[0].text
    assert driver.current_url == 'http://dev.localhost:3000/login'

def test_registration(get_driver):
    try:
        driver = get_driver()
        driver.get('http://dev.localhost:3000')
        email = driver.find_element_by_id('register-email')
        username = driver.find_element_by_id('register-username')
        password = driver.find_element_by_id('register-password')
        email.send_keys('xoch@example.com')
        username.send_keys('xoch')
        password.send_keys('dog')
        password.send_keys(Keys.ENTER)
        WebDriverWait(driver, timeout=5).until(lambda d: len(d.find_elements_by_class_name('success')) > 0)
        assert 'Thanks for signing up!' in driver.find_elements_by_class_name('success')[0].text
    finally:
        db.session.delete(
                User.query.filter_by(username='xoch').first()
            )
        db.session.commit()

def test_login(get_driver, get_user):
    driver = get_driver()
    user = get_user(username='xoch', email='xoch@example.com', password='dog')
    driver.get('http://dev.localhost:3000')
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.send_keys('xoch')
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    WebDriverWait(driver, timeout=5).until(
            lambda d: d.current_url == 'http://dev.localhost:3000/'
        )
    menu_toggle = driver.find_element_by_id('menu-toggle')
    assert menu_toggle.text.lower() == 'xoch'
    unset_user(driver)

def test_logout(get_driver, get_user):
    user = get_user(username='xoch')
    driver = get_driver()
    set_user(driver, user)
    driver.get('http://dev.localhost:3000')
    menu_toggle = WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element_by_id('menu-toggle')
        )
    assert driver.find_elements('id', 'menu') == []
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    assert len(menu_items)==2
    logout = [item for item in menu_items if "Log Out" in item.text][0] 
    logout.click()
    assert driver.current_url == 'http://dev.localhost:3000/login'
    unset_user(driver)

    #TODO:
    #  Make sure there's no funny business caused by cookies or
    #  localStorage with multiple users using the same browser
    #  (Pretty much accomplished by test_second_user)
