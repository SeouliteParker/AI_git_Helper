# AI Git Helper

Git 변경 내용을 분석하여 AI가 **커밋 메시지(Commit Message)** 와 **Pull Request(PR) 초안**을 자동으로 작성해 주는 Python CLI 도구입니다.

개발자가 직접 `git diff` 내용을 읽고 커밋 메시지나 PR 설명을 작성해야 하는 시간을 줄이고, 변경 내용을 보다 일관된 형식으로 정리하는 것을 목표로 합니다.

---

## 1. 프로젝트 소개

개발 과정에서 코드를 수정한 뒤에는 보통 다음 작업이 필요합니다.

- 변경된 파일 확인
- `git diff` 확인
- 커밋 메시지 작성
- Pull Request 제목 작성
- PR 변경 내용 설명 작성

AI Git Helper는 이러한 과정을 간단하게 만들어 줍니다.

현재 Git 저장소의 변경 내용을 읽어 AI API에 전달하고, 그 결과를 바탕으로 다음 내용을 생성합니다.

- Commit Message
- PR 제목
- PR 설명
- 변경 이유
- 주요 변경 사항
- 테스트 방법

---

## 2. 주요 기능

### Commit 메시지 생성

현재 Git 변경 내용을 분석하여 AI가 적절한 커밋 메시지를 생성합니다.

실행 명령:

```bash
python main.py commit
```

---

### PR 초안 생성

현재 Git 변경 내용을 분석하여 Pull Request 제목과 본문 초안을 생성합니다.

실행 명령:

```bash
python main.py pr
```

PR 본문은 다음과 같은 구조로 생성될 수 있습니다.

```text
PR 제목: AI 기반 커밋 메시지 및 PR 초안 생성 기능 추가

## Why

- Git 변경 내용을 직접 분석하여 PR을 작성하는 시간을 줄이기 위해 추가했습니다.

## What

- Git diff 수집 기능 추가
- AI API 연동 기능 추가
- Commit 메시지 생성 기능 추가
- PR 초안 생성 기능 추가

## How to Test

1. 프로젝트 파일을 수정합니다.
2. python main.py pr 명령을 실행합니다.
3. 생성된 PR 제목과 설명을 확인합니다.
```

---

## 3. 프로젝트 구조

```text
AI_git_Helper/
│
├─ main.py
├─ ai_client.py
├─ utils.py
├─ requirements.txt
├─ .gitignore
└─ README.md
```

### main.py

프로그램의 시작점입니다.

사용자가 입력한 명령을 확인하고 다음 기능을 실행합니다.

```text
commit
pr
```

또한 AI 모델과 관련된 옵션도 처리합니다.

---

### git_utils.py

Git 저장소의 정보를 가져오는 역할을 담당합니다.

예를 들어 다음 정보를 수집할 수 있습니다.

```bash
git status
git diff
```

즉, 현재 어떤 파일이 변경되었는지와 실제 코드가 어떻게 수정되었는지를 가져옵니다.

---

### ai_client.py

AI API와 통신하는 역할을 담당합니다.

Git 변경 내용을 프롬프트로 만들어 AI에게 전달하고 결과를 받아옵니다.

예:

```text
Git diff
        ↓
프롬프트 생성
        ↓
Gemini API
        ↓
Commit / PR 초안
```

---

## 4. 설치 방법

먼저 저장소를 Clone 합니다.

```bash
git clone https://github.com/SeouliteParker/AI_git_Helper.git
```

프로젝트 폴더로 이동합니다.

```bash
cd AI_git_Helper
```

필요한 Python 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

---

## 5. Gemini API Key 설정

AI 기능을 사용하려면 Gemini API Key가 필요합니다.

API Key는 코드 안에 직접 작성하지 않고 환경변수로 설정하는 것이 안전합니다.

### Windows PowerShell

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

`YOUR_API_KEY` 부분에 실제 Gemini API Key를 입력합니다.

예:

```powershell
$env:GEMINI_API_KEY="여기에_본인의_API_KEY"
```

API Key가 정상적으로 등록되었는지 확인하려면:

```powershell
echo $env:GEMINI_API_KEY
```

---

## 6. Commit 메시지 생성

먼저 프로젝트의 코드를 수정합니다.

Git 상태를 확인합니다.

```bash
git status
```

Commit 메시지를 생성합니다.

```bash
python main.py commit
```

예상 출력:

```text
[INFO] Commit 메시지 생성을 시작합니다.

[INFO] Model: gemini-3.8-flash
[INFO] Temperature: 0.3
[INFO] Max Tokens: 2000
[INFO] Safe Mode: False

[RESULT] 생성된 Commit 메시지

feat: AI 기반 PR 초안 생성 기능 추가

- Git diff 기반 AI 분석 기능 추가
- Commit 메시지 생성 기능 구현
- PR 설명 자동 생성 기능 구현
```

