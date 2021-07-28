import pytest
from selenium.webdriver.support.ui import WebDriverWait
from .conftest import set_user, unset_user

##################################
######### Meta Test ##############
##################################
def test_fixtures(get_driver, get_user):
    assert set_user
    xoch = get_user(username='xoch')
    driver = get_driver()
    set_user(driver, xoch)
    driver.get('dev.localhost:3000')
    assert driver.current_url != 'http://dev.localhost:3000/login'
    WebDriverWait(driver, timeout=9).until(
            lambda d: d.find_element_by_id('lessons').get_attribute('innerHTML') == ''
        )
    unset_user(driver)

def test_second_user(get_driver, get_user):
    xoch = get_user(username='xoch')
    driver = get_driver()
    set_user(driver, xoch)
    driver.get('dev.localhost:3000')
    driver.quit()

    susan = get_user(username='susan')
    driver = get_driver()
    set_user(driver, susan)
    driver.get('dev.localhost:3000')
    unset_user(driver)
