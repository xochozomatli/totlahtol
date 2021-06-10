import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Firefox
import time
import multiprocessing as mp
import re

#######################################
######### Register and Login ##########
#######################################
def test_redirect_to_login(app):
    driver = Firefox()
    driver.get('http://localhost:3000')
    time.sleep(2)
    assert driver.current_url == 'http://localhost:3000/login'
    driver.quit()


def test_registration(app):
    driver = Firefox()
    driver.get('http://localhost:3000')
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
    driver.quit()

    
def test_cant_login_unregistered(app):
    driver = Firefox()
    driver.get('http://localhost:3000')
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('susan')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    assert  len(driver.find_elements_by_class_name('error')) > 0
    assert 'The username or password provided were incorrect!' \
            in driver.find_elements_by_class_name('error')[0].text 
    driver.quit()

def test_login_out():
    driver = Firefox()
    driver.get('http://localhost:3000')
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

    driver.quit()


    
##########################
######### Feed  ##########
##########################
def test_lesson_feed():
    # Xoch logs in and sees a blank feed
    driver = Firefox()
    driver.get('localhost:3000')
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('xoch')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(3)
    feed = driver.find_element_by_id('lessons')
    assert feed.get_attribute('innerHTML') == ''
    # Xoch adds some lessons which instantly appear in feed
    title = driver.find_element_by_id('new-lesson-title')
    text_area = driver.find_element_by_id('new-lesson-textarea')
    share_button = driver.find_element_by_id('new-lesson-share-button')
    title.send_keys('Hello')
    text_area.send_keys('World!')
    share_button.click()
    time.sleep(1)
    assert re.match('<div.+id="lesson1".+Hello by xoch</a></div>', feed.get_attribute('innerHTML'))
    title.send_keys('Foo')
    text_area.send_keys('Bar!')
    share_button.click()
    title.send_keys('Foofoo')
    text_area.send_keys('barbar!')
    share_button.click()
    title.send_keys('foofoofoo')
    text_area.send_keys('barbarbar!')
    share_button.click()
    feed = driver.find_element_by_id('lessons')
    time.sleep(1)
    assert len(re.findall('id="lesson[1-9]".*?by xoch', feed.get_attribute('innerHTML')))==4

    # Xoch logs out; Susan logs in and is greeted by Xoch's posts
    menu_toggle = driver.find_element_by_id('menu-toggle')
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    logout = [item for item in menu_items if "Log Out" in item.text][0] 
    logout.click()
    driver.quit()

    driver = Firefox()
    driver.get('localhost:3000')
    email = driver.find_element_by_id('register-email')
    username = driver.find_element_by_id('register-username')
    password = driver.find_element_by_id('register-password')
    email.clear()
    email.send_keys('susan@example.com')
    username.clear()
    username.send_keys('susan')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(1)

    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('susan')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(3)

    title = driver.find_element_by_id('new-lesson-title')
    text_area = driver.find_element_by_id('new-lesson-textarea')
    share_button = driver.find_element_by_id('new-lesson-share-button')
    title.send_keys("Susan's lesson")
    text_area.send_keys('Susan susan lesson')
    share_button.click()
    title.send_keys("Susan's second lesson")
    text_area.send_keys('Susan second. Second susan lesson')
    share_button.click()
    time.sleep(1)

    feed = driver.find_element_by_id('lessons')
    assert len(re.findall('id="lesson[1-9]".*?by xoch', feed.get_attribute('innerHTML')))==4
    assert len(re.findall('id="lesson[1-9]".*?by susan', feed.get_attribute('innerHTML')))==2

    menu_toggle = driver.find_element_by_id('menu-toggle')
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    logout = [item for item in menu_items if "Log Out" in item.text][0] 
    logout.click()
    driver.quit()



############################
####### Use Lessons ########
############################

