Python 3.10 이상이 필요합니다. (`google-genai` 라이브러리가 3.10 이상을 요구합니다.)

**1) 저장소 받기**

```bash
git clone https://github.com/SeouliteParker/AI_git_Helper.git
cd AI_git_Helper
```

**2) 가상환경 만들기 및 활성화**

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

프롬프트 앞에 `(.venv)`가 붙으면 활성화된 것입니다. PowerShell에서 스크립트 실행 오류가 나면 아래를 먼저 실행합니다.

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**3) 버전 확인 및 패키지 설치**

```bash
python --version   # 3.10 이상인지 확인
pip install -r requirements.txt
```

`.venv` 폴더는 `.gitignore`에 등록되어 있어 GitHub에 올라가지 않습니다.