#!/usr/bin/env python3
"""
gitwrap: Main Interface Definition & Router
Coordinates command line execution workflows by combining git operations and YAML formatting.
"""
import argparse
import sys

# Cross-module custom references
from git_ops import (
    verify_git_repository,
    parse_git_status,
    get_untracked_files_to_clean,
    run_git_command
)
from yaml_output import to_yaml

def handle_clean(args):
    """Executes the custom business logic flow for the clean wrapper command."""
    verify_git_repository()
    files_to_remove = get_untracked_files_to_clean()
    
    # Global Output Setup
    output_data = {}
    output_data["dry_run"] = args.dry_run or None
    output_data["action"] = "clean"
    output_data["favourite_pokemon"] = args.favourite_pokemon
    
    if not files_to_remove:
        if args.dry_run:
            print(to_yaml(output_data))
        else:
            print("Everything is clean. No untracked files to delete.")
        return

    if args.dry_run:
        output_data["files"] = files_to_remove
        print(to_yaml(output_data))
        return

    # Interactive Step: Prompt user if --yes flag isn't provided
    if not args.yes:
        try:
            choice = input(f"This will delete {len(files_to_remove)} untracked files. Continue? [y/N]: ").strip().lower()
            if choice not in ("y", "yes"):
                print("Clean operation aborted by user.")
                sys.exit(0)
        except (KeyboardInterrupt, EOFError):
            print("\nClean operation aborted.")
            sys.exit(1)

    # Execution Step
    code, _, stderr = run_git_command(["clean", "-fd"])
    if code != 0:
        print(f"Error executing git clean: {stderr.strip()}", file=sys.stderr)
        sys.exit(1)
        
    output_data["files"] = files_to_remove
    print(to_yaml(output_data))


def handle_status(args):
    """Executes the custom business logic flow for the status wrapper command."""
    verify_git_repository()
    
    output_data = {}
    output_data["dry_run"] = args.dry_run or None
        
    # Merge status data matrix
    status_matrix = parse_git_status()
    output_data.update(status_matrix)
    output_data["favourite_pokemon"] = args.favourite_pokemon
    
    print(to_yaml(output_data))


def main():
    # Setup global flags shared globally down structural sub-commands
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Outputs what the tool would do instead of altering live state"
    )
    parent_parser.add_argument(
        "--favourite-pokemon", 
        default="Pikachu", 
        help="Optional field included in YAML output (default: Pikachu)"
    )
    main_parser = argparse.ArgumentParser(
        description="gitwrap: A safer, structured interface CLI wrapping common Git commands.",
        parents=[parent_parser]
    )
    subparsers = main_parser.add_subparsers(dest="command", required=True, help="Subcommands")

    # Clean Command Parser Setup
    clean_parser = subparsers.add_parser(
        "clean", 
        parents=[parent_parser],
        help="Safer wrapper wrapping 'git clean -fd'"
    )
    clean_parser.add_argument(
        "--yes", "-y", 
        action="store_true", 
        help="Skip confirmation prompt before destructive execution passes"
    )
    clean_parser.set_defaults(func=handle_clean)

    # Status Command Parser Setup
    status_parser = subparsers.add_parser(
        "status", 
        parents=[parent_parser],
        help="Structured wrapper extracting deterministic YAML from 'git status'"
    )
    status_parser.set_defaults(func=handle_status)

    # Parse and Route Execution Paths
    args = main_parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()