import sys
from pathlib import Path
from importlib import import_module

# ensure project root (parent of the `game` package) is on sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    package = Path(__file__).resolve().parent.name  # typically `game`
    play = import_module(".play", package=package).play  # import as package module
    play()
