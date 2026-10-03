import os

from google import genai
from google.genai import types
from google.genai import errors


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY 환경변수가 설정되지 않았습니다."
        )

    return api_key


def generate_commit_message(
    diff_text,
    model="gemini-3.8-flash",
    temperature=0.3,
    max_tokens=500
):
    try:
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

        prompt = f"""
아래 Git diff를 분석해서 커밋 메시지를 작성해줘.

조건:
- 커밋 제목 1줄 필수
- feat:, fix:, refactor:, docs:, chore: 형식 사용
- 제목은 최대 72자
- 필요하면 핵심 변경 내용을 불릿으로 작성
- 불필요한 설명은 하지 말 것

Git diff:
{diff_text}
"""

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        return response.text

    except ValueError as e:
        return f'[ERROR] {e}\n예) $env:GEMINI_API_KEY="YOUR_KEY"'

    except errors.ClientError as e:
        return f"[ERROR] AI API 요청 오류: {e}"

    except errors.ServerError as e:
        return f"[ERROR] AI 서버 오류: {e}"

    except Exception as e:
        return f"[ERROR] AI API 호출 실패: {e}"


def generate_pr_draft(
    diff_text,
    model="gemini-3.8-flash",
    temperature=0.3,
    max_tokens=700
):
    try:
        api_key = get_api_key()
        client = genai.Client(api_key=api_key)

        prompt = f"""
아래 Git diff를 분석해서 Pull Request 초안을 작성해줘.

반드시 아래 형식을 그대로 지켜서 출력해.

PR 제목: 한 줄, 최대 80자

## Why
- 변경 배경을 최소 1개 불릿으로 작성

## What
- 핵심 변경 사항을 최소 1개 불릿으로 작성

## How to Test
- 테스트 방법을 최소 1개 불릿으로 작성

중요:
- 제목만 출력하면 안 됨
- Why / What / How to Test 세 섹션은 반드시 모두 포함
- 각 섹션마다 최소 1개의 '-' 불릿 필수
- 불필요한 설명은 하지 말 것

Git diff:
{diff_text}
"""

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            ),
        )

        result = response.text

        required_sections = [
            "## Why",
            "## What",
            "## How to Test"
        ]

        # 필수 섹션이 빠졌으면 한 번만 다시 생성
        if not all(section in result for section in required_sections):
            retry_prompt = f"""
이전 결과가 PR 형식을 지키지 않았습니다.
아래 형식 외에는 출력하지 마세요.

PR 제목: 변경 내용을 나타내는 한 줄

## Why
- 변경 배경

## What
- 핵심 변경 사항

## How to Test
- 테스트 방법

반드시 Why, What, How to Test 세 섹션을 모두 작성하세요.

Git diff:
{diff_text}
"""

            response = client.models.generate_content(
                model=model,
                contents=retry_prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )

            result = response.text

        return result

    except ValueError as e:
        return f'[ERROR] {e}\n예) $env:GEMINI_API_KEY="YOUR_KEY"'

    except errors.ClientError as e:
        return f"[ERROR] AI API 요청 오류: {e}"

    except errors.ServerError as e:
        return f"[ERROR] AI 서버 오류: {e}"

    except Exception as e:
        return f"[ERROR] AI API 호출 실패: {e}"