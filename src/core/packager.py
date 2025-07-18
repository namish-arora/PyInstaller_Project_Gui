from src.tools.core_libs import *
from src.tools.ui_libs import *


def run_pyinstaller(app_name, entry_file, folder_path, python_exe, mode_file, mode_console, output_text, root, package_button):
    if not app_name or not entry_file or not folder_path or not python_exe:
        messagebox.showerror("Error", "Please fill all fields before running PyInstaller.")
        return

    entry_path = os.path.join(folder_path, entry_file)
    command = [
        python_exe,
        "-m", "PyInstaller",
        "--name", app_name,
        entry_path
    ]

    if mode_file == "onefile":
        command.append("--onefile")
    else:
        command.append("--onedir")

    if mode_console == "console":
        command.append("--console")
    else:
        command.append("--windowed")

    command += [
        "--distpath", os.path.join(folder_path, "dist"),
        "--workpath", os.path.join(folder_path, "build"),
        "--specpath", folder_path,
        "--hidden-import=ansys",
        "--hidden-import=PySide6"
    ]

    try:
        exe_path = os.path.join(folder_path, "dist", app_name + ".exe")
        if os.path.exists(exe_path):
            messagebox.showinfo("Info", f"Executable already exists at:\n{exe_path}\nSkipping packaging.")
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, exe_path)
            return

        progress_bar = ttk.Progressbar(root, length=500, mode='determinate')
        progress_bar.pack(before=package_button, pady=(10, 20))
        progress_bar.start(1000)
        root.update_idletasks()

        subprocess.run(command, check=True)

        output_text.delete("1.0", tk.END)
        dist_path = os.path.join(folder_path, "dist", app_name)
        output_text.insert(tk.END, dist_path)

        progress_bar.stop()
        progress_bar.pack_forget()

        messagebox.showinfo("Success", f"App '{app_name}' packaged successfully! Your app is in the dist folder")

    except subprocess.CalledProcessError as e:
        output_text.delete("1.0", tk.END)
        messagebox.showinfo("Error Occurred")
        output_text.insert(tk.END, f"Packaging failed:\n{e}")
