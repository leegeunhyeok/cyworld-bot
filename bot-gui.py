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
import multiprocessing

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt

from bot import CyBot
from src.util import open_directory, resource_path

class MainWidget(QWidget):
    def __init__(self, window, left, top, width, height, cpu_count):
        '''생성자

        Parameters
        ----------
        left : int, required
            좌측 여백
        top : int, required
            상단 여백
        width : int, required
            폭
        height : int, required
            높이
        cpu_count : int, required
            CPU 코어 수
        '''
        super().__init__()
        self.window = window
        self.setGeometry(left, top, width, height)
        self.chromeDriver = ''
        self.parserCount = 1
        self.downloaderCount = 1

        # 메인 레이아웃
        mainLayout = QVBoxLayout()

        # 로고 이미지, 설명 문구
        logo = QLabel()
        logo.setPixmap(QPixmap(resource_path('logo.png')))
        logo.setAlignment(Qt.AlignCenter)
        description = QLabel('싸이월드의 사진들로 추억을 간직하세요')
        description.setAlignment(Qt.AlignCenter)

        # 계정 정보 레이아웃
        accountForm = QFormLayout()
        emailLabel = QLabel('E-Mail')
        emailField = QLineEdit(self)
        self.emailField = emailField

        passwordLabel = QLabel('Password')
        passwordField = QLineEdit(self)
        passwordField.setEchoMode(QLineEdit.Password)
        self.passwordField = passwordField

        accountForm.addRow(emailLabel, emailField)
        accountForm.addRow(passwordLabel, passwordField)

        accountLayout = QHBoxLayout()
        accountLayout.addStretch(1)
        accountLayout.addLayout(accountForm)
        accountLayout.addStretch(1)

        # 설정 폼 레이아웃
        optionLayout = QVBoxLayout()
        
        # 크롬 드라이버 옵션 레이아웃
        chromeDriverLayout = QFormLayout()
        chromeDriverLabel = QLabel('Chrome Driver')
        chromeDriverButton = QPushButton('불러오기')
        chromeDriverButton.clicked.connect(self.onDriverSelect)

        chromeDriverLayout.addRow(chromeDriverLabel, chromeDriverButton)

        # 파서, 다운로더 옵션 영역 (#1)
        primaryOptionLayout = QFormLayout()
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

        primaryOptionLayout.addRow(parserLabel, parserOption)
        primaryOptionLayout.addRow(downloaderLabel, downloaderOption)

        # 네트워크 대기시간, 지연시간 옵션 영역 (#2)
        secondaryOptionLayout = QFormLayout()
        timeoutLabel = QLabel('Timeout')
        timeoutField = QLineEdit('10')
        timeoutField.setFixedWidth(50)
        self.timeoutField = timeoutField

        delayLabel = QLabel('Delay')
        delayField = QLineEdit('3')
        delayField.setFixedWidth(50)
        self.delayField = delayField

        secondaryOptionLayout.addRow(timeoutLabel, timeoutField)
        secondaryOptionLayout.addRow(delayLabel, delayField)
        secondaryOptionLayout.setContentsMargins(0, 2, 0, 0)

        mergeOptionLayout = QHBoxLayout()
        mergeOptionLayout.addStretch()
        mergeOptionLayout.addLayout(primaryOptionLayout)
        mergeOptionLayout.addLayout(secondaryOptionLayout)
        mergeOptionLayout.addStretch()

        chromeHLayout = QHBoxLayout()
        chromeHLayout.addStretch(1)
        chromeHLayout.addLayout(chromeDriverLayout)
        chromeHLayout.addStretch(1)

        optionLayout.addLayout(chromeHLayout)
        optionLayout.addLayout(mergeOptionLayout)

        # 개발자 및 깃허브 정보
        style = 'style="color: #888888; text-decoration: none;"'
        href_profile = 'href="https://github.com/leegeunhyeok"'
        developer = QLabel('<a {} {}>Developed by leegeunhyeok</a>'.format(style, href_profile))
        developer.setAlignment(Qt.AlignCenter)
        developer.setOpenExternalLinks(True)

        # 하단 레이아웃 (시작 버튼 영역)
        bottomLayout = QHBoxLayout()
        startButton = QPushButton('시작하기')
        startButton.clicked.connect(self.onStart)
        bottomLayout.setAlignment(Qt.AlignCenter)
        bottomLayout.addWidget(startButton)

        # 메인 레이아웃에 모든 요소 추가
        mainLayout.addWidget(logo)
        mainLayout.addWidget(description)
        mainLayout.addStretch(1)
        mainLayout.addLayout(accountLayout)
        mainLayout.addStretch(1)
        mainLayout.addLayout(optionLayout)
        mainLayout.addLayout(bottomLayout)
        mainLayout.addStretch(1)
        mainLayout.addWidget(developer)

        self.setLayout(mainLayout)
        self.setFixedSize(width, height)

    def showDialog(self, message):
        '''대화창을 생성합니다.

        Parameters
        ----------
        message : str, required
            대화창에 표시할 메시지
        '''
        dialogWidth = 300
        dialogHeight = 120

        dialog = QDialog()
        dialogLayout = QVBoxLayout()
        message = QLabel(message)
        message.setAlignment(Qt.AlignCenter)
        button = QPushButton('확인')
        button.clicked.connect(lambda: dialog.close())

        dialogLayout.addStretch(1)
        dialogLayout.addWidget(message)
        dialogLayout.addStretch()
        dialogLayout.addWidget(button)
        dialogLayout.setAlignment(Qt.AlignCenter)
        dialogLayout.addStretch(1)

        dialog.setLayout(dialogLayout)
        dialog.setWindowTitle('알림')
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.setFixedSize(dialogWidth, dialogHeight)
        dialog.exec_()

    def onDriverSelect(self):
        '''파일 대화창을 열고 선택한 파일 경로를 chromeDriver에 저장합니다.'''
        self.chromeDriver = QFileDialog.getOpenFileName(self)[0]

    def onStart(self):
        '''싸이월드 크롤링 작업을 시작합니다.

        만약 유저 정보가 비어있거나, 드라이버를 선택하지 않은 경우 알림창을 표시합니다.
        '''
        email = self.emailField.text()
        password = self.passwordField.text()

        try:
            timeout = int(self.timeoutField.text())
            delay = int(self.delayField.text())
        except ValueError as e:
            self.showDialog('대기시간과 지연시간은 숫자로 입력해주세요')
            return

        if email and password and self.chromeDriver:
            self.window.start(
                email,
                password,
                self.chromeDriver,
                self.parserCount,
                self.downloaderCount,
                timeout,
                delay
            )
        else:
            if not (email and password):
                self.showDialog('계정 정보를 입력해주세요')
            elif not self.chromeDriver:
                self.showDialog('크롬 드라이버 파일을 선택해주세요')

    def onParserOption(self, item):
        '''파서 프로세스 수가 변경된 경우 호출되는 핸들러

        Parameters
        ----------
        item : str, required
            선택된 항목의 인덱스 번호
        '''
        self.parserCount = item + 1

    def onDownloaderOption(self, item):
        '''다운로더 프로세스 수가 변경된 경우 호출되는 핸들러

        Parameters
        ----------
        item : str, required
            선택된 항목의 인덱스 번호
        '''
        self.downloaderCount = item + 1

