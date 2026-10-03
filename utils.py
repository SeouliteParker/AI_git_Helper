import subprocess
 
 
def run_git(args):
    return subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
 
 
def get_git_status():
    result = run_git(["status", "--short"])
    return result.stdout
 
 
def get_git_diff():
    # staged + unstaged 변경을 모두 가져옴
    result = run_git(["diff", "HEAD"])
 
    if result.returncode == 0:
        return result.stdout
 
    # 첫 커밋 전이라 HEAD가 없으면 staged / unstaged를 따로 합침
    staged = run_git(["diff", "--cached"])
    unstaged = run_git(["diff"])
    return staged.stdout + unstaged.stdout
 
 
def limit_diff(diff_text, max_lines=200):
    lines = diff_text.splitlines()
 
    if len(lines) > max_lines:
        lines = lines[:max_lines]
 
    return "\n".join(lines)
 