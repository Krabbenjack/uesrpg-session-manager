"""
Derived Stats Engine for UESRPG Session Manager.

This engine loads mechanics rules from derived_stats_v1.json and applies them
to character state to compute:
- Characteristic bonuses (from scores)
- Base bonuses (mapped from characteristic bonuses)
- Derived stats (HP, MP, Speed, IR, etc.)

The engine respects "do_not_overwrite" policies to preserve user-edited values
like current HP/MP pools.
"""

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, List, Optional
from copy import deepcopy

logger = logging.getLogger(__name__)


class DerivedStatsEngine:
    """Engine for computing derived stats from mechanics rules."""
    
    def __init__(self, rules_path: Optional[str] = None):
        """
        Initialize the engine with rules.
        
        Args:
            rules_path: Path to derived_stats JSON file. If None, uses default.
        """
        self.rules = None
        self.rules_path = rules_path or self._get_default_rules_path()
        self._load_rules()
    
    def _get_default_rules_path(self) -> str:
        """Get default path to derived_stats_v1.json."""
        # Assume this module is in core/mechanics/
        module_dir = Path(__file__).parent
        rules_file = module_dir / "derived_stats_v1.json"
        return str(rules_file)
    
    def _load_rules(self):
        """Load mechanics rules from JSON file."""
        try:
            with open(self.rules_path, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            logger.info(f"Loaded derived stats rules from {self.rules_path}")
        except FileNotFoundError:
            logger.error(f"Rules file not found: {self.rules_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in rules file: {e}")
            raise
    
    def apply(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply derived stats rules to a character state.
        
        Args:
            state: Character state dictionary (will be modified in place)
        
        Returns:
            Modified state with computed derived values
        """
        if not self.rules:
            logger.warning("No rules loaded, skipping derived stats computation")
            return state
        
        # Process each operation in order
        operations = self.rules.get('operations', [])
        for operation in operations:
            try:
                self._apply_operation(state, operation)
            except Exception as e:
                op_id = operation.get('id', 'unknown')
                logger.error(f"Error applying operation {op_id}: {e}", exc_info=True)
                # Continue with other operations even if one fails
        
        return state
    
    def _apply_operation(self, state: Dict, operation: Dict):
        """Apply a single operation to the state."""
        op_type = operation.get('type')
        op_id = operation.get('id', 'unknown')
        
        if op_type == 'for_each_in_list':
            self._apply_for_each_in_list(state, operation)
        elif op_type == 'set_many':
            self._apply_set_many(state, operation)
        else:
            logger.warning(f"Unknown operation type: {op_type} in {op_id}")
    
    def _apply_for_each_in_list(self, state: Dict, operation: Dict):
        """
        Apply for_each_in_list operation.
        
        Iterates over items in a list and applies set operations to each item.
        """
        list_path = operation.get('list_path')
        where_clause = operation.get('where', {})
        set_operations = operation.get('set', [])
        
        # Get the list from state
        items = self._get_path_value(state, list_path)
        if not isinstance(items, list):
            logger.warning(f"Path {list_path} did not resolve to a list")
            return
        
        # Filter items if where clause is present
        target_abbrs = where_clause.get('in', []) if where_clause.get('key') == 'abbr' else None
        
        # Process each item
        for index, item in enumerate(items):
            # Check if item matches where clause
            if target_abbrs:
                item_abbr = item.get('abbr', '')
                if item_abbr not in target_abbrs:
                    continue
            
            # Apply set operations for this item
            for set_op in set_operations:
                path_template = set_op.get('path_template')
                expr = set_op.get('expr')
                
                # Resolve path template with index
                path = path_template.replace('{index}', str(index))
                
                # Evaluate expression
                value = self._evaluate_expression(state, expr, {'index': index})
                
                # Set the value
                self._set_path_value(state, path, value)
    
    def _apply_set_many(self, state: Dict, operation: Dict):
        """
        Apply set_many operation.
        
        Sets multiple values according to expressions.
        Respects do_not_overwrite policy for specific paths.
        """
        policy = operation.get('policy', {})
        overwrite = policy.get('overwrite', True)
        do_not_overwrite_paths = policy.get('do_not_overwrite_paths_matching', [])
        
        set_operations = operation.get('set', [])
        
        for set_op in set_operations:
            path = set_op.get('path')
            expr = set_op.get('expr')
            
            # Check if this path should not be overwritten
            if do_not_overwrite_paths:
                should_skip = False
                for protected_path in do_not_overwrite_paths:
                    if path == protected_path:
                        # Check if value already exists
                        existing_value = self._get_path_value(state, path)
                        if existing_value is not None:
                            should_skip = True
                            break
                
                if should_skip:
                    continue
            
            # Evaluate expression and set value
            if isinstance(expr, (int, float, str, bool)):
                # Literal value
                value = expr
            else:
                # Expression to evaluate
                value = self._evaluate_expression(state, expr)
            
            self._set_path_value(state, path, value)
    
    def _evaluate_expression(self, state: Dict, expr: Any, context: Optional[Dict] = None) -> Any:
        """
        Evaluate an expression.
        
        Args:
            state: Character state
            expr: Expression to evaluate (dict with 'op' key, or literal value)
            context: Optional context (e.g., loop variables)
        
        Returns:
            Evaluated value
        """
        if not isinstance(expr, dict):
            # Literal value
            return expr
        
        # Handle path_template (used in for_each_in_list)
        if 'path_template' in expr and context:
            path_template = expr.get('path_template')
            # Replace placeholders with context values
            path = path_template
            for key, value in context.items():
                path = path.replace(f'{{{key}}}', str(value))
            return self._get_path_value(state, path)
        
        op = expr.get('op')
        if not op:
            logger.warning(f"Expression missing 'op' key: {expr}")
            return None
        
        # Evaluate operation
        if op == 'tens_digit':
            arg_expr = expr.get('arg')
            arg_value = self._evaluate_expression(state, arg_expr, context)
            return self._op_tens_digit(arg_value)
        
        elif op == 'ceil_div':
            a_expr = expr.get('a')
            b_expr = expr.get('b')
            a_value = self._evaluate_expression(state, a_expr, context)
            b_value = self._evaluate_expression(state, b_expr, context)
            return self._op_ceil_div(a_value, b_value)
        
        elif op == 'add':
            args_exprs = expr.get('args', [])
            values = [self._evaluate_expression(state, arg, context) for arg in args_exprs]
            return self._op_add(values)
        
        elif op == 'mul':
            a_expr = expr.get('a')
            b_expr = expr.get('b')
            a_value = self._evaluate_expression(state, a_expr, context)
            b_value = self._evaluate_expression(state, b_expr, context)
            return self._op_mul(a_value, b_value)
        
        elif op == 'get_path':
            path = expr.get('path')
            return self._get_path_value(state, path)
        
        elif op == 'char_score_by_abbr':
            abbr = expr.get('abbr')
            return self._op_char_score_by_abbr(state, abbr)
        
        elif op == 'char_bonus_by_abbr':
            abbr = expr.get('abbr')
            return self._op_char_bonus_by_abbr(state, abbr)
        
        else:
            logger.warning(f"Unknown operation: {op}")
            return None
    
    # Operation implementations
    
    def _op_tens_digit(self, value: Any) -> int:
        """Compute tens digit (floor(x / 10))."""
        try:
            num = int(value) if value is not None else 0
            return num // 10
        except (ValueError, TypeError):
            logger.warning(f"Cannot compute tens_digit for value: {value}")
            return 0
    
    def _op_ceil_div(self, a: Any, b: Any) -> int:
        """Compute ceiling division (ceil(a / b))."""
        try:
            a_num = float(a) if a is not None else 0
            b_num = float(b) if b is not None else 1
            if b_num == 0:
                return 0
            return math.ceil(a_num / b_num)
        except (ValueError, TypeError):
            logger.warning(f"Cannot compute ceil_div for values: {a}, {b}")
            return 0
    
    def _op_add(self, values: List[Any]) -> int:
        """Compute sum of values."""
        try:
            total = 0
            for val in values:
                num = int(val) if val is not None else 0
                total += num
            return total
        except (ValueError, TypeError):
            logger.warning(f"Cannot compute add for values: {values}")
            return 0
    
    def _op_mul(self, a: Any, b: Any) -> int:
        """Compute multiplication (a * b)."""
        try:
            a_num = int(a) if a is not None else 0
            b_num = int(b) if b is not None else 0
            return a_num * b_num
        except (ValueError, TypeError):
            logger.warning(f"Cannot compute mul for values: {a}, {b}")
            return 0
    
    def _op_char_score_by_abbr(self, state: Dict, abbr: str) -> int:
        """Look up characteristic score by abbreviation."""
        characteristics = state.get('characteristics', [])
        for char in characteristics:
            if char.get('abbr') == abbr:
                return char.get('score', 0)
        logger.warning(f"Characteristic not found: {abbr}")
        return 0
    
    def _op_char_bonus_by_abbr(self, state: Dict, abbr: str) -> int:
        """Look up characteristic bonus by abbreviation."""
        characteristics = state.get('characteristics', [])
        for char in characteristics:
            if char.get('abbr') == abbr:
                return char.get('bonus', 0)
        logger.warning(f"Characteristic not found: {abbr}")
        return 0
    
    # Path utility methods
    
    def _get_path_value(self, state: Dict, path: str) -> Any:
        """
        Get value from state using JSONPath-style path.
        
        Supports:
        - $.key for root-level keys
        - $.key.subkey for nested keys
        - $.key[0].subkey for list indexing
        
        Args:
            state: State dictionary
            path: JSONPath string (e.g., "$.characteristics[0].score")
        
        Returns:
            Value at path, or None if not found
        """
        if not path or not path.startswith('$.'):
            logger.warning(f"Invalid path format: {path}")
            return None
        
        # Remove $. prefix
        path = path[2:]
        
        # Split path into parts
        parts = self._parse_path(path)
        
        # Traverse the state
        current = state
        for part in parts:
            if isinstance(part, str):
                # Dictionary key
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    return None
            elif isinstance(part, int):
                # List index
                if isinstance(current, list) and 0 <= part < len(current):
                    current = current[part]
                else:
                    return None
            
            if current is None:
                return None
        
        return current
    
    def _set_path_value(self, state: Dict, path: str, value: Any):
        """
        Set value in state using JSONPath-style path.
        
        Creates intermediate dictionaries/lists as needed.
        
        Args:
            state: State dictionary (modified in place)
            path: JSONPath string (e.g., "$.characteristics[0].bonus")
            value: Value to set
        """
        if not path or not path.startswith('$.'):
            logger.warning(f"Invalid path format: {path}")
            return
        
        # Remove $. prefix
        path = path[2:]
        
        # Split path into parts
        parts = self._parse_path(path)
        
        if not parts:
            return
        
        # Traverse to the parent of the target
        current = state
        for i, part in enumerate(parts[:-1]):
            next_part = parts[i + 1]
            
            if isinstance(part, str):
                # Dictionary key
                if part not in current:
                    # Create intermediate structure
                    if isinstance(next_part, int):
                        current[part] = []
                    else:
                        current[part] = {}
                current = current[part]
            elif isinstance(part, int):
                # List index
                if not isinstance(current, list):
                    logger.warning(f"Cannot index non-list at path: {path}")
                    return
                # Extend list if needed
                while len(current) <= part:
                    current.append({})
                current = current[part]
        
        # Set the final value
        final_part = parts[-1]
        if isinstance(final_part, str):
            if isinstance(current, dict):
                current[final_part] = value
            else:
                logger.warning(f"Cannot set key on non-dict at path: {path}")
        elif isinstance(final_part, int):
            if isinstance(current, list):
                while len(current) <= final_part:
                    current.append(None)
                current[final_part] = value
            else:
                logger.warning(f"Cannot set index on non-list at path: {path}")
    
    def _parse_path(self, path: str) -> List:
        """
        Parse a JSONPath string into parts.
        
        Args:
            path: Path string (without $. prefix)
        
        Returns:
            List of parts (strings for keys, ints for list indices)
        
        Examples:
            "characteristics[0].score" -> ["characteristics", 0, "score"]
            "base_bonuses.SB" -> ["base_bonuses", "SB"]
        """
        parts = []
        current = ""
        i = 0
        
        while i < len(path):
            char = path[i]
            
            if char == '.':
                # End of current part
                if current:
                    parts.append(current)
                    current = ""
                i += 1
            elif char == '[':
                # Start of list index
                if current:
                    parts.append(current)
                    current = ""
                # Find closing bracket
                j = i + 1
                while j < len(path) and path[j] != ']':
                    j += 1
                if j < len(path):
                    index_str = path[i+1:j]
                    try:
                        parts.append(int(index_str))
                    except ValueError:
                        logger.warning(f"Invalid list index: {index_str}")
                    i = j + 1
                else:
                    logger.warning(f"Unclosed bracket in path: {path}")
                    i += 1
            else:
                current += char
                i += 1
        
        # Add final part
        if current:
            parts.append(current)
        
        return parts


# Module-level function for easy access
_engine_instance = None

def apply_derived_stats(state: Dict[str, Any], rules_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Apply derived stats rules to a character state.
    
    This is the main entry point for computing derived stats.
    Uses a module-level engine instance for efficiency.
    
    Args:
        state: Character state dictionary (modified in place)
        rules_path: Optional path to rules JSON file
    
    Returns:
        Modified state with computed derived values
    """
    global _engine_instance
    
    # Create or reuse engine instance
    if _engine_instance is None or rules_path is not None:
        _engine_instance = DerivedStatsEngine(rules_path)
    
    return _engine_instance.apply(state)
