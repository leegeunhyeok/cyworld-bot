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
from multiprocessing import Process, Manager, current_process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.logger import Logger
from src.parser import Parser
from src.downloader import Downloader


# 유저 계정 정보 로드
config = configparser.ConfigParser()
config.read('config.ini')
user_email = config.get('user', 'email')
user_password = config.get('user', 'password')

delay = config.get('bot', 'delay')
parser = config.get('bot', 'parser')
downloader = config.get('bot', 'downloader')

class CyBot:
    def __init__(self):
        self._logger = Logger('test.txt')

        ext = ''
        if config.get('bot', 'chromedriver') == 'exe':
            ext = '.exe'

        self._logger.info('크롬 드라이버 로딩 중..')
        driver = webdriver.Chrome('./driver/chromedriver' + ext)
        driver.implicitly_wait(5)
        self._logger.info('크롬 드라이버 로딩 완료')
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)


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


    def feeder(self, content_list, running):
        while self._driver.find_element_by_css_selector('p.btn_list_more'):
            contents = self._driver \
                .find_elements_by_css_selector('input[name="contentID[]"]')
            # print(contents)

            next_button = self._wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'p.btn_list_more'))
            )
            time.sleep(1)

            if not (next_button.is_displayed() and next_button.is_enabled()):
                break

            next_button.click()


    def run(self, parser=2, downloader=2):
        with Manager() as manager:
            processes = []
            content_list = manager.list()
            image_list = manager.list()
            running = manager.Value('i', 1)

            parser_instance = Parser()
            downloader_instance = Downloader()

            for idx in range(parser):
                parser_process = Process(target=parser_instance.parser, \
                    args=(content_list, image_list))
                parser_process.name = 'Parser::' + str(idx)
                parser_process.start()
                processes.append(parser_process)
                self._logger.info('Parser', str(idx), '프로세스 시작')

            for idx in range(downloader):
                downloader_process = Process(target=downloader_instance.downloader, \
                    args=(image_list,))
                downloader_process.name = 'Downloader::' + str(idx)
                downloader_process.start()
                processes.append(downloader_process)
                self._logger.info('Downloader', str(idx), '프로세스 시작')

            self._logger.info('Feeder 프로세스 시작')
            self.feeder(content_list, running)

            for p in processes:
                p.join()


if __name__ == '__main__':

    if not (user_email and user_password):
        raise ValueError('계정 정보가 필요합니다.')

    bot = CyBot()
    bot.init() \
        .login(user_email, user_password) \
        .home() \
        .run(parser=parser, downloader=downloader)
