# AI Git Helper

Git 변경 내용을 분석해서 AI가 **커밋 메시지**와 **Pull Request(PR) 초안**을 자동으로 작성해 주는 Python CLI 도구입니다.

`git status`, `git diff` 결과를 수집해 Gemini API에 전달하고, 생성된 결과를 길이·형식 규칙에 맞게 검증한 뒤 터미널에 출력합니다.

---

## 1. 주요 기능

- `python main.py commit` : 커밋 메시지 생성 (제목 1줄 + 핵심 변경 불릿)
- `python main.py pr` : PR 제목 + 본문(Why / What / How to Test) 생성
- 결과 검증 및 후처리 : 제목 길이 제한, PR 필수 섹션·불릿 보정
- CLI 옵션 : `--model`, `--temperature`, `--max-tokens`, `--safe-mode`
- 예외 처리 : API Key 미설정, 네트워크/인증/서버 오류 시 원인 메시지 출력

---

## 2. 프로젝트 구조

```
AI_git_Helper/
├─ main.py           # 프로그램 시작점, 전체 흐름 제어
├─ utils.py          # Git 정보 수집 (git status, git diff)
├─ ai_client.py      # Gemini API 호출, 프롬프트 구성, 예외 처리
├─ validator.py      # AI 결과 길이·형식 검증 및 후처리
├─ requirements.txt
├─ .gitignore
└─ README.md
```

| 파일 | 역할 |
| --- | --- |
| `main.py` | CLI 명령과 옵션을 받고, 수집 → AI 호출 → 검증 → 출력 순서로 실행 |
| `utils.py` | `git status --short`, `git diff HEAD`로 변경 사항 수집, safe-mode용 diff 줄 수 제한 |
| `ai_client.py` | 환경변수에서 API Key를 읽고, 커밋/PR 프롬프트를 만들어 Gemini API 호출 |
| `validator.py` | 제목 길이 검사·자르기, PR 섹션과 불릿 보정, 코드블록 표시 제거 |

---

## 3. 동작 흐름

```
python main.py commit / pr
        ↓
git status 수집 → 변경 없으면 종료
        ↓
git diff 수집 → diff 비었으면 종료
        ↓
(safe-mode) diff 최대 200줄로 제한
        ↓
프롬프트 구성 → Gemini API 호출
        ↓
validator로 길이·형식 검증 및 후처리
        ↓
구분선으로 나눠 터미널 출력
        ↓
사용자가 검토 후 직접 커밋 / PR 작성
```

---

## 4. 설치 방법

Python 3.10 이상이 필요합니다.

```bash
git clone https://github.com/SeouliteParker/AI_git_Helper.git
cd AI_git_Helper
pip install -r requirements.txt
```

---

## 5. API Key 설정

API Key는 코드에 직접 쓰지 않고 **환경변수**로만 설정합니다.

**Windows PowerShell**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
echo $env:GEMINI_API_KEY   # 확인
```

**macOS / Linux**

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
echo $GEMINI_API_KEY       # 확인
```

위 방식은 현재 터미널 창에서만 유지됩니다. 새 터미널을 열면 다시 설정해야 합니다.

---

## 6. 사용 방법

도구는 **Git이 초기화된 프로젝트 루트 디렉토리**에서 실행합니다.

### 커밋 메시지 생성

```bash
python main.py commit
```

### PR 초안 생성

```bash
python main.py pr
```

### CLI 옵션

| 옵션 | 기본값 | 설명 |
| --- | --- | --- |
| `--model` | `gemini-3.8-flash` | 사용할 AI 모델 |
| `--temperature` | `0.3` | 응답 다양성. 낮을수록 일관되고, 높을수록 표현이 다양해짐 |
| `--max-tokens` | `2000` | AI가 생성할 최대 출력 토큰 수. 너무 작으면 결과가 중간에 잘릴 수 있음 |
| `--safe-mode` | 꺼짐 | diff를 최대 200줄까지만 전송 |

```bash
python main.py commit --temperature 0.2
python main.py pr --max-tokens 1500
python main.py pr --model gemini-3.8-flash --safe-mode
```

커밋/PR 메시지처럼 형식이 정해진 글은 `temperature`를 0.1~0.3 정도로 낮게 두는 것을 권장합니다.

---

## 7. 출력 예시

### 커밋 메시지

```
[INFO] Git status 수집 완료
 M ai_client.py
 M utils.py

[INFO] Git diff 수집 완료
(git diff 내용 출력)
[INFO] Model: gemini-3.8-flash
[INFO] Temperature: 0.3
[INFO] Max Tokens: 2000
[INFO] Safe Mode: False
[INFO] 커밋 메시지 생성을 시작합니다.
[DONE] 커밋 메시지 생성 완료

--- Commit Message ---
fix: staged 변경 포함 및 API Key 예외 처리 개선

- utils.py: git diff HEAD로 staged/unstaged 변경 모두 수집
- ai_client.py: API Key 미설정 시 안내 메시지 출력
----------------------
```

### PR 초안

```
[INFO] PR 초안 생성을 시작합니다.
[DONE] PR 초안 생성 완료

--- PR Title ---
feat: 커밋/PR 결과 길이·형식 검증 기능 추가

--- PR Body ---
## Why
- AI 결과가 제목 길이나 PR 템플릿 규칙을 지키지 않는 경우가 있었습니다.

## What
- validator.py 추가: 커밋/PR 제목 길이 검사 및 자르기
- PR 본문 필수 섹션(Why/What/How to Test)과 불릿 보정
- 결과 출력에 구분선 추가

## How to Test
- 코드를 수정한 뒤 python main.py commit 실행
- python main.py pr 실행 후 세 섹션과 불릿이 모두 있는지 확인
----------------
```

