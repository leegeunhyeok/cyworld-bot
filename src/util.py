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

import re
import os
import sys
import subprocess

class EC_or:
    def __init__(self, *args):
        self.ecs = args
    
    def __call__(self, driver):
        for ec in self.ecs:
            try:
                if ec(driver):
                    return True
            except:
                pass

def extract_number(s):
    return re.findall(r'\d+', s)

def extract_date(s):
    return re.search(r'\d{4}.\d{2}.\d{2}', s).group()

def to_valid_filename(s):
    return re.sub(r'[^a-zA-Z0-9가-힣]', '_', s)

def update_size(s):
    sh = re.sub(r'height=\d{0,10}', 'height=10000', s)
    return re.sub(r'width=\d{0,10}', 'width=10000', sh)

def clean_text(s):
    return re.sub(r'\s{2,}', '', s)

def open_directory(path):
    try:
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':
            subprocess.check_call(['open', '--', path])
        else:
            subprocess.check_call(['xdg-open', '--', path])
    except:
        pass

def resource_path(relative_path):
    try:
        # PyInstaller는 _MEIPASS에 경로 저장함
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)
