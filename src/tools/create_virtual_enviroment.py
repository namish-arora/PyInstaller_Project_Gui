from src.tools.core_libs import *
from src.tools.ui_libs import *


def create_virtual_env(venv_path, requirements_path):
    """Create a virtual environment and install required packages."""

    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    pip_executable = os.path.join(venv_path, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")
    if os.path.exists(requirements_path):
            subprocess.run([pip_executable, "install", "-r", requirements_path], check=True) # to install required dependencies

    subprocess.run([pip_executable, "install", "pyinstaller"], check=True) # to install pyinstaller

    return os.path.join(venv_path, "Scripts", "pyinstaller.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pyinstaller")
   
   