import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# https://stackoverflow.com/a/46237916/17260275
__version__ = subprocess.check_output(["git", "describe", "--tags", "--always"],
                                      cwd=BASE_DIR).decode('UTF-8').strip()
__build__ = ''

print('here', __version__, __build__)
