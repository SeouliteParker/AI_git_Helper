import argparse

from utils import get_git_status, get_git_diff, limit_diff

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
        default="gpt-5.6",
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
        default=500,
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

    # Git diff 수집
    git_diff = get_git_diff()

    print("[INFO] Git diff 수집 완료")
    print(git_diff)

    # CLI 옵션 확인
    print(f"[INFO] Model: {args.model}")
    print(f"[INFO] Temperature: {args.temperature}")
    print(f"[INFO] Max Tokens: {args.max_tokens}")
    print(f"[INFO] Safe Mode: {args.safe_mode}")

    if args.command == "commit":
        print("[INFO] 커밋 메시지 생성을 시작합니다.")

    elif args.command == "pr":
        print("[INFO] PR 초안 생성을 시작합니다.")


if __name__ == "__main__":
    main()