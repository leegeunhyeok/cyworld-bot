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
import requests
from multiprocessing import current_process

class Downloader:
    def __init__(self, logger):
        self._logger = logger


    def download(self, image_list, count, lock, parser_running):
        name = current_process().name

        while parser_running.value or len(image_list) != 0:
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
                    res = requests.get(image_data['src'])

                    # 파일 확장자
                    ext = image_data['src'].split('.').pop()

                    # 저장 파일명 생성
                    filename = '{}_{}_{}'.format(
                        image_data['date'],
                        image_data['title'],
                        current_count
                    )

                    # 게시물 내용 저장
                    with open('./posts/{}.txt'.format(filename), 'w') as text:
                        text.write(image_data['content'])

                    # 이미지 파일 저장
                    with open('./images/{}.{}'.format(filename, ext), 'wb') \
                        as image:
                        image.write(res.content)
                        self._logger.info(name, filename, '다운로드 됨')

                # 싸이월드 서버 부하 방지를 위해 잠시 대기
                time.sleep(1)
            except Exception as e:
                self._logger.error(str(e))

        self._logger.info(name, '종료')
