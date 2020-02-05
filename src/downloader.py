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

import os
import sys
import time
import shutil
import requests
from multiprocessing import current_process

class Downloader:
    # 오류 발생 시 재시도할 횟수
    __ATTEMPT__ = 3

    def __init__(self, logger):
        self._logger = logger

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            import __main__
            application_path = os.path.dirname(__main__.__file__)

        post_dir = os.path.join(application_path, './backup/posts')
        image_dir = os.path.join(application_path, './backup/images')
            
        if not os.path.exists(post_dir):
            os.makedirs(post_dir)

        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        self.post_dir = post_dir
        self.image_dir = image_dir


    def download(self, image_list, count, lock, parser_running):
        name = current_process().name

        while parser_running.value or len(image_list) != 0:
            attempt = 0

            while attempt < Downloader.__ATTEMPT__:
                attempt += 1

                try:
                    if len(image_list) != 0:
                        # 공유 메모리 변수 락
                        with lock:
                            # 현재 카운트 저장 및 1증가
                            current_count = count.value
                            count.value += 1

                        # 이미지 데이터 추출
                        image_data = image_list.pop(0)

                        # 이미지 다운로드
                        res = requests.get(
                            image_data['src'],
                            timeout=20,
                            stream=True
                        )

                        # 파일 확장자
                        ext = image_data['src'].split('.').pop()

                        # 저장 파일명 생성
                        filename = '{}_{}_{}'.format(
                            image_data['date'],
                            image_data['title'],
                            current_count
                        )

                        # 게시물 내용 저장
                        post_file_name = '{}.txt'.format(filename)
                        with open(
                            os.path.join(self.post_dir, post_file_name),
                            'w'
                        ) as text:
                            text.write(image_data['content'])

                        # 이미지 파일 저장
                        image_file_name = '{}.{}'.format(filename, ext)
                        with open(
                            os.path.join(self.image_dir, image_file_name),
                            'wb'
                        ) as image:
                            shutil.copyfileobj(res.raw, image)
                            self._logger.info(name, filename, '다운로드 됨')

                    # 싸이월드 서버 부하 방지를 위해 잠시 대기
                    time.sleep(1)
                    break
                except IndexError:
                    break
                except Exception as e:
                    time.sleep(3)
                    self._logger.error(str(e) + ' - Attempt({}/{})' \
                        .format(attempt, Downloader.__ATTEMPT__))

        self._logger.info(name, '종료')