def test_use_lesson():
    # Xoch logs in, sees the feed, and clicks the first lesson
    # a modal pops up with a header containing the title
    # and below, the text.
    driver = Firefox()
    driver.get('localhost:3000')
    time.sleep(1)
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('xoch')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(5)

    lesson_link=driver.find_elements_by_partial_link_text('by susan')[0]
    lesson_title = re.split(' by susan', lesson_link.get_attribute('innerHTML'))[0]
    lesson_link.click()
    assert driver.find_element_by_id('modal-title').get_attribute('innerHTML')==lesson_title

    # Xoch sees the lesson content words are underlined green.
    # He hovers his cursor over the word and a green box appears underneath.
    # He clicks inside to add a definition and presses enter. The box turns red.
    # The same word in other positions is also underlined red and hovering reflects the change.
    tlahtolli = driver.find_elements_by_css_selector('div > span')[-1]
    assert tlahtolli.value_of_css_property('border-bottom-color')=='rgb(95, 163, 72)'#totlahtol green
    
    hover = ActionChains(driver).move_to_element(tlahtolli)
    hover.perform()

    tlahtolli_input = tlahtolli.find_element_by_xpath('../form/input')
    assert tlahtolli_input.value_of_css_property('border-left-color')=='rgb(95, 163, 72)'
    tlahtolli_input.send_keys('test definition')
    tlahtolli_input.send_keys(Keys.ENTER)

    time.sleep(.5)
    tlahtolli = driver.find_elements_by_css_selector('div > span')[-1]
    tlahtolli_input = tlahtolli.find_element_by_xpath('../form/input')

    assert tlahtolli.value_of_css_property('border-bottom-color')=='rgb(186, 66, 30)'#totlahtol red
    hover = ActionChains(driver).move_to_element(tlahtolli)
    hover.perform()
    assert tlahtolli_input.value_of_css_property('border-left-color')=='rgb(186, 66, 30)'

    # Xoch clicks the 'X' to close the current lesson and clicks another.
    # The same word as before in the new lesson is also underlined red
    # and hovering shows the new definition.
    X = driver.find_element_by_id('modal-exit')
    X.click()
    lesson_link=driver.find_elements_by_partial_link_text('by susan')[1]
    lesson_link.click()
    tlahtolli = driver.find_elements_by_css_selector('div > span')[-1]
    assert tlahtolli.value_of_css_property('border-bottom-color')=='rgb(186, 66, 30)'#totlahtol red

    hover = ActionChains(driver).move_to_element(tlahtolli)
    hover.perform()
    tlahtolli_input = tlahtolli.find_element_by_xpath('../form/input')
    assert tlahtolli_input.get_attribute('value')=='test definition'
    # Satisfied, Xoch logs out and closes the browser.
    X = driver.find_element_by_id('modal-exit')
    X.click()
    menu_toggle = driver.find_element_by_id('menu-toggle')
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    logout = [item for item in menu_items if "Log Out" in item.text][0] 
    logout.click()
    driver.quit()
    # Susan opens a browser and logs in, clicking on her first lesson.
    # She finds that words are all underlined green and don't display
    # Xoch's new definition.
    driver = Firefox()
    driver.get('localhost:3000')
    username = driver.find_element_by_id('login-username')
    password = driver.find_element_by_id('login-password')
    username.clear()
    username.send_keys('susan')
    password.clear()
    password.send_keys('dog')
    password.send_keys(Keys.ENTER)
    time.sleep(3)

    lesson_link=driver.find_elements_by_partial_link_text('by susan')[0]
    lesson_link_text = lesson_link.text
    lesson_link.click()

    tlahtolli = driver.find_elements_by_css_selector('div > span')[-1]
    assert tlahtolli.value_of_css_property('border-bottom-color')=='rgb(95, 163, 72)'#totlahtol green
    hover = ActionChains(driver).move_to_element(tlahtolli)
    hover.perform()
    tlahtolli_input = tlahtolli.find_element_by_xpath('../form/input')
    assert tlahtolli_input.value_of_css_property('border-left-color')=='rgb(95, 163, 72)'
    assert tlahtolli_input.get_attribute('value')==''

    # Susan looks in the header bar and notices an 'Edit' button
    # She clicks it and the lesson content area turns into an editable textarea
    # She takes the opportunity to tweak her lesson, but gets cold feet and clicks cancel
    edit_button = driver.find_element_by_id('edit-lesson-button')
    edit_button.click()
    textarea = driver.find_element_by_id('edit-lesson-textarea')
    og_lesson_text = textarea.get_attribute('value')
    textarea.clear()
    edit_text = 'I never liked this lesson. I hope I don\'t regret this...'
    textarea.send_keys(edit_text )
    cancel_button = driver.find_element_by_id('edit-lesson-cancel')
    cancel_button.click()

    modal_content = driver.find_element_by_id('modal-content')
    tlahtolli_array = modal_content.find_elements_by_tag_name('span')
    assert ' '.join([tlahtolli.text for tlahtolli in tlahtolli_array])==og_lesson_text

    edit_button = driver.find_element_by_id('edit-lesson-button')
    edit_button.click()
    textarea = driver.find_element_by_id('edit-lesson-textarea')
### TODO current sticking point: textarea remembers canceled edit ###
    assert textarea.get_attribute('value')==og_lesson_text

    # She works the nerve back up, redoes her edit, and clicks save.
    # She sees her edit reflected in the lesson content, but hates it.
    textarea.clear()
    textarea.send_keys(edit_text)
    save_button = driver.find_element_by_id('edit-lesson-save')
    save_button.click()
    assert ' '.join([tlahtolli.text for tlahtolli in tlahtolli_array])==edit_text

    # Susan clicks 'Edit' again, but this time she clicks 'Delete' in the upper right corner.
    # The button asks her to confirm, which she does. The modal closes and the lesson disappears from her feed.
    delete_button = driver.find_element_by_id('delete-lesson-button')
    assert delete_button.text=='Delete'
    delete_button.click()
    assert delete_button.text=='Are you sure?'
    delete_button.click()
    try:
        driver.find_element_by_id('lesson-modal')
    except:
        pass
    else:
        raise Exception('lesson-modal should be closed')
    feed = driver.find_element_by_id('lessons')
    assert re.search('lesson_link_text', feed.get_attribute('innerHTML'))\
            == None

    menu_toggle = driver.find_element_by_id('menu-toggle')
    menu_toggle.click()
    menu = driver.find_element_by_id('menu')
    menu_items = menu.find_elements_by_class_name("menu-item")
    logout = [item for item in menu_items if "Log Out" in item.text][0] 
    logout.click()
    driver.quit()



#################################
######### User Profile ##########
#################################





###############################
######### Equis Test ##########
###############################


###############################
######### Equis Test ##########
###############################
