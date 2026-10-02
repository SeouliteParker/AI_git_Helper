import subprocess


def get_git_status():
    result = subprocess.run(
        ["git", "status", "--short"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return result.stdout


def get_git_diff():
    result = subprocess.run(
        ["git", "diff"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )

    return result.stdout

def limit_diff(diff_text, max_lines=200):
    lines = diff_text.splitlines()

    if len(lines) > max_lines:
        lines = lines[:max_lines]

    return "\n".join(lines)