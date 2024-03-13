import os
from pathlib import Path
import platform

def is_running_on_wsl():
    return platform.system() == 'Linux' and "microsoft" in platform.uname().release.lower()


WSL_HOST: bool = is_running_on_wsl()
user_folder = Path(os.path.expanduser("~"))
CONFIG_FOLDER = user_folder / ".nfs"
CONFIG_FOLDER.mkdir(exist_ok=True)

SERVER_PORT = 12000