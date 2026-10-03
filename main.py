import argparse
 
from utils import get_git_status, get_git_diff, limit_diff
from ai_client import generate_commit_message, generate_pr_draft
from validator import validate_commit, validate_pr
 
 
def print_warnings(warnings):
    for warning in warnings:
        print(f"[WARN] {warning}")
 
 
def main():
    parser = argparse.ArgumentParser(
        description="Git 변경 사항을 분석해 AI가 Commit/PR 초안을 생성하는 도구"
    )
 
    parser.add_argument(
        "command",
        choices=["commit", "pr"],
        help="생성할 문서 종류: commit 또는 pr"
    )
 
    parser.add_argument(
        "--model",
        default="gemini-3.8-flash",
        help="사용할 AI 모델"
    )
 
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="AI 응답의 다양성 조절 값"
    )
 
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=2000,
        help="AI가 생성할 최대 토큰 수"
    )
 
    parser.add_argument(
        "--safe-mode",
        action="store_true",
        help="민감정보 보호 및 diff 전송량 제한"
    )
 
    args = parser.parse_args()
 
    # Git 변경 파일 확인
    git_status = get_git_status()
 
    print("[INFO] Git status 수집 완료")
    print(git_status)
 
    # 변경 사항이 없으면 프로그램 종료
    if not git_status.strip():
        print("[INFO] 변경 사항이 없습니다. 커밋/PR 초안을 생성하지 않고 종료합니다.")
        return
 
    # Git diff 수집 (staged + unstaged)
    git_diff = get_git_diff()
 
    # status에는 있지만 diff가 비었으면 (새 파일만 있는 경우 등) 종료
    if not git_diff.strip():
        print("[INFO] diff 내용이 없습니다.")
        print("[INFO] 새로 만든 파일만 있다면 git add 후 다시 실행하세요.")
        return
 
    if args.safe_mode:
        git_diff = limit_diff(git_diff, max_lines=200)
        print("[INFO] Safe Mode 적용: diff를 최대 200줄로 제한했습니다.")
 
    print("[INFO] Git diff 수집 완료")
    print(git_diff)
 
    # CLI 옵션 확인
    print(f"[INFO] Model: {args.model}")
    print(f"[INFO] Temperature: {args.temperature}")
    print(f"[INFO] Max Tokens: {args.max_tokens}")
    print(f"[INFO] Safe Mode: {args.safe_mode}")
 
    if args.command == "commit":
        print("[INFO] 커밋 메시지 생성을 시작합니다.")
 
        commit_message = generate_commit_message(
            git_diff,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
 
        if commit_message.startswith("[ERROR]"):
            print(commit_message)
            return
 
        title, body, warnings = validate_commit(commit_message)
        print_warnings(warnings)
        print("[DONE] 커밋 메시지 생성 완료")
 
        print("\n--- Commit Message ---")
        print(title)
        if body:
            print()
            print(body)
        print("----------------------")
 
    elif args.command == "pr":
        print("[INFO] PR 초안 생성을 시작합니다.")
 
        pr_draft = generate_pr_draft(
            git_diff,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens
        )
 
        if pr_draft.startswith("[ERROR]"):
            print(pr_draft)
            return
 
        title, body, warnings = validate_pr(pr_draft)
        print_warnings(warnings)
        print("[DONE] PR 초안 생성 완료")
 
        print("\n--- PR Title ---")
        print(title)
        print("\n--- PR Body ---")
        print(body)
        print("----------------")
 
 
if __name__ == "__main__":
    main()
 