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

import time
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from src.logger import Logger

# 유저 계정 정보 로드
config = configparser.ConfigParser()
config.read('config.ini')
user_email = config.get('user', 'email')
user_password = config.get('user', 'password')

feeder = config.get('bot', 'feeder')
downloader = config.get('bot', 'downloader')

class CyBot:
    def __init__(self):
        self._logger = Logger('test.txt')

        ext = ''
        if config.get('bot', 'chromedriver') == 'exe':
            ext = '.exe'

        self._logger.info('크롬 드라이버 로딩 중..')
        driver = webdriver.Chrome('./driver/chromedriver' + ext)
        driver.implicitly_wait(3)
        self._logger.info('크롬 드라이버 로딩 완료')
        self._driver = driver

    def init(self):
        self._logger.info('싸이월드 홈페이지 접속 중..')
        # 싸이월드 페이지 열기
        self._driver.get('https://cyworld.com')
        self._logger.success('싸이월드 홈페이지 접속 완료')
        return self

    def login(self, user_email, user_password):
        self._logger.info('로그인 시도 중..')
        self._driver.find_element_by_name('email').send_keys(user_email)
        self._driver.find_element_by_name('passwd').send_keys(user_password, Keys.RETURN)
        time.sleep(3)

        url = self._driver.current_url
        if 'cyMain' in url:
            self._logger.error('사용자 정보를 다시 확인해주세요')
            exit()
        # elif '비밀번호 변경 요청' in url:
        #     pass
        elif 'timeline' in url:
            self._logger.success('로그인 성공')
            return self

    def home(self):
        self._logger.info('마이 홈으로 이동 중..')
        self._driver.find_element_by_css_selector('a.freak1').click()

        if 'home' not in self._driver.current_url:
            self._logger.error('마이 홈으로 이동할 수 없습니다')
            exit()

        self._logger.success('이동 완료')
        return self

    def feeder(self, process=2):
        images = self._driver.find_elements_by_class_name('timeline_img')
        print(images)
        return self

    def downloader(self, process=2):
        pass

if __name__ == '__main__':

    if not (user_email and user_password):
        raise ValueError('계정 정보가 필요합니다.')

    bot = CyBot()
    bot.init() \
        .login(user_email, user_password) \
        .home() \
        .feeder(feeder) \
        .downloader(downloader)
