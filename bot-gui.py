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
import multiprocessing

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWidget(QWidget):
    def __init__(self, left, top, width, height, cpu_count):
        super().__init__()
        self.setGeometry(left, top, width, height)
        self.parserCount = 1
        self.downloaderCount = 1

        # 메인 레이아웃
        mainLayout = QVBoxLayout()

        # 로고 이미지, 설명 문구
        logo = QLabel()
        logo.setPixmap(QPixmap('a.png'))
        logo.setAlignment(Qt.AlignCenter)
        description = QLabel('싸이월드의 사진들로 추억을 간직하세요')
        description.setAlignment(Qt.AlignCenter)

        # 계정 정보 레이아웃
        accountForm = QFormLayout()
        emailLabel = QLabel('E-Mail')
        emailField = QLineEdit(self)

        passwordLabel = QLabel('Password')
        passwordField = QLineEdit(self)
        passwordField.setEchoMode(QLineEdit.Password)

        accountForm.addRow(emailLabel, emailField)
        accountForm.addRow(passwordLabel, passwordField)

        # 설정 폼 레이아웃
        optionForm = QFormLayout()
        chromeDriverLabel = QLabel('Chrome Driver')
        driverButton = QPushButton('불러오기')
        driverButton.clicked.connect(self.onDriverSelect)

        parserLabel = QLabel('Parser')
        parserOption = QComboBox(self)
        for i in range(cpu_count):
            parserOption.addItem(str(i + 1))
        parserOption.currentIndexChanged.connect(self.onParserOption)
        parserOption.setCurrentIndex(int(cpu_count / 2) - 1)

        downloaderLabel = QLabel('Downloader')
        downloaderOption = QComboBox(self)
        for i in range(cpu_count):
            downloaderOption.addItem(str(i + 1))
        downloaderOption.currentIndexChanged.connect(self.onDownloaderOption)
        downloaderOption.setCurrentIndex(int(cpu_count / 2) - 1)

        optionForm.addRow(chromeDriverLabel, driverButton)
        optionForm.addRow(parserLabel, parserOption)
        optionForm.addRow(downloaderLabel, downloaderOption)

        # 하단 레이아웃 (시작 버튼 영역)
        bottomLayout = QHBoxLayout()
        startButton = QPushButton('시작하기')
        startButton.clicked.connect(self.onStart)
        bottomLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.addWidget(startButton)

        # 메인 레이아웃에 모든 요소 추가
        mainLayout.addWidget(logo)
        mainLayout.addWidget(description)
        mainLayout.addSpacing(30)
        mainLayout.addLayout(accountForm)
        mainLayout.addLayout(optionForm)
        mainLayout.addSpacing(20)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)
        self.setFixedSize(width, height)

    def showDialog(self, message):
        dialogWidth = 200
        dialogHeight = 100

        dialog = QDialog()
        dialogLayout = QVBoxLayout()
        message = QLabel(message)
        message.setAlignment(Qt.AlignCenter)
        button = QPushButton('확인')
        button.clicked.connect(lambda: dialog.close())

        dialogLayout.addSpacing(10)
        dialogLayout.addWidget(message)
        dialogLayout.addStretch()
        dialogLayout.addWidget(button)
        dialogLayout.setAlignment(Qt.AlignCenter)
        dialogLayout.addSpacing(10)

        dialog.setLayout(dialogLayout)
        dialog.setWindowTitle('알림')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setFixedSize(dialogWidth, dialogHeight)
        dialog.exec_()

    def onDriverSelect(self):
        self._fileName = QFileDialog.getOpenFileName(self)

    def onStart(self):
        self.showDialog('Hello')

    def onParserOption(self, item):
        self.parserCount = item + 1

    def onDownloaderOption(self, item):
        self.downloaderCount = item + 1


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Cyworld Bot'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.cpu_count = multiprocessing.cpu_count()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.mainWidget = MainWidget(
            self.left,
            self.top,
            self.width,
            self.height,
            self.cpu_count
        )

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.addWidget(self.mainWidget)
        self.centralWidget.addWidget(self.mainWidget)
        self.showMainWidget()
        self.show()

    def showMainWidget(self):
        self.centralWidget.setCurrentWidget(self.mainWidget)

    def showRunningWidget(self):
        self.centralWidget.setCurrentWidget(self.mainWidget)

if __name__ == '__main__':
    app = QApplication([])
    CyWorldBot = App()
    sys.exit(app.exec_())
