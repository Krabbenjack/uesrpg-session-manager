#!/usr/bin/env python3
"""
UESRPG Session Manager - Character Window
Entry point for the Tkinter-based character management UI.
"""

import tkinter as tk
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Main entry point - create root window and launch UI."""
    try:
        # Import UI module
        from ui import CharacterWindowUI
        
        # Create Tk root
        root = tk.Tk()
        
        # Create and initialize UI
        ui = CharacterWindowUI(root)
        
        # Run mainloop
        root.mainloop()
        
    except Exception as e:
        logging.error(f"Failed to start application: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
