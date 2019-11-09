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

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Cyworld Bot'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 메인 레이아웃
        mainLayout = QVBoxLayout()

        # 로고 이미지, 설명 문구
        logo = QLabel(self)
        logo.setPixmap(QPixmap('logo.png'))
        logo.setAlignment(Qt.AlignCenter)
        description = QLabel('싸이월드의 사진들로 추억을 간직하세요')
        description.setAlignment(Qt.AlignCenter)

        mainLayout.addWidget(logo)
        mainLayout.addWidget(description)

        self.setLayout(mainLayout)
        self.setFixedSize(self.width, self.height)
        self.show()

if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())
