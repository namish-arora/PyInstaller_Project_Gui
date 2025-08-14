import os
import tkinter as tk
import subprocess
import threading
from tkinter import messagebox, ttk, Label
import sys    
import getpass
import shutil


from ..utils.image_loader import load_image
from ..tools.create_virtual_enviroment import create_virtual_env


def open_folder(folder_path):
    """Open the specified folder in the file explorer."""
    if sys.platform == "win32":
        os.startfile(folder_path)


#move the venv to app data
def move_venv_to_local(venv_path,app_name):
    user_machine_name = getpass.getuser()
    target_path=  os.path.join("C:/Users",user_machine_name,"AppData","Local","ansys_venv")
    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    shutil.move(venv_path,target_path)
    print("venv moved successfully...")

    # want to return the path to the .exe created in the dist folder of venv
    execution_formed_path = os.path.join(target_path,"dist",app_name + ".exe")

    return execution_formed_path


def get_parent_folder_path(start_path):
    """Find the parent folder path containing 'pyproject.toml'."""
    current_path = start_path
    while True:
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            return None
        if os.path.exists(os.path.join(parent_path, "pyproject.toml")) or os.path.exists(os.path.join(parent_path,"requirements.txt")):
            return parent_path
        current_path = parent_path


def find_frozen_path(start_path):
    current_path = start_path
    while True:
        frozen_path = os.path.join(current_path,"frozen.spec")
        if os.path.exists(frozen_path):
            return frozen_path
        parent_path = os.path.dirname(current_path) # move one step up in tree
        if parent_path == current_path:
            return None
        
        current_path = parent_path



