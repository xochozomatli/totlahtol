import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from .conftest import root_url, set_user, unset_user
from string import punctuation as punct
import re
import time

############################
####### Use Lessons ########
############################

def test_use_lesson(get_driver, get_user, get_lesson):
    # Xoch logs in, sees the feed, and clicks the first lesson
    # a modal pops up with a header containing the title
    # and below, the text.
    xoch = get_user(username='xoch')
    susan = get_user(username='susan')
    _ = get_lesson(
            title='susan lesson',
            content='lesson susan. susanny lesson.', 
            author_id=susan.id
        )
    _ = get_lesson(
            title='susan\'s second lesson',
            content='lesson susan second. second susanny lesson.', 
            author_id=susan.id
        )

    driver = get_driver()
    set_user(driver, xoch)
    driver.get(root_url)
    WebDriverWait(driver, timeout=10).until(
            ec.presence_of_element_located((By.ID, 'lesson1'))
        )
    lesson_link=driver.find_elements_by_partial_link_text('by susan')[0]
    lesson_title = re.split(' by susan', lesson_link.get_attribute('innerHTML'))[0]
    lesson_link.click()
    assert driver.find_element_by_id('modal-title').get_attribute('innerHTML')==lesson_title

    # Xoch sees the lesson content words are underlined green.
    # He hovers his cursor over the word and a green box appears underneath.
    # He clicks inside to add a definition and presses enter. The box turns red.
    # The same word in other positions is also underlined red and hovering reflects the change.

    tlahtolli = driver.find_elements_by_css_selector('div > span')[-3]
    assert tlahtolli.value_of_css_property('border-bottom-color')=='rgb(95, 163, 72)'
    
    hover = ActionChains(driver).move_to_element(tlahtolli)
    hover.perform()

    tlahtolli_input = tlahtolli.find_element_by_xpath('../form/input')
    assert tlahtolli_input.value_of_css_property('border-left-color')=='rgb(95, 163, 72)'
    tlahtolli_input.send_keys('test definition')
    tlahtolli_input.send_keys(Keys.ENTER)

    time.sleep(1) # Or else figure out how to detect the rerender
    tlahtolli = driver.find_elements_by_css_selector('div > span')[-3]
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
    time.sleep(1)
    tlahtolli = driver.find_elements_by_css_selector('div > span')[-3]
    assert tlahtolli.value_of_css_property('border-bottom-color')=='rgb(186, 66, 30)'#totlahtol red

    hover = ActionChains(driver).move_to_element(tlahtolli)
    hover.perform()
    tlahtolli_input = tlahtolli.find_element_by_xpath('../form/input')
    assert tlahtolli_input.get_attribute('value')=='test definition'
    # Satisfied, Xoch logs out and closes the browser.
    X = driver.find_element_by_id('modal-exit')
    X.click()
    unset_user(driver)
    driver.quit()

    # Susan opens a browser and logs in, clicking on her first lesson.
    # She finds that words are all underlined green and don't display
    # Xoch's new definition.
    driver = get_driver()
    set_user(driver, susan)
    driver.get(root_url)

    lesson_links = WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_elements_by_partial_link_text('by susan')
        )
    lesson_link = lesson_links[0]
    lesson_link.click()

    tlahtolli = driver.find_elements_by_css_selector('div > span')[-3]
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
    print(type(og_lesson_text), og_lesson_text)
    textarea.clear()
    edit_text = 'I never liked this lesson. I hope I don\'t regret this...'
    textarea.send_keys(edit_text)
    cancel_button = driver.find_element_by_id('edit-lesson-cancel')
    cancel_button.click()

    modal_content = driver.find_element_by_id('modal-content')
    tlahtolli_array = modal_content.find_elements_by_tag_name('span')
    text_array = [tlahtolli.text for tlahtolli in tlahtolli_array]
    print(text_array)
    punct_fixed_text_array = ''.join(text_array)
    assert punct_fixed_text_array==og_lesson_text

    edit_button = driver.find_element_by_id('edit-lesson-button')
    edit_button.click()
    textarea = driver.find_element_by_id('edit-lesson-textarea')
    assert textarea.get_attribute('value')==og_lesson_text

    # She works the nerve back up, redoes her edit, and clicks save.
    # She sees her edit reflected in the lesson content, but hates it.
    textarea.clear()
    textarea.send_keys(edit_text)
    save_button = driver.find_element_by_id('edit-lesson-save')
    save_button.click()

    modal_content = driver.find_element_by_id('modal-content')
    tlahtolli_array = modal_content.find_elements_by_tag_name('span')
    text_array = [tlahtolli.text for tlahtolli in tlahtolli_array]
    punct_fixed_text_array = ''.join(text_array)
    print('Reformatted Array: '+punct_fixed_text_array)
    assert punct_fixed_text_array==edit_text

    # Susan clicks 'Edit' again, but this time she clicks 'Delete' in the upper right corner.
    # The button asks her to confirm, which she does. The modal closes and the lesson disappears from her feed.
    edit_button = driver.find_element_by_id('edit-lesson-button')
    edit_button.click()
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
    assert re.search('lesson_link_text', feed.get_attribute('innerHTML')) == None

    unset_user(driver)
