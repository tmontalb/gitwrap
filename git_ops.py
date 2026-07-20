"""
Git Operation & Subprocess Integration Layer
Handles direct OS shell interactions and porcelain command output transformations.
"""
import subprocess
import sys

def run_git_command(args: list[str]) -> tuple[int, str, str]:
    """Executes a git command and returns (return_code, stdout, stderr)."""
    try:
        # Explicitly decode using 'replace' to prevent crashing on invalid UTF-8 files
        res = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        return res.returncode, res.stdout, res.stderr
    except FileNotFoundError:
        print("Error: 'git' binary not found. Please ensure Git is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

def verify_git_repository():
    """Validates that the current working directory is inside a valid git repository."""
    code, _, _ = run_git_command(["rev-parse", "--is-inside-work-tree"])
    if code != 0:
        print("Error: Not a git repository (or any of the parent directories).", file=sys.stderr)
        sys.exit(1)

def parse_git_status() -> dict:
    """Parses `git status --porcelain=v2 --branch` to segment files consistently."""
    code, stdout, stderr = run_git_command(["status", "--porcelain=v2", "--branch"])
    if code != 0:
        print(f"Error checking git status: {stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    branch = "HEAD (Detached)"
    staged = []
    unstaged = []
    untracked = []

    for line in stdout.splitlines():
        if not line:
            continue
        
        # Branch header lines
        if line.startswith("# branch.head "):
            branch = line.split(" ", 2)[2].strip()
            continue
        
        parts = line.split(" ")
        # Tracked files (modified, added, deleted, etc.)
        if parts[0] in ("1", "2"):  # 1: normal tracked changes, 2: renames/copies
            xy = parts[1]
            staged_char, unstaged_char = xy[0], xy[1]
            path = parts[-1] 
            
            if staged_char != ".":
                staged.append(path)
            if unstaged_char != ".":
                unstaged.append(path)
                
        # Untracked files
        elif parts[0] == "?":
            path = line.split(" ", 1)[1].strip()
            untracked.append(path)

    result = {"action": "status", "branch": branch}
    if staged:    result["staged_files"] = staged
    if unstaged:  result["unstaged_files"] = unstaged
    if untracked: result["untracked_files"] = untracked
    return result

def get_untracked_files_to_clean() -> list[str]:
    """Discovers what untracked files `git clean -fd` would delete using native dry-run."""
    code, stdout, stderr = run_git_command(["clean", "-fdn"])
    if code != 0:
        print(f"Error calculating clean footprint: {stderr.strip()}", file=sys.stderr)
        sys.exit(1)
        
    files = []
    for line in stdout.splitlines():
        if line.startswith("Would remove "):
            path = line.replace("Would remove ", "").strip()
            files.append(path)
    return files