def run_pyinstaller(app_name, entry_file, folder_path, python_exe, mode_file, mode_console,
                    output_text, root, package_button, output_frame, output_label_ref, scrollbar, final_venv_path):
    
    if not app_name or not entry_file or not folder_path or not python_exe:
        messagebox.showerror("Error", "Please fill all fields before running PyInstaller.")
        return

    entry_path = os.path.join(folder_path, entry_file)
    venv_path = os.path.join(folder_path, "venv")




    dist_path = os.path.join(venv_path, "dist")
    build_path = os.path.join(venv_path, "build")
    # spec_path = venv_path
    parent_path = get_parent_folder_path(folder_path)
    spec_path = parent_path 

    if spec_path is None:
        spec_path = venv_path

    # Determine where the venv will be after moving
    user_machine_name = getpass.getuser()
    target_venv_path = os.path.join("C:/Users", user_machine_name, "AppData", "Local", "ansys_venv")
    exe_path = os.path.join(target_venv_path, "dist", app_name + ".exe")

    # Logic for skip packaging
    if os.path.exists(exe_path):
        messagebox.showinfo("Info", f"Executable already exists at:\n{exe_path}\nSkipping packaging.")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, exe_path)
        return

    #logic for skip packaging
    if os.path.exists(exe_path):
        messagebox.showinfo("Info", f"Executable already exists at:\n{exe_path}\nSkipping packaging.")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, exe_path)
        return

    progress_bar = ttk.Progressbar(root, length=500, mode='indeterminate')
    progress_bar.pack(before=package_button, pady=(10, 20))
    progress_bar.start(1000)
    root.update_idletasks()

    def task():
        try:
           
            pyinstaller_executable = create_virtual_env(venv_path,folder_path) #created the venv

            frozen_spec_path = find_frozen_path(folder_path)
            user_project_path = os.path.dirname(frozen_spec_path) if frozen_spec_path else None



            # Get site-packages path 
            site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
            # print(f"Using site-packages path: {site_packages_path}")

            # # Collect Ansys/GRANTA packages
            # included_packages = [
            #     pkg for pkg in os.listdir(site_packages_path)
            #     if pkg.startswith("ansys") or pkg.startswith("GRANTA")
            # ]

            # # Prepare data files to include
            # data_files = [(os.path.join(site_packages_path, pkg), pkg) for pkg in included_packages]

  
            # # Build --add-data arguments
            # sep = ';' if os.name == 'nt' else ':'
            # add_data_args = []
            # for src, dest in data_files:
            #     add_data_args.extend(['--add-data', f'{src}{sep}{dest}'])

            #check for frozen.spec file and if it is then directly run the command

            print("the frozen spec path is:", frozen_spec_path)

            if frozen_spec_path:

                # Change working directory to where frozen.spec is
                os.chdir(user_project_path)

                # Run PyInstaller using the spec file
                # subprocess.run(["pyinstaller", "frozen.spec"], check=True) 
                subprocess.run([pyinstaller_executable,"frozen.spec"], check=True) 



                # #run the file with uv    it is creating its own .venv
                # subprocess.run([
                #     "uv","run","pyinstaller", "frozen.spec",
                #     "--python", str(pyinstaller_executable)
                # ], check=True)
                
            # Build the PyInstaller command

            else:
              
                # # Add --add-data for PySide6 plugins
                # sep = ';' if os.name == 'nt' else ':'
                # pyside6_plugins = os.path.join(site_packages_path, 'PySide6', 'plugins')
                # add_data_args = []
                # if os.path.exists(pyside6_plugins):
                #     add_data_args.extend(['--add-data', f'{pyside6_plugins}{sep}PySide6/plugins'])

                
                print("pyinstaller_executable:", pyinstaller_executable)
                print("app_name:", app_name)
                print("entry_path:", entry_path)
                print("dist_path:", dist_path)
                print("build_path:", build_path)
                print("spec_path:", spec_path)


                command = [
                    pyinstaller_executable,
                    "--name", app_name,
                    entry_path,
                    "--distpath", dist_path,
                    "--workpath", build_path,
                    "--specpath", spec_path,
                    "--onefile" if mode_file == "onefile" else "--onedir",
                    "--console" if mode_console == "console" else "--windowed",
                    # *add_data_args
                ]


                subprocess.run(command, check=True) #run the command




            def on_success():
                progress_bar.stop()
                progress_bar.pack_forget()

                final_venv_path = move_venv_to_local(venv_path,app_name)
                exe_path = os.path.join(final_venv_path, "dist", app_name + ".exe")
                print(f"***Final venv path***: {final_venv_path}")

                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, final_venv_path)

                if output_label_ref[0] is None:
                    output_frame.pack(before=package_button, anchor=tk.W, padx=20, pady=(10, 0))
                    output_label_ref[0] = tk.Label(output_frame, text="Output:", font=("Arial", 12))
                    output_label_ref[0].pack(side=tk.LEFT, padx=(0, 10))
                    folder_image = load_image("folder_icon.png", (20, 20))
                    folder_icon_label = Label(output_frame, image=folder_image)
                    folder_icon_label.image = folder_image
                    folder_icon_label.pack(side=tk.LEFT, padx=(0, 10))
                    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
                    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                    output_frame_for_open = tk.Frame(root)
                    output_frame_for_open.pack(before=package_button,padx=20,pady=5)

                    open_folder_button = tk.Button(output_frame_for_open,text="Open Folder",fg="white",bg="deepskyblue3",width=40,font=("Aerial", 12),command=lambda: open_folder(os.path.dirname(final_venv_path)))
                    open_folder_button.pack(pady=(10,10))
                    
                  

                messagebox.showinfo("Success", f"App '{app_name}' packaged successfully! Your app is in the venv/dist folder")

            root.after(0, on_success)

        except subprocess.CalledProcessError as e:
            def on_error():
                progress_bar.stop()
                progress_bar.pack_forget()

                final_venv_path = move_venv_to_local(venv_path,app_name)
                print(f"***Final venv path***: {final_venv_path}")

                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, f"Packaging failed:\n")

                if output_label_ref[0] is None:
                    output_frame.pack(before=package_button, anchor=tk.W, padx=20, pady=(10, 0))
                    output_label_ref[0] = tk.Label(output_frame, text="Output:", font=("Arial", 12))
                    output_label_ref[0].pack(side=tk.LEFT, padx=(0, 10))
                    folder_image = load_image("folder_icon.png", (20, 20))
                    folder_icon_label = Label(output_frame, image=folder_image)
                    folder_icon_label.image = folder_image
                    folder_icon_label.pack(side=tk.LEFT, padx=(0, 10))
                    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
                    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                messagebox.showinfo("Error Occurred", "Packaging failed.")

            root.after(0, on_error)

    threading.Thread(target=task).start()

 


