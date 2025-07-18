from src.tools.core_libs import *
from src.tools.ui_libs import *
from src.utils.custom_radio import CustomRadioGroup

def create_mode_selectors_with_display(root):
    mode_var_file = tk.StringVar(value="onefile") # by default 

    mode_frame = tk.Frame(root)
    mode_frame.pack(anchor=tk.W, padx=10, pady=(20,5))
    # Options for packaging mode
    options = [
        ("Onefile (--onefile)", "onefile"),
        ("Onefolder (--onedir)", "onefolder")
    ]
    Label(mode_frame,text="Select a packaging mode:",font=("Arial", 12)).pack(side=tk.LEFT, padx=(4,2))
    # Create custom radio buttons

    radio_group = CustomRadioGroup(mode_frame, options, variable=mode_var_file)
    radio_group.pack(side=tk.LEFT, padx=2)




    #same for window and console radio buttons
    mode_var_console = tk.StringVar(value="console") # by default
    mode_frame_console = tk.Frame(root)
    mode_frame_console.pack(anchor=tk.W, padx=10, pady=(20,5))
    # Options for console mode
    options_console = [
        ("Console (--console)", "console"),
        ("Windowed (--windowed)", "windowed")
    ]
    # Label for console mode
    Label(mode_frame_console,text="Select a console mode:",font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
    # Create custom radio buttons for console mode

    radio_group_console = CustomRadioGroup(mode_frame_console, options_console, variable=mode_var_console)
    radio_group_console.pack(side=tk.LEFT, padx=10)

    return mode_var_file, mode_var_console  # Return the variables for further use
