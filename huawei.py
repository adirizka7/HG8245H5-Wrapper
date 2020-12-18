from selenium import webdriver
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
            'Advanced': ('', 'name_addconfig'),
            'Security': ('', 'name_securityconfig'),
            'Parental Control': ('', 'parentalctrl'),
            'Content': ('frame', 'menuIframe'),
            'Overview': ('frame', 'pccframeContent'),
            'New': ('', 'Newbutton')
        }
        self.base_xpath_id = '//*[@id="{}"]'

    def login(self, username, password):
        username_form = self.driver.find_element_by_xpath('//*[@id="txt_Username"]')
        username_form.send_keys(username)
        password_form = self.driver.find_element_by_xpath('//*[@id="txt_Password"]')
        password_form.send_keys(password)
        submit = self.driver.find_element_by_xpath('//*[@id="loginbutton"]')
        submit.click()

    def go_to(self, clickable):

        default_xpath = lambda x: ('', x)
        xpath = self.clickable_mapping.get(clickable, default_xpath(clickable))

        if len(xpath) != 2:
            print('xpath length should be 2')
            return

        if xpath[0] == 'frame':
            xpath_selector = self.base_xpath_id.format(xpath[1])
            self.driver.switch_to.frame(
                self.driver.find_element_by_xpath(xpath_selector)
            )
            time.sleep(5)
            return

        xpath_selector = self.base_xpath_id.format(xpath[1])
        self.driver.find_element_by_xpath(xpath_selector).click()

if __name__ == '__main__':

    username = os.environ.get('Huawei_Wifi_Username', '')
    password = os.environ.get('Huawei_Wifi_Password', '')

    huawei = Huawei()
    huawei.login(username, password)

    commands_sequence = [
        'Advanced', 'Security', 'Parental Control', 'Content', 'Overview', 'New'
    ]
    for command in commands_sequence:
        huawei.go_to(command)
