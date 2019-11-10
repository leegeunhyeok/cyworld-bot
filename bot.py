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

from src.util import EC_or
from src.logger import Logger
from src.parser import Parser
from src.downloader import Downloader


# 유저 계정 정보 로드
config = configparser.ConfigParser()
config.read('config.ini')

class CyBot:
    def __init__(self, chromedriver, wait=5, delay=3, \
        headless=False, onlog=None, onerror=exit, done=exit):
        self._logger = Logger('./logs/cybot.log', callback=onlog)

        self._chromedriver = chromedriver
        self._base_url = 'https://cy.cyworld.com'
        self._user_id = ''
        self._wait_time = wait
        self._delay = delay
        self._headless = headless
        self._onlog = onlog
        self._onerror = onerror
        self._done = done
        self._options = None
        self._driver = None
        self._wait = None


    def init(self):
        self._logger.info('크롬 드라이버 로딩 중..')
        try:
            options = None
            if self._headless:
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('window-size=1920x1080')
                options.add_argument("disable-gpu")
                options.add_argument('log-level=3')
                driver = webdriver.Chrome(chromedriver, chrome_options=options)
            else:
                driver = webdriver.Chrome(chromedriver)
            driver.implicitly_wait(self._wait_time)
        except Exception as e:
            self._logger.error('크롬 드라이버 로딩 실패')
            self._onerror()
            return

        self._options = options
        self._chromedriver = driver
        self._wait = WebDriverWait(driver, self._wait_time)
        self._logger.info('크롬 드라이버 로딩 완료')

        # 싸이월드 페이지 열기
        self._logger.info('싸이월드 홈페이지 접속 중..')
        self._driver.get('https://cyworld.com')
        self._logger.success('싸이월드 홈페이지 접속 완료')
        return self


    def login(self, user_email, user_password):
        self._logger.info('로그인 시도 중..')

        prev_url = self._driver.current_url
        self._driver.find_element_by_name('email').send_keys(user_email)
        self._driver.find_element_by_name('passwd').send_keys(user_password, Keys.RETURN)

        try:
            self._wait.until(EC_or(
                EC.url_changes(prev_url),
                EC.invisibility_of_element( \
                    (By.CSS_SELECTOR, '.ui-dialog.ui-widget.ui-widget-content.ui-corner-all.ui-front.ui-draggable.ui-resizable'))
            ))
        except:
            self._logger.error('시간이 초과되었습니다')
            self._onerror()
            return None

        url = self._driver.current_url
        if 'timeline' in url:
            self._logger.success('로그인 성공')
            return self
        else:
            self._logger.error('사용자 정보를 확인해주세요')
            self._onerror()
            return None


    def home(self):
        self._logger.info('마이 홈으로 이동 중..')

        prev_url = self._driver.current_url

        # 유저 고유번호 추출
        profile = self._driver.find_element_by_css_selector('a.freak1')
        self._user_id = profile.get_attribute('href').split('/').pop()

        # 프로필 사진 영역 클릭
        self._driver.find_element_by_id('imggnbuser').click()

        try:
            self._wait.until(EC.url_changes(prev_url))
        except:
            self._logger.error('시간이 초과되었습니다')
            self._onerror()
            return None

        if 'home' not in self._driver.current_url:
            self._logger.error('마이 홈으로 이동할 수 없습니다')
            self._onerror()
            return None

        self._logger.success('이동 완료')
        return self


    def feeder(self, content_list, running):
        content_index = 0

        # 모든 타임라인 컨텐츠 영역 추출
        while self._driver.find_element_by_css_selector('p.btn_list_more'):
            contents = self._driver \
                .find_elements_by_css_selector(
                    'input[name="contentID[]"]'
                )[content_index:]

            for content in contents:
                cid = content.get_attribute('value')
                content_url = '{}/home/{}/post/{}/layer' \
                    .format(self._base_url, self._user_id, cid)
                self._logger.info('Feeder::', content_url)
                content_list.append(content_url)
                content_index += 1

            # 더 보기 버튼 대기
            try:
                next_button = self._wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'p.btn_list_more'))
                )
                time.sleep(self._delay)
            except:
                pass

            # 더 보기 버튼을 클릭할 수 없는 경우 (마지막 페이지인 경우) 반복 종료
            if not (next_button.is_displayed() and next_button.is_enabled()):
                running.value = 0
                break
            
            # 다음버튼 클릭
            next_button.click()

        running.value = 0
        self._driver.close()
        self._logger.info('Feeder:: 종료')


    def run(self, parser=2, downloader=2):
        self._logger.info('이미지 다운로드 작업 시작')
        start = time.time()

        # 멀티 프로세싱 처리를 위한 매니저
        with Manager() as manager:
            # 프로세스 목록
            processes = []

            # 공유 메모리 변수
            content_list = manager.list()
            image_list = manager.list()
            count = manager.Value('i', 0)
            lock = manager.Lock()
            feeder_running = manager.Value('i', 1)
            parser_running = manager.Value('i', 1)

            parser_logger = Logger('./logs/cybot_parser.log')
            downloader_logger = Logger('./logs/cybot_downloader.log', \
                callback=self._onlog)
            main_cookies = self._driver.get_cookies()
            cookie = []

            for c in main_cookies:
                cookie.append({ 'name': c['name'], 'value': c['value'] })

            # 파서 프로세스 생성 및 시작
            for idx in range(parser):
                parser_instance = Parser(
                    self._chromedriver,
                    cookie,
                    parser_logger,
                    self._wait_time,
                    self._delay,
                    self._headless
                )
                parser_process = Process(
                    target=parser_instance.parse, \
                    args=(
                        content_list,
                        image_list,
                        feeder_running,
                        parser_running
                    )
                )
                parser_process.name = 'Parser::' + str(idx)
                parser_process.start()
                processes.append(parser_process)
                self._logger.info('Parser', str(idx), '프로세스 시작')

            # 다운로더 프로세스 생성 및 시작
            for idx in range(downloader):
                downloader_instance = Downloader(downloader_logger)
                downloader_process = Process(
                    target=downloader_instance.download, \
                    args=(image_list, count, lock, parser_running))
                downloader_process.name = 'Downloader::' + str(idx)
                downloader_process.start()
                processes.append(downloader_process)
                self._logger.info('Downloader', str(idx), '프로세스 시작')

            # 피더 프로세스 시작
            self._logger.info('Feeder 시작')
            self.feeder(content_list, feeder_running)

            # 파서, 다운로더 프로세스가 종료되지않은 경우 대기
            for p in processes:
                p.join()

        self._logger.info('작업 소요시간: {}초' \
            .format(round(time.time() - start, 2)))
        self._logger.info('전체 이미지 수: {}'.format(count.value))
        self._done()


if __name__ == '__main__':
    user_email = config.get('user', 'email')
    user_password = config.get('user', 'password')

    if not (user_email and user_password):
        raise ValueError('계정 정보가 필요합니다.')

    chromedriver = config.get('bot', 'chromedriver')
    wait = int(config.get('bot', 'wait'))
    delay = int(config.get('bot', 'delay'))
    parser = int(config.get('bot', 'parser'))
    downloader = int(config.get('bot', 'downloader'))

    bot = CyBot(chromedriver, wait=wait, delay=delay)
    bot.init() \
        .login(user_email, user_password) \
        .home() \
        .run(parser=parser, downloader=downloader)
