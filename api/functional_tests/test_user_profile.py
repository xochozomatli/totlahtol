import pytest
from .conftest import root_url, set_user, unset_user
from app import db
from app.models import User
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

def test_profile(get_driver, get_user):
    # Xoch goes to main feed and decides to check his profile.
    xoch = get_user(username='xoch', email='xoch@example.com')
    driver = get_driver()
    set_user(driver, xoch)
    driver.get(root_url)
    # He opens the dropdown menu in the navbar and clicks 'Profile'
    menu_toggle = WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element_by_id('menu-toggle')
        )
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    profile = [item for item in menu_items if "Profile" in item.text][0]
    profile.click()
    
    # He checks that his information is correct and that all's as it ought to be.
    profile_title = driver.find_element_by_id('modal-title')
    assert profile_title.text=='xoch'
    profile_username = driver.find_element_by_id('profile-username')
    assert profile_username.find_element_by_tag_name('input').get_attribute('value')=='xoch'
    profile_email = driver.find_element_by_id('profile-email')
    assert profile_email.find_element_by_tag_name('input').get_attribute('value')=='xoch@example.com'
    unset_user(driver)


def test_edit(get_driver, get_user):
    # Xoch goes to his profile
    xoch = get_user(username='xoch', email='xoch@example.com')
    _ = get_user(username='susan', email='susan@example.com')
    driver = get_driver()
    set_user(driver, xoch)
    driver.get(root_url+'/users/xoch')
    profile_save = WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element_by_id('profile-save')
        )
    # He tries to change his username to another user's and receives and error
    profile_username = driver.find_element_by_id('profile-username')
    profile_username.find_element_by_tag_name('input').clear()
    profile_username.find_element_by_tag_name('input').send_keys('susan')
    profile_save.click()
    assert 'There was a problem updating your profile:' \
            in driver.find_elements_by_class_name('error')[0].text
    assert profile_username.find_element_by_tag_name('input').get_attribute('value')=='xoch'

    # So he changes his username to something that's not taken instead
    profile_username.find_element_by_tag_name('input').clear()
    profile_username.find_element_by_tag_name('input').send_keys('scott')
    profile_save.click()
    assert len(driver.find_elements_by_class_name('error'))==0
    assert 'Profile Updated!' \
            in driver.find_elements_by_class_name('success')[0].text

    assert profile_username.find_element_by_tag_name('input').get_attribute('value')=='scott'

    # He does the same with his email and receives a similar error
    profile_email = driver.find_element_by_id('profile-email')
    profile_email.find_element_by_tag_name('input').clear()
    profile_email.find_element_by_tag_name('input').send_keys('susan@example.com')
    profile_save.click()
    assert len(driver.find_elements_by_class_name('success'))==0
    assert 'There was a problem updating your profile:' \
            in driver.find_elements_by_class_name('error')[0].text
    assert profile_email.find_element_by_tag_name('input').get_attribute('value')=='xoch@example.com'

    # So he changes his email to something that's not taken instead
    profile_email.find_element_by_tag_name('input').clear()
    profile_email.find_element_by_tag_name('input').send_keys('scott@example.com')
    profile_save.click()
    assert len(driver.find_elements_by_class_name('error'))==0
    assert 'Profile Updated!' \
            in driver.find_elements_by_class_name('success')[0].text
    assert profile_email.find_element_by_tag_name('input').get_attribute('value')=='scott@example.com'
    unset_user(driver)


def test_delete(get_driver, get_user):
    # Xoch goes to his profile and clicks the "Delete Account" button
    xoch = get_user(username='xoch', email='xoch@example.com')
    driver = get_driver()
    set_user(driver, xoch)
    driver.get(root_url+'/users/xoch')
    delete_button = WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element_by_id('profile-delete-button')
        )
    assert delete_button.text=="Delete Account"
    delete_button.click()
    # He notices that the text changes to "Are you sure?"
    assert delete_button.text=="Are You Sure?"
    # He is sure, so he clicks again and is redirected to the sign in and registration page
    delete_button.click()
    time.sleep(1)
    assert driver.current_url == root_url+"/login"

    # He tries to sign in with his old username and password and receives and error.
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.send_keys('xoch')
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    WebDriverWait(driver, timeout=5).until(lambda d: len(d.find_elements_by_class_name('error')) > 0)
    assert 'The username or password provided were incorrect!' \
            in driver.find_elements_by_class_name('error')[0].text
    # Finally, he registers a new account using his old username and email.
    email = driver.find_element_by_id('register-email')
    username = driver.find_element_by_id('register-username')
    password = driver.find_element_by_id('register-password')
    email.send_keys('xoch@example.com')
    username.send_keys('xoch')
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    WebDriverWait(driver, timeout=5).until(lambda d: len(d.find_elements_by_class_name('success')) > 0)
    assert 'Thanks for signing up!' in driver.find_elements_by_class_name('success')[0].text
    try:
        db.session.delete(
                User.query.filter_by(username='xoch').first()
            )
        db.session.commit()
    except:
        pass

def test_other_user_profile(get_driver, get_user):
    # Xoch goes to the url of susan's profile page
    # He sees that it ocontains susan's info, but that it's not editable
    pass