---

## 8. 결과 검증 규칙 (validator.py)

AI 결과는 규칙을 항상 지키지는 않기 때문에, 출력 전에 코드로 한 번 더 검사하고 다듬습니다. 추가 API 호출 없이 **후처리** 방식으로 처리합니다.

| 대상 | 규칙 | 처리 |
| --- | --- | --- |
| 커밋 제목 | 50자 이내 권장, 최대 72자 | 50자 초과 시 경고, 72자 초과 시 72자로 자름 |
| PR 제목 | 최대 80자 | 80자 초과 시 80자로 자름 |
| PR 본문 | `## Why`, `## What`, `## How to Test` 필수 | 빠진 섹션은 추가 |
| PR 섹션 | 섹션마다 불릿 1개 이상 | 불릿이 없으면 `- (작성 필요)` 삽입 |
| 공통 | 불릿 형식 통일 | `1.` 번호 목록 → `-` 불릿 변환, ``` 코드블록 표시 제거 |

보정이 일어나면 `[WARN]`으로 무엇을 고쳤는지 알려줍니다.

```
[WARN] 커밋 제목이 86자라서 72자로 잘랐습니다.
[WARN] ## What 섹션에 불릿이 없어 '(작성 필요)'를 넣었습니다.
```

`(작성 필요)`가 보이면 해당 섹션은 직접 채워 넣어야 합니다.

---

## 9. 예외 상황

### 변경 사항이 없을 때

```
[INFO] 변경 사항이 없습니다. 커밋/PR 초안을 생성하지 않고 종료합니다.
```

### 새 파일만 있고 diff가 비어 있을 때

`git diff`는 Git이 아직 추적하지 않는 새 파일(untracked)을 보여주지 않습니다. 이 경우 AI를 호출하지 않고 종료합니다.

```
[INFO] diff 내용이 없습니다.
[INFO] 새로 만든 파일만 있다면 git add 후 다시 실행하세요.
```

`git add`로 추가한 변경(staged)은 `git diff HEAD`로 함께 수집되므로, add 후 다시 실행하면 됩니다.

### API Key가 설정되지 않았을 때

```
[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.
예) $env:GEMINI_API_KEY="YOUR_KEY"
```

### API 호출 실패

오류 종류에 따라 원인을 포함한 메시지를 출력하고, 검증 단계 없이 종료합니다.

```
[ERROR] AI API 요청 오류: ...   # 잘못된 Key, 모델 이름 오류, 요청 제한 등 (4xx)
[ERROR] AI 서버 오류: ...       # Gemini 서버 측 문제 (5xx)
[ERROR] AI API 호출 실패: ...   # 네트워크 끊김 등 그 외 오류
```

확인 순서: 인터넷 연결 → API Key → 모델 이름 → 사용량/요청 제한

---

## 10. 비용 및 요청 횟수

- `commit` : 실행 1회당 API **1회** 호출
- `pr` : 기본 **1회** 호출. AI 결과에 필수 섹션이 빠졌을 때만 1회 재요청해서 **최대 2회**
- 무료 사용량을 넘기면 `Rate Limit`, `Quota 초과` 오류가 날 수 있습니다.
- 변경 사항을 어느 정도 모은 뒤 실행하는 것을 권장합니다. 큰 diff는 토큰 사용량이 커지므로 `--safe-mode`로 줄여서 보낼 수 있습니다.

---

## 11. 보안 및 Safe Mode

`git diff`에는 API Key, 비밀번호, 토큰, 개인정보 같은 민감정보가 섞여 있을 수 있고, 이 도구는 diff를 외부 AI API로 전송합니다.

### Safe Mode가 하는 일

```bash
python main.py commit --safe-mode
```

- diff를 **최대 200줄**까지만 잘라서 전송합니다.
- 전송되는 코드 양을 줄여 노출 범위와 토큰 사용량을 줄이는 용도입니다.

### Safe Mode가 하지 않는 일

- 현재 버전은 **민감정보 마스킹을 하지 않습니다.** 200줄 안에 Key나 비밀번호가 있으면 그대로 전송됩니다.
- 따라서 실행 전에 `git diff`로 민감정보가 없는지 직접 확인해야 합니다.

### 권장 사항

- API Key는 코드에 쓰지 말고 환경변수로만 관리합니다.
- `.env` 파일은 `.gitignore`에 등록합니다. (이 리포는 이미 등록되어 있습니다.)
- 민감정보가 포함된 변경은 이 도구로 처리하지 않습니다.

현재 `.gitignore`:

```
__pycache__/
*.pyc
.env
```

---

## 12. 주의사항

생성된 커밋 메시지와 PR 초안은 **최종 정답이 아니라 초안**입니다. 적용하기 전에 아래를 확인하세요.

- 실제로 바꾸지 않은 내용을 AI가 설명하고 있지 않은지
- 파일 이름과 기능 이름이 정확한지
- How to Test가 실제 프로젝트에서 실행 가능한지
- `(작성 필요)` 표시가 남아 있지 않은지
- 민감정보가 포함되지 않았는지

이 도구는 텍스트 생성까지만 담당합니다. `git commit`, `git push`, GitHub PR 생성은 사용자가 직접 진행합니다.