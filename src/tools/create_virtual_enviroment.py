from src.tools.core_libs import *
from src.tools.ui_libs import *


def create_virtual_env(venv_path,folder_path):
    """Create a virtual environment and install required packages."""

    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    pip_executable = os.path.join(venv_path, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")
    requirements_path = os.path.join(os.path.dirname(folder_path), "requirements.txt") # the folder path is also including src folder but the txt is in the parent folder
    pyproject_path = os.path.dirname(folder_path) #pip cannot directly install toml file, so point it to the parent folder and it will itself find it

    if(os.path.exists(requirements_path)):
        subprocess.run([pip_executable, "install", "-r", requirements_path], check=True)

    if(os.path.exists(pyproject_path)):
        subprocess.run([pip_executable, "install", pyproject_path], check=True)




    

    subprocess.run([pip_executable, "install", "pyinstaller"], check=True) # to install pyinstaller

    return os.path.join(venv_path, "Scripts", "pyinstaller.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pyinstaller")
   
   