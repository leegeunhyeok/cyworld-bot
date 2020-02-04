
<div align="center">
  <img src="./logo.png">

싸이월드의 사진들로 추억을 간직하세요

  <img alt="Github actions" src="https://github.com/leegeunhyeok/cyworld-bot/workflows/pyinstaller-build/badge.svg">

</div>


## 설치 및 사용법 - GUI 방식

### 0. 사전 준비

정상적인 실행을 위해 크롬 드라이버가 필요합니다.
- 크롬 드라이버 - [다운로드](https://sites.google.com/a/chromium.org/chromedriver/downloads)

자세한 내용은 [여기](#3-크롬-드라이버-다운로드)를 참고해주세요

### 1. 프로그램 다운로드

- CyBot [다운로드](https://github.com/leegeunhyeok/cyworld-bot/releases)

> `2020.02.04` 기준 지원 운영체제 (Windows, MacOS)

### 2. 기본 설정

- 다운로드 받은 파일을 실행해주세요
  - 콘솔창이 먼저 표시되고 잠시 뒤 아래와 같은 창이 표시됩니다.
  - ※ 콘솔창은 절대 닫지 마세요 (프로그램이 종료됩니다.) ※

<img src="./guide/gui/1.png">

- `싸이월드 사용자 계정 정보`를 올바르게 입력해주세요
- 크롬 드라이버 선택 버튼을 눌러 사전 준비 단계에서 다운로드받은 `크롬 드라이버 파일`을 선택해주세요
  - 다운로드받은 크롬 드라이버 파일은 압축 해제해야합니다.
- 상세 옵션 - 일반적인 경우 조작할 필요는 없습니다.
  - parser, downloader 프로세스 수를 지정할 수 있습니다.
  - timeout: 페이지 로딩 대기시간입니다. 싸이월드 접속 시 해당 시간만큼 대기하며, 초과할 경우 작업을 중단합니다.
    - 로그인 시도, 홈 페이지로 이동 중 오류가 발생할 경우 timeout 값을 더 늘린 후 다시 시도해주세요
  - delay: 싸이월드 서버 부하 방지를 위한 CyBot 자체 대기시간입니다.
    - 기본값 사용을 권장합니다.

> 모든 설정 후 `시작하기` 버튼을 눌러 백업을 시작할 수 있습니다.

### 4. 작업 중

<img src="./guide/gui/2.png">

게시물을 수집하여 다운로드 작업이 진행됩니다.

> 게시물 수에 따라 소요되는 시간이 달라질 수 있습니다. 종료하지 말고 잠시 기다려주세요

### 3. 완료

<img src="./guide/gui/3.png">

작업이 완료되면 메시지와 함께 결과물을 확인할 수 있는 버튼이 표시됩니다.


## 설치 및 사용법 - CLI 방식

### 0. 사전 준비

- 파이썬3 - [다운로드](https://www.python.org/downloads/release/python-365)
- 구글 크롬 브라우저 - [다운로드](https://www.google.com/intl/ko/chrome)
- 크롬 드라이버 - [다운로드](https://sites.google.com/a/chromium.org/chromedriver/downloads)

아래 가이드를 통해 상세한 설치 방법을 확인하실 수 있습니다.



### 1. 소스코드 다운로드

<img src="./guide/cli/1.png">

`Clone or download` 버튼을 눌러 ZIP 파일로 소스코드를 다운로드 받습니다.
- 다운로드 받은 후 압축을 풀어주세요

### 2. 크롬 브라우저 버전 확인

<img src="./guide/cli/2.png">

`메뉴 > 도움말 > Chrome 정보` 순서대로 진입하여 정보창으로 진입합니다.

<img src="./guide/cli/3.png">

크롬 정보창에서 크롬 버전의 맨 앞자리를 메모해주세요 (위 사진의 경우 78)

### 3. 크롬 드라이버 다운로드

<img src="./guide/cli/4.png">

[크롬 드라이버 다운로드](https://chromedriver.chromium.org/downloads) 페이지에 접속하여 `3번` 과정에서 메모한 버전과 일치하는 드라이버를 다운로드 받습니다.

<img src="./guide/cli/5.png">

컴퓨터 운영체제에 맞는 버전을 다운로드 받고 압축을 풀어줍니다.
- 압축 해제 후 나온 파일은 driver 폴더에 넣어주세요

### 4. 의존 라이브러리 설치

<img src="./guide/cli/6.png">

CMD 혹은 터미널 등을 소스코드가 있는 폴더에서 열어 아래 명령어를 입력합니다.

- [파이썬](https://www.python.org/downloads/release/python-365)이 설치되어 있어야 합니다!

```bash
pip3 install -r requirements.txt
```

### 5. 기본 설정

- `config.ini` 파일을 열어 개인 설정을 진행해주세요
  - user
    - email: 싸이월드 이메일
    - password: 비밀번호
  - bot
    - chromedriver: 크롬드라이버 경로
      - 윈도우: ./driver/chromedriver.exe
      - 리눅스 & 맥: ./driver/chromedriver
    - wait: 크롬드라이버 대기시간 (초)
      - 네트워크 환경이 좋지 않아 로그인, 홈으로 이동 과정 등에서 시간초과 오류가 발생할 경우 적절히 조절해주세요
    - delay: 다운로드 지연시간 (되도록이면 기본값인 3초를 유지해주세요)
    - parser: 파싱 프로세스 수
      - ⚠️ CPU 코어 수보다 큰 수를 입력하지 않는것을 추천합니다. (1 ~ 코어 수)
    - downloader: 다운로더 프로세스 수
      - ⚠️ CPU 코어 수보다 큰 수를 입력하지 않는것을 추천합니다. (1 ~ 코어 수)

```
[user]
email=이메일
password=비밀번호

[bot]
chromedriver=./driver/chromedriver.exe
delay=3
parser=4
downloader=4
```

### 6. 실행

아래 명령어를 입력하여 싸이월드 이미지 수집을 시작할 수 있습니다.

```bash
python3 bot.py
```

<img src="./guide/cli/7.png">

- 결과 이미지는 images 폴더 내에 `날짜_번호_제목` 형식으로 저장됩니다
- 결과 텍스트는 posts 폴더 내에 `날짜_번호_제목` 형식으로 저장됩니다


## GUI(PyQt5) 빌드

> GUI 버전의 경우 파이썬 `3.7.5` 버전으로 테스트 및 빌드

```bash
# Windows
pyinstaller -F -i="icon.ico" --add-data "icon.ico;." --add-data "logo.png;." --add-data "loading.gif;." --name CyBot --clean bot-gui.py

# Mac OS
pyinstaller -F -i=icon.icns --add-data icon.icns:. --add-data logo.png:. --add-data loading.gif:. --name CyBot --clean bot-gui.py
```

- `-F`: 하나의 파일로 번들링
- `-i`: 애플리케이션 아이콘 지정
- `--add-data`: 애플리케이션 리소스 지정
- `--name`: 빌드 결과물 파일먕
- `--clean`: 임시파일 및 캐시 삭제

- `-w`: 옵션 사용 불가, (멀티 프로세싱 관련 문제가 발생.. 해결하기 위해 노력했으나 문제점을 찾지 못함)

## 이슈
사용 중 문제가 발생할 경우 [이슈](https://github.com/leegeunhyeok/cyworld-bot/issues) 남겨주세요 😊

## 개발자
[Geunhyeok LEE](https://github.com/leegeunhyeok)
