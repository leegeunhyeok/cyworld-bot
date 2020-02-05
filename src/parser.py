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

from src.util import extract_date, to_valid_filename, update_size, clean_text

class Parser:
    # 오류 발생 시 재시도할 횟수
    __ATTEMPT__ = 3

    def __init__(self, chromedriver, cookie, logger, wait, delay, \
        headless, options):
        self._chromedriver = chromedriver
        self._cookie = cookie
        self._logger = logger
        self._wait = wait
        self._delay = delay
        self._headless = headless
        self._options = options


    def parse(self, content_list, image_list, feeder_running, parser_running):
        name = current_process().name
        self._logger.info(name, '크롬 드라이버 로딩 중..')

        parser_driver = webdriver.Chrome(
            self._chromedriver, 
            chrome_options=self._options
        )

        parser_driver.implicitly_wait(self._wait)
        parser_driver.get('https://cyworld.com')
        for cookie in self._cookie:
            parser_driver.add_cookie(cookie)

        self._logger.info(name, '크롬 드라이버 로딩 완료')

        while feeder_running.value or len(content_list) != 0:
            try:
                # 공유 리스트에서 게시물 URL 추출 및 접속
                target_url = content_list.pop(0)
            except IndexError:
                time.sleep(1)
                continue
            except Exception as e:
                self._logger.error(str(e))
                time.sleep(1)
                continue

            attempt = 0
            while attempt < Parser.__ATTEMPT__:
                attempt += 1

                try:
                    # 공유 리스트에서 게시물 URL 추출 및 접속
                    self._logger.info(name, target_url)
                    parser_driver.get(target_url)

                    # 필요한 데이터 추출
                    date = parser_driver \
                        .find_element_by_css_selector('div.view1 p')
                    images = parser_driver \
                        .find_elements_by_css_selector('section.imageBox')
                    texts = parser_driver \
                        .find_elements_by_css_selector('section.textBox')

                    # 원본 제목
                    title = parser_driver \
                        .find_element_by_id('cyco-post-title') \
                        .get_attribute('innerText')

                    # 파일 저장을 위해 전처리한 제목 (파일명으로 사용됨)
                    preprocessed_title = to_valid_filename(title)

                    # 게시글 날짜 업로드 날짜
                    post_date = extract_date(date.get_attribute('innerText'))

                    # 게시글 데이터 병합
                    post_text = '[ {} ]\n\n'.format(title)
                    for text in texts:
                        current_text = text.get_attribute('innerText') \
                            .strip()

                        if len(current_text):
                            post_text += clean_text(current_text) + '\n'

                    # 이미지 목록 추출
                    for image in images:
                        imgs = image.find_elements_by_tag_name('img')

                        for img in imgs:
                            src = update_size(img.get_attribute('src'))

                            image_list.append({
                                'title': preprocessed_title,
                                'date': post_date,
                                'content': post_text,
                                'src': src
                            })

                            self._logger.info(
                                name, '{}_{} 포스트 파싱 됨'.format(
                                    post_date, title)
                            )

                    # 싸이월드 서버 부하 방지를 위해 잠시 대기
                    time.sleep(1)
                    break
                except Exception as e:
                    time.sleep(3)
                    self._logger.error(str(e) + ' - Attempt({}/{})' \
                        .format(attempt, Parser.__ATTEMPT__))

        parser_running.value = 0
        parser_driver.close()
        self._logger.info(name, '종료')
