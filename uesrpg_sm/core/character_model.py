"""Character data model with JSONPath-like binding support."""
import copy


class CharacterModel:
    """Manages character data with JSONPath-like binding."""
    
    def __init__(self, default_data=None):
        """Initialize character model.
        
        Args:
            default_data: Default character data dictionary
        """
        self.data = default_data if default_data else {}
        self._observers = []
    
    def reset(self, default_data):
        """Reset character to default data.
        
        Args:
            default_data: Default character data dictionary
        """
        self.data = copy.deepcopy(default_data)
        self._notify_observers()
    
    def get_value(self, bind_path):
        """Get value from character data using JSONPath-like binding.
        
        Args:
            bind_path: JSONPath string like "$.name" or "$.derived_stats.HP.current"
                       or "$.characteristics[0].name"
            
        Returns:
            Value at the path or None if not found
        """
        if not bind_path or not bind_path.startswith('$'):
            return None
        
        # Remove the leading '$.' or '$'
        path = bind_path[2:] if bind_path.startswith('$.') else bind_path[1:]
        if not path:
            return self.data
        
        # Parse path with array notation support
        import re
        # Split by . but keep array indices separate
        parts = []
        for segment in path.split('.'):
            # Check for array notation like "characteristics[0]"
            match = re.match(r'([^\[]+)\[(\d+)\]', segment)
            if match:
                parts.append(match.group(1))  # The key part
                parts.append(match.group(2))  # The index part
            else:
                parts.append(segment)
        
        # Navigate through the data structure
        current = self.data
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    current = current[idx] if idx < len(current) else None
                except (ValueError, IndexError):
                    return None
            else:
                return None
            
            if current is None:
                return None
        
        return current
    
    def set_value(self, bind_path, value):
        """Set value in character data using JSONPath-like binding.
        
        Args:
            bind_path: JSONPath string like "$.name" or "$.derived_stats.HP.current"
                       or "$.characteristics[0].name"
            value: Value to set
        """
        if not bind_path or not bind_path.startswith('$'):
            return
        
        # Remove the leading '$.' or '$'
        path = bind_path[2:] if bind_path.startswith('$.') else bind_path[1:]
        if not path:
            return
        
        # Parse path with array notation support
        import re
        parts = []
        for segment in path.split('.'):
            # Check for array notation like "characteristics[0]"
            match = re.match(r'([^\[]+)\[(\d+)\]', segment)
            if match:
                parts.append(match.group(1))  # The key part
                parts.append(match.group(2))  # The index part
            else:
                parts.append(segment)
        
        # Navigate through the data structure, creating as needed
        current = self.data
        
        for i, part in enumerate(parts[:-1]):
            if isinstance(current, dict):
                if part not in current:
                    # Determine if next part is a number (list index) or string (dict key)
                    next_part = parts[i + 1]
                    try:
                        int(next_part)
                        current[part] = []
                    except ValueError:
                        current[part] = {}
                current = current[part]
            elif isinstance(current, list):
                try:
                    idx = int(part)
                    # Extend list if needed
                    while len(current) <= idx:
                        current.append({})
                    current = current[idx]
                except ValueError:
                    return
            else:
                return
        
        # Set the final value
        final_key = parts[-1]
        if isinstance(current, dict):
            current[final_key] = value
        elif isinstance(current, list):
            try:
                idx = int(final_key)
                # Extend list if needed
                while len(current) <= idx:
                    current.append(None)
                current[idx] = value
            except ValueError:
                pass
        
        self._notify_observers()
    
    def add_observer(self, callback):
        """Add an observer callback for data changes.
        
        Args:
            callback: Function to call when data changes
        """
        if callback not in self._observers:
            self._observers.append(callback)
    
    def remove_observer(self, callback):
        """Remove an observer callback.
        
        Args:
            callback: Function to remove
        """
        if callback in self._observers:
            self._observers.remove(callback)
    
    def _notify_observers(self):
        """Notify all observers of data changes."""
        for callback in self._observers:
            try:
                callback()
            except Exception as e:
                print(f"Error in observer callback: {e}")
    
    def to_dict(self):
        """Get the character data as a dictionary.
        
        Returns:
            Character data dictionary
        """
        return self.data
    
    def from_dict(self, data):
        """Load character data from a dictionary.
        
        Args:
            data: Character data dictionary
        """
        self.data = copy.deepcopy(data)
        self._notify_observers()
