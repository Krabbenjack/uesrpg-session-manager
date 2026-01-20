"""UESRPG Session Manager - Main application entry point."""
import tkinter as tk
import os
import sys

from uesrpg_sm.core.spec_loader import SpecLoader
from uesrpg_sm.core.character_model import CharacterModel
from uesrpg_sm.core.importer import Importer
from uesrpg_sm.ui.spec_renderer import SpecRenderer
from uesrpg_sm.ui.character_window import CharacterWindow


def main():
    """Main application entry point."""
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load UI specification
    spec_path = os.path.join(script_dir, 'ui', 'ui_spec.json')
    
    try:
        spec_loader = SpecLoader(spec_path)
    except Exception as e:
        print(f"Error loading specification: {e}")
        sys.exit(1)
    
    # Create root window
    root = tk.Tk()
    
    # Get application config
    app_config = spec_loader.get_app_config()
    root.title(app_config.get('title', 'UESRPG Session Manager'))
    
    # Initialize character model with default data
    default_character = spec_loader.get_default_character()
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
    
    # Create main window
    character_window = CharacterWindow(root, char_window_spec, spec_loader, renderer, character_model, importer)
    
    # Start main loop
    root.mainloop()


if __name__ == '__main__':
    main()
