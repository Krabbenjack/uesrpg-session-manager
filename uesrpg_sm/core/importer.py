"""Import character data from external JSON files."""
import json
import copy


class Importer:
    """Handles importing character data with merge rules."""
    
    def __init__(self, import_map):
        """Initialize importer with an import map.
        
        Args:
            import_map: Dictionary mapping source keys to target bind paths
        """
        self.import_map = import_map
    
    def load_json(self, file_path):
        """Load JSON data from a file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            Loaded JSON data as dictionary
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_preview_info(self, data):
        """Generate preview information from imported data.
        
        Args:
            data: Imported JSON data
            
        Returns:
            Preview string with key information
        """
        lines = []
        
        # Extract key fields for preview
        if 'name' in data:
            lines.append(f"Name: {data['name']}")
        
        if 'race' in data:
            lines.append(f"Race: {data['race']}")
        
        if 'birthsign' in data:
            bs = data['birthsign']
            if isinstance(bs, dict):
                sign_str = bs.get('sign', '')
                category_str = bs.get('category', '')
                if sign_str or category_str:
                    lines.append(f"Birthsign: {category_str} - {sign_str}")
        
        # Count skills
        if 'skills' in data and isinstance(data['skills'], list):
            lines.append(f"Skills: {len(data['skills'])} skill(s)")
        
        if not lines:
            lines.append("(No preview data available)")
        
        return '\n'.join(lines)
    
    def import_data(self, source_data, character_model, overwrite=False):
        """Import data into character model using the import map.
        
        Args:
            source_data: Source JSON data
            character_model: CharacterModel instance to import into
            overwrite: If True, overwrite existing fields; if False, only fill empty fields
        """
        for source_key, target_bind in self.import_map.items():
            if source_key in source_data:
                source_value = source_data[source_key]
                
                # Get current value
                current_value = character_model.get_value(target_bind)
                
                # Decide whether to import based on overwrite flag
                should_import = overwrite or self._is_empty(current_value)
                
                if should_import:
                    # Deep copy to avoid reference issues
                    value_to_set = copy.deepcopy(source_value)
                    character_model.set_value(target_bind, value_to_set)
    
    def _is_empty(self, value):
        """Check if a value is considered empty for import purposes.
        
        Args:
            value: Value to check
            
        Returns:
            True if value is empty, False otherwise
        """
        if value is None:
            return True
        if value == "":
            return True
        if isinstance(value, list) and len(value) == 0:
            return True
        if isinstance(value, dict) and len(value) == 0:
            return True
        return False
