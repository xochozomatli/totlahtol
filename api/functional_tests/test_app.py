import pytest
from selenium.webdriver.common.keys import Keys
import time
import multiprocessing as mp

def test_redirect_to_login(app, driver):
    driver.get('localhost:3000')
    time.sleep(2)
    assert driver.current_url == 'http://localhost:3000/login'


def test_registration(app, driver):
    email = driver.find_element_by_id('register-email')
    username = driver.find_element_by_id('register-username')
    password = driver.find_element_by_id('register-password')
    email.clear()
    email.send_keys('xoch@example.com')
    username.clear()
    username.send_keys('xoch')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(2)
    assert  len(driver.find_elements_by_class_name('success')) > 0
    assert 'Thanks for signing up!' in driver.find_elements_by_class_name('success')[0].text 

    
def test_cant_login_unregistered(app, driver):
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('susan')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(2)
    assert  len(driver.find_elements_by_class_name('error')) > 0
    assert 'The username or password provided were incorrect!' in driver.find_elements_by_class_name('error')[0].text 
    

def test_login_out(driver):
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('xoch')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    assert driver.current_url == 'http://localhost:3000/'

    menu_toggle = driver.find_element_by_id('menu-toggle')
    assert menu_toggle.text.lower() == 'xoch'
    assert driver.find_elements('id', 'menu') == []
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    assert len(menu_items)==2
    logout = [item for item in menu_items if "Log Out" in item.text][0] 
    logout.click()
    assert driver.current_url == 'http://localhost:3000/login'
