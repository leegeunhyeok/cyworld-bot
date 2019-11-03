
<div align="center">
  <img src="./logo.png">

싸이월드의 사진들로 추억을 간직하세요
</div>


## 설치

- 파이썬3 버전 설치가 필요합니다 - [다운로드](https://www.python.org/downloads/release/python-365)
- 구글 크롬 브라우저가 필요합니다 - [다운로드](https://www.google.com/intl/ko/chrome)
- 크롬 드라이버가 필요합니다 - [다운로드](https://sites.google.com/a/chromium.org/chromedriver/downloads)
  - 다운로드 후 `chromedriver.exe` 파일을 `driver` 폴더에 넣어주세요 (리눅스, 맥의 경우 chromedriver)

```bash
# 본 저장소 다운로드 받기
git clone https://github.com/leegeunhyeok/cyworld-bot.git

# 의존 라이브러리 설치
pip install -r requirement.txt

# 실행!
python bot.py
```

## 설정

- `config.ini` 파일에 싸이월드 로그인을 위한 계정을 입력해주세요

```
[USER]
id=아이디
password=비밀번호
```
