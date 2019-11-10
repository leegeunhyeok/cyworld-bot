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
from datetime import datetime

class Logger:
    def __init__(self, filename, callback=None):
        self._format = '%Y-%m-%d %H:%M:%S.%f'
        self._filename = filename
        self._callback = callback

    def _timestamp(self):
        return '(' + datetime.now().strftime(self._format) + ')'

    def _log(self, level, *args, callback):
        m = level + ' ' + (' '.join(args[0]))
        tm = self._timestamp() + ' - ' + m
        print(tm)

        if self._callback and callback:
            self._callback(m)

        with open(self._filename, 'a', encoding='utf8') as f:
            f.write(tm.strip() + '\n')

    def info(self, *args, callback=True):
        self._log('[INFO]', args, callback=callback)

    def success(self, *args, callback=True):
        self._log('[SUCCESS]', args, callback=callback)

    def warning(self, *args, callback=True):
        self._log('[WARNING]', args, callback=callback)

    def error(self, *args, callback=True):
        self._log('[ERROR]', args, callback=callback)

    def danger(self, *args, callback=True):
        self._log('[DANGER]', args, callback=callback)

    def critical(self, *args, callback=True):
        self._log('[CRITICAL]', args, callback=callback)