생성된 결과를 확인한 뒤 실제 Git Commit에 사용할 수 있습니다.

예:

```bash
git add .
git commit -m "feat: AI 기반 PR 초안 생성 기능 추가"
```

---

## 7. PR 초안 생성

다음 명령을 실행합니다.

```bash
python main.py pr
```

예상 출력:

```text
[INFO] Model: gemini-3.8-flash
[INFO] Temperature: 0.3
[INFO] Max Tokens: 2000
[INFO] Safe Mode: False
[INFO] PR 초안 생성을 시작합니다.

[RESULT] 생성된 PR 초안

PR 제목: AI 기반 커밋 메시지 및 PR 초안 생성 로직 연동 및 기본 모델 변경

## Why

- 개발자가 Git 변경 내용을 직접 정리해야 하는 작업을 줄이기 위해 추가했습니다.
- AI를 이용하여 변경 내용을 보다 빠르게 이해할 수 있도록 했습니다.

## What

- Git diff 수집 기능 추가
- AI Client 연동
- Commit 메시지 생성
- PR 초안 생성
- 기본 AI 모델 설정

## How to Test

1. 프로젝트 코드를 수정합니다.
2. git status 명령으로 변경 내용을 확인합니다.
3. python main.py pr 명령을 실행합니다.
4. 생성된 PR 제목과 설명을 확인합니다.
```

---

## 8. CLI 옵션

기본 실행 방법:

```bash
python main.py commit
```

또는:

```bash
python main.py pr
```

추가 옵션을 사용할 수 있습니다.

---

### AI 모델 지정

```bash
python main.py commit --model gemini-3.8-flash
```

예:

```bash
python main.py pr --model gemini-3.8-flash
```

---

### Temperature 설정

AI 응답의 다양성을 조절할 수 있습니다.

```bash
python main.py commit --temperature 0.3
```

값이 낮을수록 비교적 일관된 결과가 생성됩니다.

예:

```text
0.1 ~ 0.3
```

값이 높아질수록 표현이 다양해질 수 있습니다.

---

### 최대 출력 Token 설정

```bash
python main.py pr --max-tokens 2000
```

AI가 생성할 수 있는 최대 출력량을 제한합니다.

---

## 9. Safe Mode

민감한 정보가 AI API로 전달되는 위험을 줄이기 위해 Safe Mode를 사용할 수 있습니다.

실행:

```bash
python main.py commit --safe-mode
```

또는:

```bash
python main.py pr --safe-mode
```

Safe Mode를 사용하면 Git diff 전체를 무조건 전송하는 대신 전송할 내용을 제한하거나 민감한 정보를 줄여서 전달할 수 있습니다.

예:

```text
API Key
Password
Token
Secret
Credential
```

등과 같이 민감할 가능성이 있는 정보가 외부 AI API로 전달되지 않도록 주의해야 합니다.

Safe Mode에서는 지나치게 큰 diff가 전달되지 않도록 변경 내용을 제한할 수 있습니다.

예:

```text
최대 약 200줄
```

---

## 10. Git 변경 내용 확인

AI Git Helper를 실행하기 전에 직접 Git 상태를 확인할 수도 있습니다.

```bash
git status
```

예:

```text
Changes not staged for commit:

        modified:   main.py

Untracked files:

        ai_client.py
```

실제 변경 내용을 확인하려면:

```bash
git diff
```

새로운 파일의 경우 아직 Git이 추적하지 않는 파일은 기본 `git diff`에 나타나지 않을 수 있습니다.

먼저 다음처럼 추가할 수 있습니다.

```bash
git add ai_client.py
```

그 후 staged diff를 확인할 수 있습니다.

```bash
git diff --cached
```

---

## 11. 변경 사항이 없을 경우

Git 변경 사항이 없다면 AI에게 전달할 내용도 없습니다.

예:

```text
변경 사항이 없습니다.
```

이 경우 Commit 메시지나 PR 초안을 생성할 필요가 없습니다.

먼저 코드를 수정한 후 다시 실행합니다.

---

## 12. API Key 오류

환경변수가 설정되지 않은 경우 AI API를 사용할 수 없습니다.

예:

```text
GEMINI_API_KEY가 설정되어 있지 않습니다.
```

Windows PowerShell에서 다시 설정합니다.

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

확인:

```powershell
echo $env:GEMINI_API_KEY
```

---

## 13. API 오류 처리

AI API 호출 중에는 다음과 같은 오류가 발생할 수 있습니다.

```text
API Key 오류
네트워크 오류
요청 제한
모델 오류
응답 생성 오류
```

