import os
import tkinter as tk


def create_folder_preview_with_display(root, folder_path_var):
    preview_label = tk.Label(root, text="Project Folder Contents:", font=("Aerial", 12))
    preview_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

    text_frame = tk.Frame(root, height=200, width=500)
    text_frame.pack(padx=20, pady=5)

    text_widget = tk.Text(text_frame, wrap="word", height=7, width=60)

    scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)

    text_widget.config(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=tk.RIGHT,fill = tk.Y)
    text_widget.pack(side=tk.LEFT)

    

    def get_project_root_path(folder_path):

    # Traverse up until we find a folder that contains typical project filesimport
        while folder_path:
            parent = os.path.dirname(folder_path)
            if any(f in os.listdir(folder_path) for f in ['requirements.txt', 'setup.py', 'pyproject.toml', '.git', 'README.md']):
                return folder_path
            if parent == folder_path:  # Reached root
                break
            folder_path = parent
        return folder_path  # Fallback to current folder


    # Function to update preview
    def update_folder_preview(*args):
        folder = get_project_root_path(folder_path_var.get())
        text_widget.delete("1.0", tk.END)
        if folder and os.path.isdir(folder):
            for root_dir, dirs, files in os.walk(folder):
                level = root_dir.replace(folder, '').count(os.sep)
                indent = ' ' * 4 * level
                text_widget.insert(tk.END, f"{indent}📁 {os.path.basename(root_dir)}\n")
                sub_indent = ' ' * 4 * (level + 1)
                for f in files:
                    text_widget.insert(tk.END, f"{sub_indent}📄 {f}\n")

    # Trigger preview update when folder is selected
    folder_path_var.trace_add("write", update_folder_preview)