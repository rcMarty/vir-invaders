# Student Research Project — Space Invaders + Research Components

## Overview
This repository contains a simple Pygame-based Space Invaders student project alongside experimental research code related to file analysis and an offline LLM integration. The project is for research and educational purposes only.

## Important Safety Notice
- The repository includes a folder `malware/` with experimental code that demonstrates concepts related to file analysis and encryption.  
- **Do not run any code in `malware/` on your primary machine or on a production network.**  
- If you want to inspect or test those components, use an isolated virtual machine or container with no network connectivity and proper backups.
- The author is responsible for following legal and ethical guidelines when using or testing the research components.

## Project Structure
- `main.py` — project entry point (runs the safe game part).
- `game/` — Pygame implementation of Space Invaders.
- `malware/` — research experiments; contains LLM integration and an encryption/backupper prototype (do not run).
- `space_invaders.spec` — PyInstaller spec for building a bundle (includes both game and research files).
- `readme.md` — this file.

## Requirements
- Python 3.11+ recommended.
- For the game: `pygame`.
- For research components (optional, do not install unless you will run them in a safe environment): `openai` (or local LLM client), `pyserde`, `cryptography`, `requests`.

## Install (safe steps for game)
1. Create and activate a virtual environment:
   - `python -m venv .venv`
   - `source .venv/bin/activate` (Linux / macOS)
2. Install minimal dependency for the game:
   - `pip install pygame`
3. Run the game from project root:
   - `python main.py`

## Do NOT run (unless isolated)
- Files under `malware/` (for example, `malware/ransomware.py`) are intentionally sensitive. Do not execute them on any system with real user data.
- If evaluating the LLM-based scanner, prefer reviewing the code statically or running tests inside a disposable VM without network access to external resources.

## Development / Building
- A PyInstaller spec is provided as `space_invaders.spec`. It currently includes `game/` and `malware/` in `datas`. Remove `malware/` from `datas` and `hiddenimports` before building a public executable.
- To build a safe game-only executable, edit `space_invaders.spec` and exclude `malware` entries.

## Research Notes
- This is a student research repository. Any experiments involving encryption, data exfiltration, or automated file analysis were created for study — they may be incomplete and are provided without warranty.
- Always follow institutional review board (IRB), legal, and ethical requirements when conducting tests.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.