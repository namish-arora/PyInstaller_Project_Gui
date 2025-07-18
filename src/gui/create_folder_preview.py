from src.tools.core_libs import *
from src.tools.ui_libs import *



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

    # Function to update preview
    def update_folder_preview(*args):
        folder = folder_path_var.get()
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