class ProcessWidget(QWidget):
    def __init__(self, window, left, top, width, height):
        '''생성자'''
        super().__init__()
        self.setGeometry(left, top, width, height)

        # 메인 레이아웃
        mainLayout = QVBoxLayout()

        # 로고 이미지, 설명 문구
        logo = QLabel()
        logo.setPixmap(QPixmap(resource_path('logo.png')))
        logo.setAlignment(Qt.AlignCenter)
        message = QLabel()
        message.setAlignment(Qt.AlignCenter)

        loadingAnimation = QMovie(resource_path('loading.gif'))
        loading = QLabel()
        loading.setMovie(loadingAnimation)
        loading.setAlignment(Qt.AlignCenter)
        loadingAnimation.start()

        buttonLayout = QHBoxLayout()

        homeButton = QPushButton('처음으로')
        homeButton.clicked.connect(window.showMainWidget)
        openButton = QPushButton('결과 폴더 열기')
        openButton.clicked.connect(self.openResultPath)

        buttonLayout.addStretch(1)
        buttonLayout.addWidget(homeButton)
        buttonLayout.addWidget(openButton)
        buttonLayout.addStretch(1)

        mainLayout.addStretch(1)
        mainLayout.addWidget(logo)
        mainLayout.addSpacing(50)
        mainLayout.addWidget(loading)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(message)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch(2)

        self.loading = loading
        self.message = message
        self.homeButton = homeButton
        self.openButton = openButton
        self.setLayout(mainLayout)
        self.setFixedSize(width, height)

    def openResultPath(self):
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            application_path = os.path.dirname(__file__)

        open_directory(os.path.join(application_path, './backup'))


