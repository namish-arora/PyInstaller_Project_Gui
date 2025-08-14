import tkinter as tk
import threading




# from src.gui.header import load_header_with_label
# from src.gui.app_name_input import create_app_name_input
# from src.gui.create_folder_selector import create_folder_selector_with_display
# from src.gui.create_entry_point_selector import create_entry_point_selector_with_display
# from src.gui.create_python_exe_selector import create_python_exe_selector_with_display
# from src.gui.create_folder_preview import create_folder_preview_with_display
# from src.gui.create_mode_selectors import create_mode_selectors_with_display
# from src.gui.create_command_preview import create_command_preview_with_display
# from src.utils.image_loader import load_image
# from src.core.packager import run_pyinstaller

from ..gui.header import load_header_with_label
from ..gui.app_name_input import create_app_name_input
from ..gui.create_folder_selector import create_folder_selector_with_display
from ..gui.create_entry_point_selector import create_entry_point_selector_with_display
from ..gui.create_python_exe_selector import create_python_exe_selector_with_display
from ..gui.create_folder_preview import create_folder_preview_with_display
from ..gui.create_mode_selectors import create_mode_selectors_with_display
from ..gui.create_command_preview import create_command_preview_with_display
from ..utils.image_loader import load_image
from ..core.packager import run_pyinstaller



output_label = None




def launch_gui():
    root = tk.Tk()
    root.title("PyInstaller GUI")
    root.geometry("600x980")

    # Load and set window icon
    icon_image = load_image("ansys_logo_2.jpg", (32, 32))
    root.iconphoto(False, icon_image)
    root.icon_image = icon_image  # Prevent garbage collection

    root.resizable(False, False)  # Disable resizing


  
    load_header_with_label(root)  # Load header with logo and welcome text



    app_name_var = create_app_name_input(root)  # Create app name input section



    folder_path_var = create_folder_selector_with_display(root)  # Create folder selector with display

    


    entry_file_var = create_entry_point_selector_with_display(root, folder_path_var)  # Create entry point selector with display

   

    python_exe_var = create_python_exe_selector_with_display(root)  # Create Python executable selector with display


    create_folder_preview_with_display(root, folder_path_var)  # Create folder preview with display


    mode_var_file, mode_var_console = create_mode_selectors_with_display(root)  # Create mode selectors with display



    create_command_preview_with_display(root, app_name_var, entry_file_var, folder_path_var, python_exe_var, mode_var_file, mode_var_console)  # Create command preview with display

    # Output frame (initially not packed)
    output_frame = tk.Frame(root)

  
    output_text = tk.Text(output_frame, height=3, width=60, wrap="word", bd=2, font=("Aerial", 10), fg="blue")
    scrollbar = tk.Scrollbar(output_frame, orient="horizontal", command=output_text.xview)
    output_text.configure(xscrollcommand=scrollbar.set)



    output_label = None
    output_label_ref = [output_label]  # Mutable reference



    def wrapper_function():
        def task():
            run_pyinstaller(
                app_name_var.get(),
                entry_file_var.get(),
                folder_path_var.get(),
                python_exe_var.get(),
                mode_var_file.get(),
                mode_var_console.get(),
                output_text,
                root,
                package_button,
                output_frame,
                output_label_ref,
                scrollbar,final_venv_path=""
            )

        threading.Thread(target=task).start()


        # Button to run PyInstaller
    package_button = tk.Button(root, text="Package  Application", command=wrapper_function, fg="white", bg="green", width=40, font=("Aerial", 12))
    package_button.pack(pady=(10,10))



    root.mainloop()
