"""Validator module for ensuring character data completeness."""
import copy


def validate_and_fill(data, default, path=""):
    """Recursively ensures all keys from default exist in data.
    
    - If a key is missing: copy from default
    - If type mismatches (e.g., expected dict but got string): replace with default and log
    - Does not delete unknown keys
    
    Args:
        data: The data dictionary to validate
        default: The default data dictionary with expected structure
        path: Current path for logging (internal use)
        
    Returns:
        The validated/filled data dictionary
    """
    if data is None:
        return copy.deepcopy(default)
    
    if not isinstance(default, dict):
        # If default is not a dict, just return data (or default if data is None)
        return data if data is not None else copy.deepcopy(default)
    
    if not isinstance(data, dict):
        # Type mismatch: data should be dict but isn't
        print(f"Warning: Type mismatch at {path or 'root'}: expected dict, got {type(data).__name__}. Replacing with default.")
        return copy.deepcopy(default)
    
    # Iterate through all keys in default
    for key, default_value in default.items():
        current_path = f"{path}.{key}" if path else key
        
        if key not in data:
            # Key is missing, copy from default
            data[key] = copy.deepcopy(default_value)
        else:
            # Key exists, check type compatibility
            data_value = data[key]
            
            if isinstance(default_value, dict):
                if not isinstance(data_value, dict):
                    # Expected dict but got something else
                    print(f"Warning: Type mismatch at {current_path}: expected dict, got {type(data_value).__name__}. Replacing with default.")
                    data[key] = copy.deepcopy(default_value)
                else:
                    # Recursively validate nested dict
                    data[key] = validate_and_fill(data_value, default_value, current_path)
                    
            elif isinstance(default_value, list):
                if not isinstance(data_value, list):
                    # Expected list but got something else
                    print(f"Warning: Type mismatch at {current_path}: expected list, got {type(data_value).__name__}. Replacing with default.")
                    data[key] = copy.deepcopy(default_value)
                # Note: We don't validate list contents - just ensure it's a list
    
    return data
