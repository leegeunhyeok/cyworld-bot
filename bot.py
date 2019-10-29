'''
MIT License

Copyright (c) 2019 GeunHyeok LEE

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 유저 계정 정보 로드
config = configparser.ConfigParser()
config.read('config.ini')
user_email = config.get('user', 'email')
user_password = config.get('user', 'password')

class CyBot:
    def __init__(self):
        ext = ''
        if config.get('bot', 'chromedriver') == 'exe':
            ext = '.exe'
        driver = webdriver.Chrome('./driver/chromedriver' + ext)
        driver.implicitly_wait(3)

        # 싸이월드 페이지 열기
        driver.get('https://cyworld.com')
        self._driver = driver

    def login(self, user_email, user_password):
        print('Login..')
        self._driver.find_element_by_name('email').send_keys(user_email)
        self._driver.find_element_by_name('passwd').send_keys(user_password, Keys.RETURN)
        print('a')

if __name__ == '__main__':

    if not (user_email and user_password):
        raise ValueError('계정 정보가 필요합니다.')

    bot = CyBot()
    bot.login(user_email, user_password)
