import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from .conftest import set_user, unset_user
import re

##########################
######### Feed  ##########
##########################
def share_lesson(driver, title, body):
    title_field = driver.find_element_by_id('new-lesson-title')
    text_area = driver.find_element_by_id('new-lesson-textarea')
    share_button = driver.find_element_by_id('new-lesson-share-button')
    title_field.send_keys(title)
    text_area.send_keys(body)
    share_button.click()

def test_lesson_feed(get_driver, get_user):
    # Xoch goes to homepage and sees a blank feed
    xoch = get_user(username='xoch')
    driver = get_driver()
    set_user(driver, xoch)
    driver.get('http://dev.localhost:3000')
    WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element_by_id('lessons').get_attribute('innerHTML') == ''
        )
    # Xoch adds some lessons which instantly appear in feed
    share_lesson(driver, "Hello", "World")
    feed = driver.find_element_by_id('lessons')
    WebDriverWait(driver, timeout=5).until(
            ec.presence_of_element_located((By.ID, 'lesson1'))
        )
    assert re.match('<div.+id="lesson1".+Hello by xoch</a></div>', feed.get_attribute('innerHTML'))
    share_lesson(driver, "Foo", "Bar!")
    share_lesson(driver, "Foofoo", "barbar!")
    WebDriverWait(driver, timeout=5).until(
            ec.presence_of_element_located((By.ID, 'lesson3'))
        )
    assert len(re.findall('id="lesson[1-9]".*?by xoch', feed.get_attribute('innerHTML')))==3
    # Xoch logs out; Susan logs in and is greeted by Xoch's posts
    driver.quit()

    susan = get_user(username='susan')
    driver = get_driver()
    set_user(driver, susan)
    driver.get('http://dev.localhost:3000')
    WebDriverWait(driver, timeout=5).until(
            ec.presence_of_element_located((By.ID, 'lessons'))
        )
    feed = driver.find_element_by_id('lessons')
    WebDriverWait(driver, timeout=5).until(
            lambda d: len(re.findall('id="lesson[1-9]".*?by xoch', feed.get_attribute('innerHTML')))==3
        )
    share_lesson(driver, "Susan's lesson", 'Susan susan lesson')
    share_lesson(driver, "Susan's second lesson", 'Susan second. Second susan lesson')
    WebDriverWait(driver, timeout=5).until(
            lambda d: len(re.findall('id="lesson[1-9]".*?by susan', feed.get_attribute('innerHTML')))==2
        )
    unset_user(driver)
