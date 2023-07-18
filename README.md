# Red Horse (Backend)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

간단한 온라인 매칭 서비스입니다.

## Requirements

- Python 3.11
- virtualenv
- [Pusher](https://pusher.com/channels/) 회원가입 및 Channels 앱 생성
  - Frontend 채팅 동기화 목적
- SMS API 연동 (Optional)
  - 회원인증 및 비밀번호 찾기 등에 이용
  - SMS 제공 서비스업체의 API 연동 필요([SMS 호출 함수](https://github.com/kimfame/redhorse/blob/main/core/sms.py)에 코드 추가)

## Installation (Local 개발환경 구축방법)

프로젝트 소스 다운로드

```bash
git clone https://github.com/kimfame/redhorse.git
```

프로젝트 폴더로 이동

```bash
cd redhorse
```

가상환경 구축 및 활성화

```bash
virtualenv venv
. venv/bin/activate
```

패키지 설치

```bash
pip install -r requirements-dev.txt
```

환경변수 파일 생성 및 값 입력

```bash
cp env_template.txt .env
vi .env
```

즉각 테스트를 원할 경우, 아래와 같이 환경변수 파일 생성 (임시 또는 거짓 데이터)

```bash
cp env_local_example.txt .env
```

테스트 환경에 프로젝트 구성에 필요한 기초 데이터 셋팅

```bash
./scripts/local_db_reset.sh
```

로컬 개발서버 실행

```bash
python manage.py runserver
```

## License

Licensed under the
[MIT](https://github.com/kimfame/redhorse/blob/main/LICENSE) License.
