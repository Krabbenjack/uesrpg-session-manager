"""Render UI widgets from specification."""
import tkinter as tk
from tkinter import ttk
import os


class SpecRenderer:
    """Renders UI widgets based on specification."""
    
    def __init__(self, spec, character_model):
        """Initialize the renderer.
        
        Args:
            spec: UI specification dictionary
            character_model: CharacterModel instance for data binding
        """
        self.spec = spec
        self.character_model = character_model
        self.theme = spec.get('theme', {})
        self.colors = self.theme.get('colors', {})
        self.typography = self.theme.get('typography', {})
        self.spacing = self.theme.get('spacing', {})
        
        # Track widgets for data binding
        self.bound_widgets = {}
        
    def apply_theme(self, root):
        """Apply theme styling to the root window.
        
        Args:
            root: Tk root window
        """
        style = ttk.Style()
        
        # Configure colors
        bg = self.colors.get('bg', '#FFD5AF')
        fg = self.colors.get('fg', '#9D6E6B')
        
        # Set default background
        root.configure(bg=bg)
        
        # Configure ttk styles
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background=bg, foreground=fg)
        style.configure('TCheckbutton', background=bg, foreground=fg)
        style.configure('TNotebook', background=bg)
        style.configure('TNotebook.Tab', background=bg, foreground=fg)
        
        # Heading style (bold)
        heading_font = self._get_font('heading')
        style.configure('Heading.TLabel', font=heading_font, background=bg, foreground=fg)
        
        # Skill style (italic)
        skill_font = self._get_font('skill')
        style.configure('Skill.TLabel', font=skill_font, background=bg, foreground=fg)
    
    def _get_font(self, font_type='base'):
        """Get font tuple from typography spec.
        
        Args:
            font_type: Type of font ('base', 'heading', 'skill')
            
        Returns:
            Font tuple (family, size, weight, slant)
        """
        font_spec = self.typography.get(font_type, self.typography.get('base', {}))
        family = font_spec.get('family', 'TkDefaultFont')
        size = font_spec.get('size', 10)
        weight = font_spec.get('weight', 'normal')
        slant = font_spec.get('slant', 'roman')
        return (family, size, weight, slant)
    
    def render_field(self, parent, field_spec, row=0, column=0):
        """Render a field widget.
        
        Args:
            parent: Parent widget
            field_spec: Field specification dictionary
            row: Grid row
            column: Grid column
            
        Returns:
            Created widget
        """
        widget_type = field_spec.get('widget', 'entry')
        label_text = field_spec.get('label', '')
        bind_path = field_spec.get('bind', '')
        colspan = field_spec.get('colspan', 1)
        
        # Create label
        label = ttk.Label(parent, text=label_text + ':')
        label.grid(row=row, column=column, sticky='w', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        # Create widget based on type
        widget = None
        widget_column = column + 1 if label_text else column
        # Calculate widget columnspan - must be at least 1
        widget_colspan = max(1, colspan - 1) if label_text else colspan
        
        if widget_type == 'entry':
            widget = ttk.Entry(parent)
            widget.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='ew', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        elif widget_type == 'readonly_entry':
            widget = ttk.Entry(parent, state='readonly')
            widget.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='ew', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        elif widget_type == 'textarea':
            height = field_spec.get('height', 5)
            frame = ttk.Frame(parent)
            frame.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='nsew', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
            
            widget = tk.Text(frame, height=height, width=30, bg='white', fg=self.colors.get('fg', '#000000'))
            widget.pack(side='left', fill='both', expand=True)
            
            scrollbar = ttk.Scrollbar(frame, command=widget.yview)
            scrollbar.pack(side='right', fill='y')
            widget.config(yscrollcommand=scrollbar.set)
        
        elif widget_type == 'spin_int':
            min_val = field_spec.get('min', 0)
            max_val = field_spec.get('max', 999999)
            widget = ttk.Spinbox(parent, from_=min_val, to=max_val, width=10)
            widget.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='w', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        elif widget_type == 'check':
            var = tk.BooleanVar()
            widget = ttk.Checkbutton(parent, variable=var)
            widget.var = var
            widget.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='w', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        elif widget_type == 'tags':
            # Comma-separated tags
            widget = ttk.Entry(parent)
            widget.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='ew', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        elif widget_type == 'int_list_csv':
            # Comma-separated integers
            widget = ttk.Entry(parent)
            widget.grid(row=row, column=widget_column, columnspan=widget_colspan, sticky='ew', padx=self.spacing.get('padx', 5), pady=self.spacing.get('pady', 2))
        
        # Bind to character model if bind path provided
        if bind_path and widget:
            self._bind_widget(widget, bind_path, widget_type)
        
        return widget
    
    def _bind_widget(self, widget, bind_path, widget_type):
        """Bind a widget to the character model.
        
        Args:
            widget: Widget to bind
            bind_path: JSONPath binding string
            widget_type: Type of widget
        """
        self.bound_widgets[bind_path] = (widget, widget_type)
        
        # Set initial value
        self._update_widget_from_model(widget, bind_path, widget_type)
        
        # Bind update events
        if widget_type in ['entry', 'readonly_entry']:
            widget.bind('<FocusOut>', lambda e: self._update_model_from_widget(widget, bind_path, widget_type))
        elif widget_type == 'textarea':
            widget.bind('<FocusOut>', lambda e: self._update_model_from_widget(widget, bind_path, widget_type))
        elif widget_type == 'spin_int':
            widget.bind('<FocusOut>', lambda e: self._update_model_from_widget(widget, bind_path, widget_type))
        elif widget_type == 'check':
            widget.var.trace('w', lambda *args: self._update_model_from_widget(widget, bind_path, widget_type))
        elif widget_type in ['tags', 'int_list_csv']:
            widget.bind('<FocusOut>', lambda e: self._update_model_from_widget(widget, bind_path, widget_type))
    
    def _update_widget_from_model(self, widget, bind_path, widget_type):
        """Update widget value from character model.
        
        Args:
            widget: Widget to update
            bind_path: JSONPath binding string
            widget_type: Type of widget
        """
        value = self.character_model.get_value(bind_path)
        
        if value is None:
            value = ""
        
        try:
            if widget_type == 'entry' or widget_type == 'readonly_entry':
                widget.delete(0, tk.END)
                widget.insert(0, str(value))
            
            elif widget_type == 'textarea':
                widget.delete('1.0', tk.END)
                widget.insert('1.0', str(value))
            
            elif widget_type == 'spin_int':
                widget.delete(0, tk.END)
                widget.insert(0, str(value) if value else "0")
            
            elif widget_type == 'check':
                widget.var.set(bool(value))
            
            elif widget_type == 'tags':
                # Convert list to comma-separated string
                if isinstance(value, list):
                    widget.delete(0, tk.END)
                    widget.insert(0, ', '.join(str(v) for v in value))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
            
            elif widget_type == 'int_list_csv':
                # Convert list to comma-separated string
                if isinstance(value, list):
                    widget.delete(0, tk.END)
                    widget.insert(0, ', '.join(str(v) for v in value))
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, str(value))
        except Exception as e:
            print(f"Error updating widget {bind_path}: {e}")
    
    def _update_model_from_widget(self, widget, bind_path, widget_type):
        """Update character model from widget value.
        
        Args:
            widget: Widget to read value from
            bind_path: JSONPath binding string
            widget_type: Type of widget
        """
        try:
            if widget_type == 'entry':
                value = widget.get()
                self.character_model.set_value(bind_path, value)
            
            elif widget_type == 'textarea':
                value = widget.get('1.0', tk.END).strip()
                self.character_model.set_value(bind_path, value)
            
            elif widget_type == 'spin_int':
                value_str = widget.get()
                try:
                    value = int(value_str) if value_str else 0
                except ValueError:
                    value = 0
                self.character_model.set_value(bind_path, value)
            
            elif widget_type == 'check':
                value = widget.var.get()
                self.character_model.set_value(bind_path, value)
            
            elif widget_type == 'tags':
                # Convert comma-separated string to list
                value_str = widget.get().strip()
                if value_str:
                    value = [v.strip() for v in value_str.split(',') if v.strip()]
                else:
                    value = []
                self.character_model.set_value(bind_path, value)
            
            elif widget_type == 'int_list_csv':
                # Convert comma-separated string to list of integers
                value_str = widget.get().strip()
                if value_str:
                    try:
                        value = [int(v.strip()) for v in value_str.split(',') if v.strip()]
                    except ValueError:
                        value = []
                else:
                    value = []
                self.character_model.set_value(bind_path, value)
        except Exception as e:
            print(f"Error updating model from widget {bind_path}: {e}")
    
    def refresh_all_widgets(self):
        """Refresh all bound widgets from the character model."""
        for bind_path, (widget, widget_type) in self.bound_widgets.items():
            self._update_widget_from_model(widget, bind_path, widget_type)
