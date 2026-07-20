# gitwrap

A lightweight CLI wrapper around common Git commands that adds safety features and produces consistent YAML output.

## Requirements

* Python 3.10+
* Git installed and available in your `PATH`
* PyYAML

Install the only dependency:

```bash
pip install pyyaml
```

Or:

```bash
pip install -r requirements.txt
```

## Usage

Display repository status as YAML:

```bash
python gitwrap.py status
```

Preview the command without making changes:

```bash
python gitwrap.py status --dry-run
```

Specify your favourite Pokémon:

```bash
python gitwrap.py status --favourite-pokemon Charizard
```

Clean untracked files safely:

```bash
python gitwrap.py clean
```

Skip the confirmation prompt:

```bash
python gitwrap.py clean --yes
```

Preview which files would be removed:

```bash
python gitwrap.py clean --dry-run
```

## Features

### `status`

* Uses `git status --porcelain=v2 --branch`
* Produces machine-readable YAML
* Reports:

  * current branch
  * staged files
  * unstaged files
  * untracked files
* Omits empty file lists for brevity

Example output:

```yaml
action: status
branch: main
staged_files:
- src/app.py
unstaged_files:
- README.md
untracked_files:
- notes.txt
favourite_pokemon: Pikachu
```

### `clean`

* Uses `git clean -fd`
* Calculates the files that would be removed using `git clean -fdn`
* Prompts for confirmation before deleting files
* Supports `--yes` to skip confirmation
* Supports `--dry-run` to preview the files that would be deleted

Example:

```yaml
dry_run: true
action: clean
files:
- build/output.log
- tmp/cache.txt
favourite_pokemon: Pikachu
```

## Project Structure

```
gitwrap.py        # CLI entry point and command routing
git_ops.py        # Git command execution and parsing
yaml_output.py    # YAML serialization helper
test_gitwrap.py   # Basic unit tests
```

## Running Tests

Execute the unit tests with:

```bash
python test_gitwrap.py
```

## Design Notes

The implementation separates responsibilities into three modules:

* **gitwrap.py** handles argument parsing and command routing.
* **git_ops.py** encapsulates all Git subprocess interactions and parsing logic.
* **yaml_output.py** formats output consistently using PyYAML.

This separation keeps Git interaction, presentation, and CLI logic independent and easier to maintain or extend.
