"""UESRPG Session Manager - Main application entry point."""
import tkinter as tk
from tkinter import messagebox
import os
import sys
import traceback

from uesrpg_sm.core.spec_loader import SpecLoader
from uesrpg_sm.core.character_model import CharacterModel
from uesrpg_sm.core.importer import Importer
from uesrpg_sm.ui.spec_renderer import SpecRenderer
from uesrpg_sm.ui.character_window import CharacterWindow


def show_error_dialog(title, message):
    """Show an error dialog using tkinter.
    
    Args:
        title: Dialog title
        message: Error message to display
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(title, message)
        root.destroy()
    except Exception:
        # Fallback to console output if tkinter fails
        print(f"ERROR: {title}")
        print(message)


def main():
    """Main application entry point."""
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load UI specification
    spec_path = os.path.join(script_dir, 'ui', 'ui_spec.json')
    
    if not os.path.exists(spec_path):
        show_error_dialog(
            "Configuration Error",
            f"UI specification file not found:\n{spec_path}\n\n"
            "Please ensure the ui/ui_spec.json file exists."
        )
        sys.exit(1)
    
    try:
        spec_loader = SpecLoader(spec_path)
    except FileNotFoundError as e:
        show_error_dialog(
            "Configuration Error",
            f"Failed to load specification file:\n{e}"
        )
        sys.exit(1)
    except Exception as e:
        show_error_dialog(
            "Configuration Error",
            f"Error loading specification:\n{e}\n\n{traceback.format_exc()}"
        )
        sys.exit(1)
    
    # Create root window
    try:
        root = tk.Tk()
    except Exception as e:
        print(f"Error: Failed to initialize tkinter: {e}")
        print("Please ensure tkinter is installed (python3-tk package)")
        sys.exit(1)
    
    try:
        # Get application config
        app_config = spec_loader.get_app_config()
        root.title(app_config.get('title', 'UESRPG Session Manager'))
        
        # Initialize character model with default data
        default_character = spec_loader.get_default_character()
        if not default_character:
            raise ValueError("No default character data found in specification")
        character_model = CharacterModel(default_character)
        
        # Create renderer
        spec = spec_loader.spec
        renderer = SpecRenderer(spec, character_model)
        
        # Apply theme
        renderer.apply_theme(root)
        
        # Create importer
        import_window_spec = spec_loader.get_window('import_window')
        import_map = import_window_spec.get('import_map', {}) if import_window_spec else {}
        importer = Importer(import_map)
        
        # Get character window spec
        char_window_spec = spec_loader.get_window('character_window')
        if not char_window_spec:
            raise ValueError("No character_window specification found")
        
        # Create main window
        character_window = CharacterWindow(root, char_window_spec, spec_loader, renderer, character_model, importer)
        
        # Ensure assets directory exists
        portrait_dir = spec_loader.get_portrait_dir()
        if portrait_dir:
            full_portrait_dir = os.path.join(script_dir, portrait_dir)
            os.makedirs(full_portrait_dir, exist_ok=True)
        
        # Start main loop
        root.mainloop()
        
    except Exception as e:
        error_msg = f"An error occurred during initialization:\n\n{e}\n\n{traceback.format_exc()}"
        try:
            messagebox.showerror("Application Error", error_msg, parent=root)
        except Exception:
            print(f"ERROR: {error_msg}")
        root.destroy()
        sys.exit(1)


if __name__ == '__main__':
    main()
