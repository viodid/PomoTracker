from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# https://stackoverflow.com/a/46237916/17260275
file = open(BASE_DIR / "version.txt", "r", encoding="utf-8")
version = file.read().split('-')

__version__ = version[0] + '.' + version[1]

print(__version__)
