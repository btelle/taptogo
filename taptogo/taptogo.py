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
        
        self.logged_in = True

        # Check for error message on failed login
        try:
            error_div = self.driver.find_element_by_css_selector('div.page-messages')
            if 'your login attempt has failed' in error_div.text.lower():
                self.logged_in = False
                return False
            else:
                return True
        except NoSuchElementException:
            return True
    
    def describe_tap_cards(self):
        if not self.logged_in:
            raise Exception('You must log in before describing cards')
        
        # This page is at /TAPMyCards, but for some reason it 
        # doesn't load correctly unless you click the link.
        self.driver.get(self.base_url)
        with wait_for_page_load(self.driver):
            self.driver.find_element_by_link_text('My TAP cards').click()

        cards_wrapper = self.driver.find_element_by_id('MyCards:tapwrapper:cardList').get_attribute('innerHTML')
        soup = BeautifulSoup(cards_wrapper, "html.parser")
        cards = []

        for div in soup.findAll('div'):
            if 'panel-card' in div.get('class', ''):
                card = {}
                for div in div.findAll('div'):
                    if 'panel-heading' in div.get('class', ''):
                        for h2 in div.findAll('h2'):
                            card['name'] = h2.text.split('-')[0].strip()
                    elif 'panel-collapse' in div.get('class', ''):
                        if 'card-' in div['id'] and '-panel' in div['id']:
                            card['id'] = div['id'].replace('card-', '').replace('-panel', '')
                            card['balance'] = float(div.findAll('div')[0].findAll('h4')[0].findAll('span')[0].text.replace('$', ''))

                            for link in div.findAll('a'):
                                link_text = link.text.lower().strip()
                                if link_text == 'add fare':
                                    card['reload_url'] = self.base_url + link['href']
                                elif link_text == 'view history':
                                    card['history_url'] = self.base_url + link['href']
                                elif link_text == 'report lost or stolen card':
                                    card['cancel_url'] = self.base_url + link['href']
                            
                            cards.append(card)
        self.cards = cards
        return cards

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