import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# https://stackoverflow.com/a/46237916/17260275
try:
    version = subprocess.check_output(["git", "describe", "--tags", "--always"],
                                      cwd=BASE_DIR).decode('UTF-8').strip()
    version = version.split('-')

    __version__ = version[0] + '.' + version[1]
except:
    __version__ = '1.2.4'

print(__version__)
