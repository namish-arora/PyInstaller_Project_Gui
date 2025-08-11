import os
import tkinter as tk
import subprocess
import threading
from tkinter import messagebox, ttk, Label


# from src.utils.image_loader import load_image
# from src.tools.create_virtual_enviroment import create_virtual_env


from ..utils.image_loader import load_image
from ..tools.create_virtual_enviroment import create_virtual_env






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
                    output_text, root, package_button, output_frame, output_label_ref, scrollbar):
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

    exe_path = os.path.join(dist_path, app_name + ".exe")

    if os.path.exists(exe_path):
        messagebox.showinfo("Info", f"Executable already exists at:\n{exe_path}\nSkipping packaging.")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, exe_path)
        return

    progress_bar = ttk.Progressbar(root, length=500, mode='determinate')
    progress_bar.pack(before=package_button, pady=(10, 20))
    progress_bar.start(1000)
    root.update_idletasks()

    def task():
        try:
           
            pyinstaller_executable = create_virtual_env(venv_path,folder_path) #created the venv

            frozen_spec_path = find_frozen_path(folder_path)
            user_project_path = os.path.dirname(frozen_spec_path) if frozen_spec_path else None



            # print("python exectable path:", pyinstaller_executable) #showing for venv python scripts path

            # command = [
            #     pyinstaller_executable,
            #     "--name", app_name,
            #     entry_path,
            #     "--distpath", dist_path,
            #     "--workpath", build_path,
            #     "--specpath", spec_path,
            # ]
          
            # command.append("--onefile" if mode_file == "onefile" else "--onedir")
            # command.append("--console" if mode_console == "console" else "--windowed")


            # Get site-packages path 
            site_packages_path = os.path.join(venv_path, "Lib", "site-packages")
            # print(f"Using site-packages path: {site_packages_path}")

            # Collect Ansys/GRANTA packages
            included_packages = [
                pkg for pkg in os.listdir(site_packages_path)
                if pkg.startswith("ansys") or pkg.startswith("GRANTA")
            ]

            # Prepare data files to include
            data_files = [(os.path.join(site_packages_path, pkg), pkg) for pkg in included_packages]

                    
       
               
  
            # Build --add-data arguments
            sep = ';' if os.name == 'nt' else ':'
            add_data_args = []
            for src, dest in data_files:
                add_data_args.extend(['--add-data', f'{src}{sep}{dest}'])

            #check for frozen.spec file and if it is then directly run the command

            print("the frozen spec path is:", frozen_spec_path)

            if frozen_spec_path:
                # Use the pyinstaller from venv and the full path to the spec file
                                
                # Path to the Ansys Python Manager repo
                #ansys_manager_path = r"C:\Users\narora\OneDrive - ANSYS, Inc\Desktop\ansys_python_manager_demo\python-installer-qt-gui"
                

                # Change working directory to where frozen.spec is
                os.chdir(user_project_path)

                # Run PyInstaller using the spec file
                subprocess.run(["pyinstaller", "frozen.spec"], check=True) 
                #subprocess.run([pyinstaller_executable,"frozen.spec"], check=True) 



            
            else:
                
            # Build the PyInstaller command
                command = [
                    pyinstaller_executable,
                    "--name", app_name,
                    entry_path,
                    "--distpath", dist_path,
                    "--workpath", build_path,
                    "--specpath", spec_path, #path to parent folder not venv
                    "--path", site_packages_path,
                    "--onefile" if mode_file == "onefile" else "--onedir",
                    "--console" if mode_console == "console" else "--windowed",
                ] + add_data_args

                
                
            

            

                subprocess.run(command, check=True) #run the command




            def on_success():
                progress_bar.stop()
                progress_bar.pack_forget()
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, exe_path)

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

                messagebox.showinfo("Success", f"App '{app_name}' packaged successfully! Your app is in the venv/dist folder")

            root.after(0, on_success)

        except subprocess.CalledProcessError as e:
            def on_error():
                progress_bar.stop()
                progress_bar.pack_forget()
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

 