프로그램은 이러한 오류가 발생했을 때 프로그램 전체가 비정상 종료되지 않도록 예외 처리를 할 수 있습니다.

예:

```text
[ERROR] AI 요청 중 오류가 발생했습니다.
```

오류가 발생하면 다음 사항을 확인합니다.

```text
1. 인터넷 연결
2. API Key
3. AI 모델 이름
4. API 사용량
5. 요청 제한 여부
```

---

## 14. API 비용 및 요청 제한

AI API는 서비스 정책에 따라 무료 사용량 또는 사용 제한이 있을 수 있습니다.

너무 자주 요청하면 다음과 같은 문제가 발생할 수 있습니다.

```text
Rate Limit
Quota 초과
API 비용 증가
```

따라서 Git 변경 내용을 확인한 후 필요한 경우에만 AI 요청을 실행하는 것이 좋습니다.

---

## 15. 보안 주의사항

Git diff 안에는 민감한 정보가 포함될 가능성이 있습니다.

예:

```text
API Key
Password
Access Token
Database Password
Secret Key
개인정보
내부 서버 주소
```

이러한 내용은 외부 AI API로 보내지 않는 것이 중요합니다.

API Key를 Python 코드에 직접 작성하지 않습니다.

잘못된 예:

```python
API_KEY = "실제_API_KEY"
```

권장 방식:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

또한 `.env` 파일을 사용하는 경우 `.gitignore`에 반드시 등록해야 합니다.

예:

```text
.env
```

---

## 16. .gitignore

Python 프로젝트에서 불필요한 파일이나 민감한 파일이 GitHub에 올라가지 않도록 `.gitignore`를 사용합니다.

예:

```gitignore
__pycache__/
*.pyc

.env

.venv/
venv/

.DS_Store
```

`__pycache__`와 `.pyc` 파일은 Python 실행 중 자동으로 만들어지는 캐시 파일이므로 일반적으로 Git에서 관리하지 않습니다.

이미 Git에 올라간 파일은 `.gitignore`를 추가하는 것만으로 자동 삭제되지 않습니다.

Git 추적을 제거하려면 다음과 같이 실행할 수 있습니다.

```bash
git rm -r --cached __pycache__
```

그 후 Commit 합니다.

```bash
git add .gitignore
git commit -m "chore: remove Python cache files"
git push
```

---

## 17. AI 결과 검토

AI가 생성한 Commit 메시지와 PR 설명을 그대로 사용하는 것이 아니라 실제 코드 변경 내용과 일치하는지 확인해야 합니다.

특히 다음 부분을 확인합니다.

```text
변경하지 않은 기능을 AI가 설명하고 있지 않은지
파일 이름이 정확한지
테스트 방법이 실제 프로젝트와 맞는지
민감정보가 포함되어 있지 않은지
```

AI 결과는 최종 결과가 아니라 개발자를 돕기 위한 초안으로 사용하는 것이 좋습니다.

---

## 18. 전체 동작 흐름

```text
개발자가 코드 수정
        ↓
git status
        ↓
git diff
        ↓
AI Git Helper 실행
        ↓
Git 변경 내용 수집
        ↓
프롬프트 생성
        ↓
Gemini API 호출
        ↓
AI 분석
        ↓
Commit 메시지 또는 PR 초안 생성
        ↓
개발자 검토
        ↓
Git Commit / Pull Request 작성
```

---

## 19. 사용 예시

### Commit 생성

```bash
python main.py commit
```

### PR 생성

```bash
python main.py pr
```

### Safe Mode Commit

```bash
python main.py commit --safe-mode
```

### Safe Mode PR

```bash
python main.py pr --safe-mode
```

### Temperature 변경

```bash
python main.py commit --temperature 0.2
```

### 최대 Token 변경

```bash
python main.py pr --max-tokens 1500
```

### 모델 지정

```bash
python main.py pr --model gemini-3.8-flash
```

---

## 20. 프로젝트 목표

이 프로젝트의 핵심 목표는 단순히 AI API를 호출하는 것이 아닙니다.

Git 변경 내용을 AI가 이해하기 좋은 입력으로 구성하고, 실제 개발 과정에서 사용할 수 있는 Commit 메시지와 PR 설명을 생성하는 것이 핵심입니다.

이를 통해 다음 과정을 경험할 수 있습니다.

- Git 명령어 활용
- Python CLI 프로그램 구조
- subprocess를 이용한 Git 명령 실행
- AI API 연동
- Prompt 설계
- 환경변수를 이용한 API Key 관리
- 예외 처리
- 보안 처리
- Commit / Pull Request Workflow

---

## Repository

GitHub:

```text
https://github.com/SeouliteParker/AI_git_Helper
```