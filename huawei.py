from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time
import os

class Huawei:
    def __init__(self):
        self.URL = 'http://192.168.100.1'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.URL)
        self.clickable_mapping = {
            'Advanced': 'name_addconfig',
            'Security': 'name_securityconfig',
            'Parental Control': 'parentalctrl',
            'New': 'Newbutton',
            'Specified Device': 'ChildrenList'
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


if __name__ == '__main__':

    username = os.environ.get('Huawei_Wifi_Username', '')
    password = os.environ.get('Huawei_Wifi_Password', '')

    huawei = Huawei()
    huawei.login(username, password)

    for command in ['Advanced', 'Security', 'Parental Control']:
        huawei.click(command)

    for frame in ['Content', 'Overview']:
        huawei.switch_to_frame(frame)

    huawei.click('New')

    huawei.select_text_option('Specified Device', 'Manually input MAC address')

    huawei.fill_form('MAC Address', 'adirizka7')
    huawei.fill_form('Device Description', 'adirizka8')

    huawei.select_text_option('Template', 'No Access')
