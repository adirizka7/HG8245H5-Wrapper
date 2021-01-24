from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import requests
import time
import os
import json
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

users = open('static/users.json', 'r').read()
users = json.loads(users)

class Huawei:
    def __init__(self):
        self.URL = 'http://192.168.100.1'

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(),
            options=options
        )
        self.driver.get(self.URL)
        self.clickable_mapping = {
            'Advanced': 'name_addconfig',
            'Security': 'name_securityconfig',
            'Parental Control': 'parentalctrl',
            'New': 'Newbutton',
            'Specified Device': 'ChildrenList',
            'Apply': 'ButtonApply'
        }
        self.frame_mapping = {
            'Content': 'menuIframe',
            'Overview': 'pccframeContent'
        }
        self.form_mapping = {
            'MAC Address': 'macAddr',
            'Device Description': 'ChildrenInfo'
        }
        self.option_mapping = {
            'Specified Device': 'ChildrenList',
            'Template': 'TemplateList'
        }
        self.base_xpath_id = '//*[@id="{}"]'

    def login(self, username, password):
        username_form = self.driver.find_element_by_xpath('//*[@id="txt_Username"]')
        username_form.send_keys(username)
        password_form = self.driver.find_element_by_xpath('//*[@id="txt_Password"]')
        password_form.send_keys(password)
        submit = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        submit.click()

    def click(self, clickable):
        xpath = self.clickable_mapping.get(clickable, clickable)

        xpath_selector = self.base_xpath_id.format(xpath)
        self.driver.find_element_by_xpath(xpath_selector).click()

    def switch_to_frame(self, frame):
        xpath = self.frame_mapping.get(frame, frame)
        xpath_selector = self.base_xpath_id.format(xpath)
        self.driver.switch_to.frame(
            self.driver.find_element_by_xpath(xpath_selector)
        )
        time.sleep(5)

    def fill_form(self, form_xpath, text):
        xpath = self.form_mapping.get(form_xpath, form_xpath)
        xpath_selector = self.base_xpath_id.format(xpath)
        form = self.driver.find_element_by_xpath(xpath_selector)
        form.send_keys(text)

    def select_text_option(self, option_xpath, chosen_text):
        xpath = self.option_mapping.get(option_xpath, option_xpath)
        xpath_selector = self.base_xpath_id.format(xpath)
        option = Select(self.driver.find_element_by_xpath(xpath_selector))
        option.select_by_visible_text(chosen_text)

    def delete_parental_control_devices(self):
        """
        get page source
        find all PCtrMacConfigList_record_[0-9]+ id
        matches all with mac addresses in users.json
        delete all matching mac addresses
        """
        pass


if __name__ == '__main__':
    username = os.environ.get('Huawei_Wifi_Username', '')
    password = os.environ.get('Huawei_Wifi_Password', '')

    huawei = Huawei()
    huawei.login(username, password)

    for command in ['Advanced', 'Security', 'Parental Control']:
        huawei.click(command)

    for frame in ['Content', 'Overview']:
        huawei.switch_to_frame(frame)

    for device_description, mac_address in users.items():
        huawei.click('New')
        huawei.select_text_option('Specified Device', 'Manually input MAC address')
        huawei.fill_form('MAC Address', mac_address)
        huawei.fill_form('Device Description', device_description)
        huawei.select_text_option('Template', 'No Access')
        huawei.click('Apply')

        try:
            WebDriverWait(huawei.driver, 0.5).until(EC.alert_is_present())
            alert = huawei.driver.switch_to.alert
            logger.info(f'[{alert.text}] {device_description} > {mac_address}')
            alert.accept()
        except TimeoutException:
            logger.info(f'[Success] {device_description} > {mac_address}')

    huawei.driver.quit()
