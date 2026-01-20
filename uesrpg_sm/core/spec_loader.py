"""Load and parse UI specification from JSON."""
import json
import os


class SpecLoader:
    """Loads and provides access to the UI specification."""
    
    def __init__(self, spec_path):
        """Initialize the spec loader.
        
        Args:
            spec_path: Path to the ui_spec.json file
        """
        self.spec_path = spec_path
        self.spec = None
        self._load()
    
    def _load(self):
        """Load the specification from JSON file."""
        if not os.path.exists(self.spec_path):
            raise FileNotFoundError(f"Spec file not found: {self.spec_path}")
        
        with open(self.spec_path, 'r', encoding='utf-8') as f:
            self.spec = json.load(f)
    
    def get_app_config(self):
        """Get application configuration."""
        return self.spec.get('app', {})
    
    def get_theme(self):
        """Get theme configuration."""
        return self.spec.get('theme', {})
    
    def get_menus(self):
        """Get menu definitions."""
        return self.spec.get('menus', [])
    
    def get_window(self, window_id):
        """Get window specification by ID.
        
        Args:
            window_id: The ID of the window to retrieve
            
        Returns:
            Window specification dict or None if not found
        """
        windows = self.spec.get('windows', [])
        for window in windows:
            if window.get('id') == window_id:
                return window
        return None
    
    def get_default_character(self):
        """Get default character data."""
        return self.spec.get('data', {}).get('default_character', {})
    
    def get_portrait_dir(self):
        """Get portrait directory path."""
        return self.spec.get('data', {}).get('portrait_dir', 'uesrpg_sm/assets/portraits')
