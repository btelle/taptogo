import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from bs4 import BeautifulSoup

class TapToGo(object):
    base_url = 'https://www.taptogo.net/'

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get(self.base_url)

    def login(self, email, password):
        self.driver.find_element_by_id('j_id0:tapwrapper:loginform:login-email').send_keys(email)
        self.driver.find_element_by_id('j_id0:tapwrapper:loginform:login-password').send_keys(password)
        
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_id('j_id0:tapwrapper:loginform:login-submit').click()
        
        # Check for error message on failed login
        try:
            error_div = self.driver.find_element_by_css_selector('div.page-messages')
            if 'your login attempt has failed' in error_div.text.lower():
                return False
            else:
                return True
        except NoSuchElementException:
            return True

# http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
class wait_for_page_load(object):
    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)
    
    def wait_for(self, condition_function):
        start_time = time.time()
        while time.time() < start_time + 3:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )