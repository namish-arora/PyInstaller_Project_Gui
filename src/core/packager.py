from click import command
from src.tools.core_libs import *
from src.tools.ui_libs import *
from src.utils.image_loader import load_image
from src.tools.create_virtual_enviroment import create_virtual_env




def run_pyinstaller(app_name, entry_file, folder_path, python_exe, mode_file, mode_console,
                    output_text, root, package_button, output_frame, output_label_ref, scrollbar):
    if not app_name or not entry_file or not folder_path:
        messagebox.showerror("Error", "Please fill all fields before running PyInstaller.")
        return

    entry_path = os.path.join(folder_path, entry_file)
    venv_path = os.path.join(folder_path, "venv")
    # requirements_path = os.path.join(folder_path, "requirements.txt")
    # pyproject_path = os.path.join(folder_path,"pyproject.toml")

    dist_path = os.path.join(venv_path, "dist")
    build_path = os.path.join(venv_path, "build")
    spec_path = venv_path
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
           
            pyinstaller_executable = create_virtual_env(venv_path,folder_path)
          

            command = [
                pyinstaller_executable,
                "--name", app_name,
                entry_path,
                "--distpath", dist_path,
                "--workpath", build_path,
                "--specpath", spec_path,
                "--hidden-import=ansys",
                "--hidden-import=PySide6",
                "--hidden-import=requests",
               
                
            ]

            command.append("--onefile" if mode_file == "onefile" else "--onedir")
            command.append("--console" if mode_console == "console" else "--windowed")

            
    


            subprocess.run(command, check=True)

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


