import os
import subprocess
import sys



def create_virtual_env(venv_path,folder_path):
    """Create a virtual environment and install required packages."""

    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

    pip_executable = os.path.join(venv_path, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pip")
   
    def find_requirements_txt(start_path): #to find requirements.txt path in parent folder
        current_path = start_path
        while True:
            requirements_path = os.path.join(current_path, "requirements.txt")
            if os.path.exists(requirements_path):
                return requirements_path
            parent_path = os.path.dirname(current_path) #move one step up
            if parent_path == current_path:
                return None
            current_path = parent_path


    def find_parent_folder_path(start_path):
        current_path = start_path
        while True:
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:
                return None
            if os.path.exists(os.path.join(parent_path, "pyproject.toml")):
                return parent_path
            current_path = parent_path



            


    # Usage
    
    requirements_path = find_requirements_txt(folder_path)
    pyproject_path = find_parent_folder_path(folder_path)

    if requirements_path:
        subprocess.run([pip_executable, "install", "-r", requirements_path], check=True)

    elif pyproject_path:
        subprocess.run([pip_executable, "install", pyproject_path], check=True)



    subprocess.run([pip_executable, "install", "pyinstaller"], check=True) # to install pyinstaller in venv

    return os.path.join(venv_path, "Scripts", "pyinstaller.exe") if os.name == "nt" else os.path.join(venv_path, "bin", "pyinstaller")
   
   