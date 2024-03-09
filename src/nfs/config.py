import os
from pathlib import Path

user_folder = Path(os.path.expanduser("~"))
CONFIG_FOLDER = user_folder / ".nfs"
CONFIG_FOLDER.mkdir(exist_ok=True)

SERVER_PORT = 12000