class BotWorker(QThread):
    def __init__(self, window, user_email, user_password, chromedriver, \
        parser, downloader, wait_timeout, delay):
        super(BotWorker, self).__init__()
        self.window = window
        self.user_email = user_email
        self.user_password = user_password
        self.chromedriver = chromedriver
        self.parser = parser
        self.downloader = downloader
        self.wait_timeout = wait_timeout
        self.delay = delay
        
    def run(self):
        bot = CyBot(
            self.chromedriver,
            wait=self.wait_timeout,
            delay=self.delay,
            headless=True,
            onlog=self.window.log_callback,
            onerror=self.window.error,
            done=self.window.done
        )

        bot = bot.init()

        if bot:
            bot = bot.login(self.user_email, self.user_password)
        
        if bot:
            bot = bot.home()

        if bot:
            bot.run(parser=self.parser, downloader=self.downloader)

    def stop(self):
        self.quit()
        self.wait()


class App(QMainWindow):
    def __init__(self):
        '''생성자'''
        super().__init__()
        self.title = 'Cyworld Bot v{}'.format(CyBot.__VERSION__) 
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.cpu_count = multiprocessing.cpu_count()
        self.worker = None
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.mainWidget = MainWidget(
            self,
            self.left,
            self.top,
            self.width,
            self.height,
            self.cpu_count
        )

        self.processWidget = ProcessWidget(
            self,
            self.left,
            self.top,
            self.width,
            self.height
        )

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.addWidget(self.mainWidget)
        self.centralWidget.addWidget(self.processWidget)
        self.showMainWidget()
        self.show()

    def showMainWidget(self):
        '''메인 위젯으로 화면을 전환합니다.'''
        self.centralWidget.setCurrentWidget(self.mainWidget)

    def showProcessWidget(self):
        '''작업 중 위젯으로 화면을 전환합니다.'''
        self.centralWidget.setCurrentWidget(self.processWidget)

    def start(self, user_email, user_password, chromedriver, 
        parser, downloader, wait_timeout, delay):
        self.processWidget.message.setText('작업 준비 중..')
        self.processWidget.homeButton.hide()
        self.processWidget.openButton.hide()
        self.processWidget.loading.show()
        self.showProcessWidget()
        
        worker = BotWorker(
            self,
            user_email,
            user_password,
            chromedriver, 
            parser,
            downloader,
            wait_timeout,
            delay
        )

        worker.start()
        self.worker = worker

    def log_callback(self, message):
        self.processWidget.message.setText(message)

    def error(self):
        self.worker.stop()
        self.processWidget.loading.hide()
        self.processWidget.homeButton.show()

    def done(self):
        self.processWidget.message.setText('게시물 다운로드가 완료되었습니다!')
        self.processWidget.loading.hide()
        self.processWidget.homeButton.show()
        self.processWidget.openButton.show()

if __name__ == '__main__':
    # 윈도우 환경을 위함
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    logo = '''
                ,000,
                0   0
                '000'
                  0
                  0
           ,0000000000000,
        ,0'000000000000000'0,
      ,00000`           `00000,
     ,0000`  @         @  `0000,
     0000`   @   ,00   @   `0000
     0000       00          0000
     0000,       '00       ,0000
     '0000,   (_______)   ,0000'
      '00000,          ,00000'
        '0,000000000000000,0'
           '0000000000000'

                CyBot

          GUI VERSION 1.0.0
    '''
    print(logo, end='\n\n')
    print('알림: 잠시만 기다려주세요..')
    print('알림: 이 창은 절대 닫지 마세요!')
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path('icon.ico')))
    CyWorldBot = App()
    sys.exit(app.exec_())
