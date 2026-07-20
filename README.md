# gitwrap 🛠️

A safer, structured interface CLI that wraps common Git operations, converting standard stream text outputs into clean, machine-readable YAML structures. `gitwrap` provides human safety filters alongside deterministic output formats ideal for automation scripts, CI/CD pipelines, or daily development workflows.

## Features

- 🔹 **Deterministic YAML Output:** Replaces complex text parsing scripts by outputting native structural layout blocks completely natively without external dependencies.
- 🔹 **Enhanced Safety Guards:** Prompts for confirmation on destructive operations (`clean`), preventing accidental file deletions unless explicitly bypassed.
- 🔹 **Flexible Flag Routing:** Intelligently captures global flags (`--dry-run`, `--favourite-pokemon`) whether they are passed before or after subcommands.
- 🔹 **Modular & Decoupled Architecture:** Cleanly isolates process execution, data serialization, and CLI parameter routing across separate modules.

---

## Repository Structure & Architecture Overview

The tool is structurally divided into three cohesive Python modules designed to run with zero third-party framework dependencies:

```
                  ┌────────────────────────┐
                  │      gitwrap.py        │
                  │  (CLI Router & Main)   │
                  └───────────┬────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
    ┌────────────────────┐        ┌────────────────────┐
    │    git_ops.py      │        │   yaml_output.py   │
    │ (Git Subprocesses) │        │  (YAML Serializer) │
    └────────────────────┘        └────────────────────┘
```

1. **`gitwrap.py` (Interface & Router):** Manages terminal `argparse` configurations, handles global and subcommand flag resolution, and orchestrates execution workflows for `status` and `clean`.
2. **`git_ops.py` (Git Integration Layer):** Coordinates execution out to the system shell using Python's `subprocess` pipeline, handling string decoding hazards, Git status parsing (`porcelain=v2`), and clean footprint calculations.
3. **`yaml_output.py` (YAML Serialization Engine):** Standalone, dependency-free state machine translating data dictionaries containing collections and booleans directly into pure YAML-compliant formats.

---

## Installation & Setup

Ensure you have **Python 3.7+** and **Git** installed and available in your system path environment variables.

1. Clone or copy the script files into your preferred local utility directory:
   ```bash
   cp gitwrap.py git_ops.py yaml_output.py /usr/local/bin/
   chmod +x /usr/local/bin/gitwrap.py
   ```
2. Verify structural capability using the isolated testing harness:
   ```bash
   python test_gitwrap.py
   ```

---

## Detailed Command Reference

### 1. `gitwrap status`
Extracts staging layer differentials using Git's porcelain processing metrics. It automatically groups files based on execution status matrices while scrubbing empty tracking lines out of sight.

**Execution Variations:**
```bash
python gitwrap.py status
python gitwrap.py status --favourite-pokemon Gengar
python gitwrap.py --dry-run status
```

**Sample Serialization Output:**
```yaml
action: status
branch: main
staged_files:
  - src/app.js
unstaged_files:
  - README.md
untracked_files:
  - temp.txt
favourite_pokemon: Gengar
```

### 2. `gitwrap clean`
Previews or destroys untracked files safely. Requires direct user input validation before executing system sweeps unless intentionally overridden.

**Dry-Run Evaluation Preview:**
```bash
python gitwrap.py clean --dry-run
python gitwrap.py --dry-run clean
```
*Output:*
```yaml
dry_run: true
action: clean
favourite_pokemon: Pikachu
files:
  - notes.md
  - temp.txt
```

**Interactive Destructive Mode:**
```bash
python gitwrap.py clean
```
*Console Prompt interaction:*
```text
This will delete 2 untracked files. Continue? [y/N]: n
Clean operation aborted by user.
```

**Forced Automation Bypass:**
```bash
python gitwrap.py clean --yes
```

---

## Development & Extension Guidelines

### Testing Isolation
The companion test module `test_gitwrap.py` imports directly from `yaml_output.py` to perform decoupled logic verification. Because it focuses heavily on data matrix serialization mapping, **it does not require a local Git repository state context to be present**:

```bash
python test_gitwrap.py
```

### Formatting Serialization Logic Rules
If extending the dictionary generation fields, the custom serialization engine (`yaml_output.py`) automatically enforces the following formatting principles:
- **Null Scrubbing:** Any key mapped to a `None` value is dynamically skipped.
- **Empty Array Avoidance:** If a collection contains no elements, it is dropped entirely instead of generating an empty key header.
- **String Encapsulation Guards:** Strings holding dangerous syntax indicators (`:`, `#`, `[`, `]`, `{`, `}`) are safely escaped in wrapped quotes.