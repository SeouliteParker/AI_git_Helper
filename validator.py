import re

COMMIT_TITLE_RECOMMEND = 50
COMMIT_TITLE_MAX = 72
PR_TITLE_MAX = 80
PR_SECTIONS = ["## Why", "## What", "## How to Test"]
PLACEHOLDER = "- (작성 필요)"


def strip_code_fence(text):
    # AI가 ``` 로 감싸서 줄 때가 있어서 제거
    lines = [
        line for line in text.strip().splitlines()
        if not line.strip().startswith("```")
    ]
    return "\n".join(lines).strip()


def validate_commit(text):
    """커밋 메시지를 제목/본문으로 나누고 제목 길이를 검증한다."""
    warnings = []
    lines = strip_code_fence(text).splitlines()

    # 앞쪽 빈 줄 제거
    while lines and not lines[0].strip():
        lines.pop(0)

    if not lines:
        return "", "", ["커밋 메시지가 비어 있습니다."]

    title = lines[0].strip()
    body = "\n".join(lines[1:]).strip()

    if len(title) > COMMIT_TITLE_MAX:
        warnings.append(
            f"커밋 제목이 {len(title)}자라서 {COMMIT_TITLE_MAX}자로 잘랐습니다."
        )
        title = title[:COMMIT_TITLE_MAX].rstrip()
    elif len(title) > COMMIT_TITLE_RECOMMEND:
        warnings.append(
            f"커밋 제목이 {len(title)}자입니다. (권장 {COMMIT_TITLE_RECOMMEND}자 이내)"
        )

    return title, body, warnings


def validate_pr(text):
    """PR 초안을 제목/본문으로 나누고 길이·섹션·불릿 규칙을 맞춘다."""
    warnings = []
    lines = strip_code_fence(text).splitlines()

    # 1) 제목 찾기
    title = ""
    body_lines = []

    for line in lines:
        stripped = line.strip()
        if not title and stripped.startswith("PR 제목:"):
            title = stripped.split(":", 1)[1].strip()
        else:
            body_lines.append(line)

    # "PR 제목:"이 없으면 섹션이 아닌 첫 줄을 제목으로 사용
    if not title:
        for i, line in enumerate(body_lines):
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                title = stripped
                body_lines.pop(i)
                break

    if not title:
        warnings.append("PR 제목을 찾지 못했습니다.")
    elif len(title) > PR_TITLE_MAX:
        warnings.append(
            f"PR 제목이 {len(title)}자라서 {PR_TITLE_MAX}자로 잘랐습니다."
        )
        title = title[:PR_TITLE_MAX].rstrip()

    # 2) 섹션별로 내용 모으기
    sections = {name: [] for name in PR_SECTIONS}
    lookup = {name.lower(): name for name in PR_SECTIONS}
    current = None

    for line in body_lines:
        stripped = line.strip()

        if stripped.lower() in lookup:
            current = lookup[stripped.lower()]
            continue

        if stripped.startswith("#"):
            current = None
            continue

        if not current or not stripped:
            continue

        # "1. 내용" 같은 번호 목록은 불릿으로 변환
        numbered = re.match(r"^\d+[.)]\s+(.*)", stripped)
        if numbered:
            stripped = "- " + numbered.group(1)

        if stripped.startswith(("- ", "* ")):
            sections[current].append("- " + stripped[2:].strip())
        else:
            sections[current].append("- " + stripped)

    # 3) 빠진 섹션/불릿 채우기
    for name in PR_SECTIONS:
        if not sections[name]:
            warnings.append(f"{name} 섹션에 불릿이 없어 '(작성 필요)'를 넣었습니다.")
            sections[name].append(PLACEHOLDER)

    # 4) 본문 다시 조립
    body_parts = []
    for name in PR_SECTIONS:
        body_parts.append(name)
        body_parts.extend(sections[name])
        body_parts.append("")

    body = "\n".join(body_parts).strip()
    return title, body, warnings