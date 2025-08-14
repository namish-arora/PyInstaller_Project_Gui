# import os
# import tkinter as tk


# def create_folder_preview_with_display(root, folder_path_var):
#     preview_label = tk.Label(root, text="Project Folder Contents:", font=("Aerial", 12))
#     preview_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

#     text_frame = tk.Frame(root, height=200, width=500)
#     text_frame.pack(padx=20, pady=5)

#     text_widget = tk.Text(text_frame, wrap="word", height=10, width=65)

#     scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)

#     text_widget.config(yscrollcommand=scrollbar.set)

#     scrollbar.pack(side=tk.RIGHT,fill = tk.Y)
#     text_widget.pack(side=tk.LEFT)

    

#     def get_project_root_path(folder_path):

#     # Traverse up until we find a folder that contains typical project filesimport
#         while folder_path:
#             parent = os.path.dirname(folder_path)
#             if any(f in os.listdir(folder_path) for f in ['requirements.txt', 'setup.py', 'pyproject.toml', '.git', 'README.md']):
#                 return folder_path
#             if parent == folder_path:  # Reached root
#                 break
#             folder_path = parent
#         return folder_path  # Fallback to current folder




#     def update_folder_preview(*args):
#         folder = get_project_root_path(folder_path_var.get())
#         text_widget.delete("1.0", tk.END)

#         if folder and os.path.isdir(folder):
#             for root_dir, dirs, _ in os.walk(folder):
#                 level = root_dir.replace(folder, '').count(os.sep)
#                 indent = '│   ' * level
#                 branch = '├── ' if level > 0 else ''
#                 text_widget.insert(tk.END, f"{indent}{branch}📁 {os.path.basename(root_dir)}\n")


#     # Trigger preview update when folder is selected
#     folder_path_var.trace_add("write", update_folder_preview)


# # import os
# # import tkinter as tk

# # def create_folder_preview_with_display(root, folder_path_var):
# #     preview_label = tk.Label(root, text="Project Folder Contents:", font=("Arial", 12))
# #     preview_label.pack(anchor=tk.W, padx=20, pady=(10, 0))

# #     text_frame = tk.Frame(root, height=200, width=500)
# #     text_frame.pack(padx=20, pady=5)

# #     text_widget = tk.Text(text_frame, wrap="word", height=12, width=60)
# #     scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
# #     text_widget.config(yscrollcommand=scrollbar.set)

# #     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# #     text_widget.pack(side=tk.LEFT)

# #     # Define color-coded tags
# #     text_widget.tag_config("level0", foreground="blue", font=("Arial", 10, "bold"))
# #     text_widget.tag_config("level1", foreground="darkgreen", font=("Arial", 10))
# #     text_widget.tag_config("level2", foreground="purple", font=("Arial", 10))
# #     text_widget.tag_config("level3", foreground="brown", font=("Arial", 10))
# #     text_widget.tag_config("special", foreground="red", font=("Arial", 10, "italic"))

# #     def get_project_root_path(folder_path):
# #         while folder_path:
# #             parent = os.path.dirname(folder_path)
# #             if any(f in os.listdir(folder_path) for f in ['requirements.txt', 'setup.py', 'pyproject.toml', '.git', 'README.md']):
# #                 return folder_path
# #             if parent == folder_path:
# #                 break
# #             folder_path = parent
# #         return folder_path

# #     def update_folder_preview(*args):
# #         folder = get_project_root_path(folder_path_var.get())
# #         text_widget.delete("1.0", tk.END)

# #         # Define folders to exclude
# #         excluded_folders = {'.git', 'venv', '__pycache__', '.idea', '.vscode', '.mypy_cache', '.pytest_cache'}

# #         if folder and os.path.isdir(folder):
# #             for root_dir, dirs, _ in os.walk(folder):
# #                 folder_name = os.path.basename(root_dir)
# #                 if folder_name in excluded_folders:
# #                     continue  # Skip unimportant folders

# #                 level = root_dir.replace(folder, '').count(os.sep)
# #                 indent = '│   ' * level
# #                 branch = '├── ' if level > 0 else ''

# #                 # Choose tag based on folder type
# #                 tag = f"level{min(level, 3)}"
# #                 text_widget.insert(tk.END, f"{indent}{branch}📁 {folder_name}\n", tag)


#     folder_path_var.trace_add("write", update_folder_preview)


import os
import tkinter as tk
from tkinter import ttk

def create_folder_preview_with_display(root, folder_path_var):
    preview_label = tk.Label(root, text="Project Folder Contents:", font=("Arial", 12))
    preview_label.pack(anchor=tk.W, padx=15, pady=(10, 0))


    tree_frame = tk.Frame(root, height=150, width=500)
    tree_frame.pack_propagate(False)  # Prevents auto-resizing
    
    tree_frame.pack(padx=10, pady=5)


    tree = ttk.Treeview(tree_frame)
    tree.pack(side=tk.LEFT, fill=tk.X, expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # Define folders to exclude
    excluded_folders = {'.git', 'venv', '__pycache__', '.idea', '.vscode', '.mypy_cache', '.pytest_cache'}

    def get_project_root_path(folder_path):
        while folder_path:
            parent = os.path.dirname(folder_path)
            if any(f in os.listdir(folder_path) for f in ['requirements.txt', 'setup.py', 'pyproject.toml', '.git', 'README.md']):
                return folder_path
            if parent == folder_path:
                break
            folder_path = parent
        return folder_path

    def insert_folders(parent_id, path):
        try:
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path) and item not in excluded_folders:
                    folder_id = tree.insert(parent_id, "end", text=f"📁 {item}", open=False)
                    insert_folders(folder_id, item_path)
        except Exception as e:
            tree.insert(parent_id, "end", text=f"[Error reading folder: {e}]")

    def update_folder_preview(*args):
        folder = get_project_root_path(folder_path_var.get())
        tree.delete(*tree.get_children())

        if folder and os.path.isdir(folder):
            root_id = tree.insert("", "end", text=f"📁 {os.path.basename(folder)}", open=True)
            insert_folders(root_id, folder)

    folder_path_var.trace_add("write", update_folder_preview)

