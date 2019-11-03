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
from multiprocessing import current_process
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from src.util import extract_date, to_valid_filename

class Parser:
    def __init__(self, chromedriver, cookie, logger, delay):
        self._chromedriver = chromedriver
        self._cookie = cookie
        self._logger = logger
        self._delay = delay


    def parse(self, content_list, image_list, feeder_running, parser_running):
        self._logger.info(current_process().name, '크롬 드라이버 로딩 중..')
        parser_driver = webdriver.Chrome(self._chromedriver)
        parser_driver.implicitly_wait(5)
        parser_driver.get('https://cyworld.com')
        for cookie in self._cookie:
            parser_driver.add_cookie(cookie)

        self._logger.info(current_process().name, '크롬 드라이버 로딩 완료')

        while(feeder_running.value):
            try:
                if len(content_list) != 0:
                    # 공유 리스트에서 게시물 URL 추출 및 접속
                    target_url = content_list.pop()
                    self._logger.info(current_process().name, target_url)
                    parser_driver.get(target_url)

                    # 필요한 데이터 추출
                    date = parser_driver.find_element_by_css_selector('div.view1 p')
                    images = parser_driver.find_elements_by_css_selector('section.imageBox')
                    title = parser_driver.find_element_by_id('cyco-post-title')
                    post_date = extract_date(date.get_attribute('innerText'))

                    title = to_valid_filename(title.get_attribute('innerText'))

                    # 이미지 목록 추출
                    for image in images:
                        imgs = image.find_elements_by_tag_name('img')

                        for img in imgs:
                            image_list.append({
                                'title': title,
                                'date': post_date,
                                'src': img.get_attribute('src')
                            })
                            self._logger.info('{}_{} 포스트 파싱 됨'.format(post_date, title))
                else:
                    # 만약 리스트가 비어있는 경우 1초 대기 후 다시 시도
                    time.sleep(1)
            except Exception as e:
                self._logger.error(e)

        parser_running.value = 0
