#!/usr/bin/env python3
"""
UESRPG Session Manager - Character Window UI
Comprehensive UI implementation driven by ui_spec.json
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import logging
import traceback
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from copy import deepcopy
import re

logger = logging.getLogger(__name__)

# Check PIL availability once at module level
_PIL_AVAILABLE = False
_PIL_IMAGE = None
_PIL_IMAGETK = None

try:
    from PIL import Image, ImageTk
    _PIL_AVAILABLE = True
    _PIL_IMAGE = Image
    _PIL_IMAGETK = ImageTk
except ImportError:
    pass


class CharacterWindowUI:
    """Main Character Window UI - dynamically generated from spec."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the UI from spec."""
        self.root = root
        self.spec = None
        self.character_data = {}
        self.widgets = {}  # Maps bind paths to widgets
        self.validation_errors = []
        
        # Load spec
        self._load_spec()
        
        # Setup window
        self._setup_window()
        
        # Build UI
        self._build_ui()
        
        # Initialize with defaults
        self.reset_to_defaults()
        
        logger.info("Character Window UI initialized successfully")
    
    def _load_spec(self):
        """Load and parse the UI specification."""
        spec_path = Path(__file__).parent / "ui" / "ui_spec.json"
        logger.info(f"Loading spec from: {spec_path.absolute()}")
        
        try:
            with open(spec_path, 'r', encoding='utf-8') as f:
                self.spec = json.load(f)
            logger.info(f"Spec loaded successfully: version {self.spec.get('spec_version', 'unknown')}")
        except FileNotFoundError:
            logger.error(f"Spec file not found: {spec_path}")
            messagebox.showerror("Error", f"Spec file not found: {spec_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse spec: {e}")
            messagebox.showerror("Error", f"Failed to parse spec: {e}")
            raise
    
    def _setup_window(self):
        """Configure the main window."""
        # Window title
        window_config = self._find_character_window_config()
        title = window_config.get('title', 'Character')
        self.root.title(title)
        
        # Window size and properties
        app_config = self.spec.get('app', {})
        window_settings = app_config.get('window', {})
        
        size = window_settings.get('size', [1100, 720])
        self.root.geometry(f"{size[0]}x{size[1]}")
        
        min_size = window_settings.get('min_size', [980, 640])
        self.root.minsize(min_size[0], min_size[1])
        
        resizable = window_settings.get('resizable', True)
        self.root.resizable(resizable, resizable)
        
        # Apply theme colors
        self._apply_theme()
    
    def _apply_theme(self):
        """Apply theme colors and styling."""
        theme = self.spec.get('theme', {})
        colors = theme.get('colors', {})
        
        bg = colors.get('bg', '#FFD5AF')
        self.root.configure(bg=bg)
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for various widgets
        style.configure('TFrame', background=bg)
        style.configure('TLabelframe', background=bg, bordercolor=colors.get('border', '#9D6E6B'))
        style.configure('TLabelframe.Label', background=bg, foreground=colors.get('fg', '#9D6E6B'))
        style.configure('TLabel', background=bg, foreground=colors.get('fg', '#9D6E6B'))
        style.configure('TButton', background=colors.get('panel_bg', '#FFD5AF'))
        style.configure('TNotebook', background=bg)
        style.configure('TNotebook.Tab', background=colors.get('panel_bg', '#FFD5AF'))
    
    def _find_character_window_config(self) -> Dict:
        """Find the character window configuration in spec."""
        windows = self.spec.get('windows', [])
        for window in windows:
            if window.get('id') == 'character_window' or window.get('type') == 'main':
                return window
        return {}
    
    def _build_ui(self):
        """Build the main UI structure."""
        window_config = self._find_character_window_config()
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create main container with scrolling
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Check for new sheet_view layout
        if 'sheet_view' in window_config:
            # New character sheet dashboard layout
            self._build_sheet_view_layout(main_frame, window_config)
        elif 'layout' in window_config:
            # Legacy two-column layout (for backwards compatibility)
            layout = window_config.get('layout', {})
            layout_type = layout.get('type', 'grid')
            
            if layout_type == 'grid':
                columns = layout.get('columns', [])
                if len(columns) >= 2:
                    # Two-column layout with left panel and main panel
                    self._build_two_column_layout(main_frame, window_config, columns)
                else:
                    # Single column
                    self._build_single_column_layout(main_frame, window_config)
            else:
                self._build_single_column_layout(main_frame, window_config)
        else:
            self._build_single_column_layout(main_frame, window_config)
        
        # Create status bar
        self._create_status_bar()
    
    def _build_sheet_view_layout(self, parent, window_config):
        """Build the new character sheet dashboard layout."""
        # Create scrollable canvas for the sheet view
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        sheet_view = window_config.get('sheet_view', {})
        
        # Render header band
        if 'header' in sheet_view:
            header_frame = ttk.Frame(scrollable_frame)
            header_frame.pack(fill=tk.X, padx=10, pady=5)
            self._render_widget(header_frame, sheet_view['header'])
        
        # Render core band (3-column stats)
        if 'core' in sheet_view:
            core_frame = ttk.Frame(scrollable_frame)
            core_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self._render_widget(core_frame, sheet_view['core'])
        
        # Render content band (skills, etc.)
        if 'content' in sheet_view:
            content_frame = ttk.Frame(scrollable_frame)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self._render_widget(content_frame, sheet_view['content'])
        
        # Add details panel toggle button and notebook (collapsed by default)
        if 'details_panel' in window_config:
            details_toggle_frame = ttk.Frame(scrollable_frame)
            details_toggle_frame.pack(fill=tk.X, padx=10, pady=5)
            
            self.details_visible = tk.BooleanVar(value=False)
            self.details_notebook_frame = None
            
            toggle_btn = ttk.Button(
                details_toggle_frame,
                text="▶ Show Details (Gear, Magic, Notes...)",
                command=self._toggle_details_panel
            )
            toggle_btn.pack(side=tk.LEFT)
            
            # Create details panel frame (initially hidden)
            self.details_notebook_frame = ttk.Frame(scrollable_frame)
            self._build_details_panel(self.details_notebook_frame, window_config.get('details_panel'))
    
    def _toggle_details_panel(self):
        """Toggle visibility of the details notebook panel."""
        if self.details_visible.get():
            # Hide details
            self.details_notebook_frame.pack_forget()
            self.details_visible.set(False)
            # Update button text
            for widget in self.root.winfo_children():
                self._update_toggle_button_text(widget, False)
        else:
            # Show details
            self.details_notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.details_visible.set(True)
            # Update button text
            for widget in self.root.winfo_children():
                self._update_toggle_button_text(widget, True)
    
    def _update_toggle_button_text(self, widget, expanded):
        """Recursively update toggle button text."""
        if isinstance(widget, ttk.Button):
            current_text = widget.cget('text')
            if 'Show Details' in current_text or 'Hide Details' in current_text:
                if expanded:
                    widget.config(text="▼ Hide Details (Gear, Magic, Notes...)")
                else:
                    widget.config(text="▶ Show Details (Gear, Magic, Notes...)")
        for child in widget.winfo_children():
            self._update_toggle_button_text(child, expanded)
    
    def _build_details_panel(self, parent, panel_config):
        """Build the details notebook panel (legacy tabs)."""
        if not panel_config:
            return
        
        panel_type = panel_config.get('type', 'notebook')
        
        if panel_type == 'notebook':
            notebook = ttk.Notebook(parent)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            tabs = panel_config.get('tabs', [])
            for tab_config in tabs:
                self._create_tab(notebook, tab_config)
    
    def _create_tab(self, notebook, tab_config):
        """Create a single tab in the notebook."""
        tab_title = tab_config.get('title', 'Tab')
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text=tab_title)
        
        # Create scrollable area for tab
        tab_canvas = tk.Canvas(tab_frame)
        tab_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=tab_canvas.yview)
        tab_scrollable = ttk.Frame(tab_canvas)
        
        tab_scrollable.bind(
            "<Configure>",
            lambda e: tab_canvas.configure(scrollregion=tab_canvas.bbox("all"))
        )
        
        tab_canvas.create_window((0, 0), window=tab_scrollable, anchor="nw")
        tab_canvas.configure(yscrollcommand=tab_scrollbar.set)
        
        tab_canvas.pack(side="left", fill="both", expand=True)
        tab_scrollbar.pack(side="right", fill="y")
        
        # Build sections in tab
        sections = tab_config.get('sections', [])
        self._build_sections(tab_scrollable, sections)
    
    def _render_widget(self, parent, widget_config):
        """Recursively render a widget based on its type."""
        widget_type = widget_config.get('type', '')
        
        if widget_type == 'layout_row':
            # Horizontal layout container
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, expand=False, pady=5)
            widgets = widget_config.get('widgets', [])
            for child_config in widgets:
                child_frame = ttk.Frame(frame)
                child_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
                self._render_widget(child_frame, child_config)
        
        elif widget_type == 'layout_col':
            # Vertical layout container
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.BOTH, expand=True)
            widgets = widget_config.get('widgets', [])
            for child_config in widgets:
                self._render_widget(frame, child_config)
        
        elif widget_type == 'sheet_grid':
            # Grid layout for core stats (3 columns)
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            num_columns = widget_config.get('columns', 3)
            for i in range(num_columns):
                frame.columnconfigure(i, weight=1)
            
            widgets = widget_config.get('widgets', [])
            for idx, child_config in enumerate(widgets):
                col = idx % num_columns
                row = idx // num_columns
                child_frame = ttk.Frame(frame)
                child_frame.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
                self._render_widget(child_frame, child_config)
        
        elif widget_type == 'portrait_box':
            # Portrait display with fixed size
            self._render_portrait_box(parent, widget_config)
        
        elif widget_type == 'stat_block':
            # Individual stat display (large value + small label)
            self._render_stat_block(parent, widget_config)
        
        elif widget_type == 'group':
            # Group with title and children (same as existing implementation)
            title = widget_config.get('title', '')
            group_frame = ttk.LabelFrame(parent, text=title)
            group_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            layout = widget_config.get('layout', {})
            widgets = widget_config.get('widgets', [])
            self._build_widgets_with_layout(group_frame, widgets, layout)
        
        elif widget_type == 'field':
            # Regular field - use grid layout with single field
            self._build_widgets_with_layout(parent, [widget_config], {'type': 'grid', 'columns': 1})
        
        elif widget_type == 'table':
            # Table widget
            self._build_widgets_with_layout(parent, [widget_config], {'type': 'grid', 'columns': 1})
        
        elif widget_type == 'table_inline':
            # Inline table widget
            self._build_widgets_with_layout(parent, [widget_config], {'type': 'grid', 'columns': 1})
        
        else:
            logger.warning(f"Unknown widget type in _render_widget: {widget_type}")
    
    def _render_portrait_box(self, parent, config):
        """Render portrait box with fixed size 320x200."""
        frame = ttk.LabelFrame(parent, text="Portrait")
        frame.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=5)
        
        size = config.get('size', [320, 200])
        width, height = size
        
        # Create a frame with fixed size
        portrait_frame = ttk.Frame(frame, width=width, height=height)
        portrait_frame.pack_propagate(False)  # Prevent resizing
        portrait_frame.pack(padx=5, pady=5)
        
        # Try to load and display image, or show placeholder
        bind_path = config.get('bind', '')
        placeholder_text = config.get('placeholder', 'No portrait')
        
        # Create label widget based on PIL availability
        if _PIL_AVAILABLE:
            portrait_label = ttk.Label(portrait_frame, text=placeholder_text, anchor='center')
            portrait_label.pack(fill=tk.BOTH, expand=True)
            portrait_label._size = size
            portrait_label._has_pil = True
        else:
            # Fallback without PIL
            portrait_label = ttk.Label(portrait_frame, text=placeholder_text, anchor='center', 
                                      relief=tk.SUNKEN, background='#D0D0D0')
            portrait_label.pack(fill=tk.BOTH, expand=True)
            portrait_label._has_pil = False
        
        # Store reference for updates
        if bind_path:
            self.widgets[bind_path] = portrait_label
            portrait_label._bind_path = bind_path
            portrait_label._current_path = ''  # Initialize empty
            portrait_label._placeholder = placeholder_text
        
        # Add select button
        button_text = config.get('button_text', 'Select Portrait…')
        command_name = config.get('command', '')
        if command_name:
            btn = ttk.Button(frame, text=button_text,
                           command=lambda: self._handle_command(command_name))
            btn.pack(pady=5)
    
    def _render_stat_block(self, parent, config):
        """Render a stat block (large value + small label)."""
        label_text = config.get('label', '')
        bind_path = config.get('bind', '')
        
        # Create a frame for the stat block
        stat_frame = ttk.Frame(parent)
        stat_frame.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Label on top (small)
        label = ttk.Label(stat_frame, text=label_text, font=('TkDefaultFont', 8))
        label.pack()
        
        # Value entry below (larger)
        value_entry = ttk.Entry(stat_frame, width=6, font=('TkDefaultFont', 10, 'bold'),
                               justify='center')
        value_entry.pack()
        
        # Register widget for data binding
        if bind_path:
            self.widgets[bind_path] = value_entry
    
    def _create_menu_bar(self):
        """Create menu bar from spec."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menus_config = self.spec.get('menus', [])
        for menu_config in menus_config:
            menu_label = menu_config.get('label', '')
            menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=menu_label, menu=menu)
            
            items = menu_config.get('items', [])
            for item in items:
                if item.get('type') == 'separator':
                    menu.add_separator()
                else:
                    item_label = item.get('label', '')
                    command_name = item.get('command', '')
                    menu.add_command(label=item_label, command=lambda cmd=command_name: self._handle_command(cmd))
    
    def _create_status_bar(self):
        """Create status bar for messages."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _build_two_column_layout(self, parent, window_config, columns):
        """Build two-column layout (left panel + main panel)."""
        # Create left and right frames
        left_weight = columns[0].get('weight', 0)
        right_weight = columns[1].get('weight', 1)
        
        left_min = columns[0].get('min', 220)
        
        parent.columnconfigure(0, weight=left_weight, minsize=left_min)
        parent.columnconfigure(1, weight=right_weight)
        parent.rowconfigure(0, weight=1)
        
        # Left panel
        left_panel_config = window_config.get('left_panel', {})
        if left_panel_config:
            left_frame = ttk.LabelFrame(parent, text=left_panel_config.get('title', ''))
            left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=0)
            self._build_panel_widgets(left_frame, left_panel_config.get('widgets', []))
        
        # Main panel (right side)
        main_panel_config = window_config.get('main_panel', {})
        if main_panel_config:
            # Create scrollable frame for main panel
            canvas = tk.Canvas(parent)
            scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.grid(row=0, column=1, sticky='nsew')
            scrollbar.grid(row=0, column=1, sticky='nse')
            
            # Build main panel content
            self._build_main_panel(scrollable_frame, main_panel_config)
            
            # Enable mouse wheel scrolling
            MOUSE_WHEEL_DELTA = 120
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/MOUSE_WHEEL_DELTA)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _build_single_column_layout(self, parent, window_config):
        """Build single-column layout."""
        # Create scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Build main panel
        main_panel_config = window_config.get('main_panel', {})
        if main_panel_config:
            self._build_main_panel(scrollable_frame, main_panel_config)
    
    def _build_main_panel(self, parent, panel_config):
        """Build main panel content (tabs or sections)."""
        panel_type = panel_config.get('type', 'sections')
        
        if panel_type == 'notebook':
            # Create notebook (tabs)
            notebook = ttk.Notebook(parent)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            tabs = panel_config.get('tabs', [])
            logger.info(f"Building {len(tabs)} tabs")
            
            for tab_config in tabs:
                tab_title = tab_config.get('title', 'Tab')
                tab_frame = ttk.Frame(notebook)
                notebook.add(tab_frame, text=tab_title)
                
                # Create scrollable area for tab
                tab_canvas = tk.Canvas(tab_frame)
                tab_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=tab_canvas.yview)
                tab_scrollable = ttk.Frame(tab_canvas)
                
                tab_scrollable.bind(
                    "<Configure>",
                    lambda e, c=tab_canvas: c.configure(scrollregion=c.bbox("all"))
                )
                
                tab_canvas.create_window((0, 0), window=tab_scrollable, anchor="nw")
                tab_canvas.configure(yscrollcommand=tab_scrollbar.set)
                
                tab_canvas.pack(side="left", fill="both", expand=True)
                tab_scrollbar.pack(side="right", fill="y")
                
                # Build sections in tab
                sections = tab_config.get('sections', [])
                self._build_sections(tab_scrollable, sections)
        else:
            # Direct sections
            sections = panel_config.get('sections', [])
            self._build_sections(parent, sections)
    
    def _build_sections(self, parent, sections):
        """Build sections within a container."""
        for section_config in sections:
            section_title = section_config.get('title', '')
            section_frame = ttk.LabelFrame(parent, text=section_title)
            section_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)
            
            widgets = section_config.get('widgets', [])
            layout = section_config.get('layout', {})
            
            self._build_widgets_with_layout(section_frame, widgets, layout)
    
    def _build_widgets_with_layout(self, parent, widgets, layout):
        """Build widgets with specified layout."""
        layout_type = layout.get('type', 'grid')
        columns = layout.get('columns', 1)
        
        if layout_type == 'grid':
            # Configure columns
            if isinstance(columns, int):
                for i in range(columns):
                    parent.columnconfigure(i, weight=1)
            
            row = 0
            col = 0
            
            for widget_config in widgets:
                try:
                    widget_type = widget_config.get('type', 'field')
                    colspan = widget_config.get('colspan', 1)
                    
                    if widget_type == 'field':
                        self._create_field_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'table':
                        self._create_table_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'table_inline':
                        self._create_table_inline_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'group':
                        self._create_group_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'button':
                        self._create_button_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'image':
                        self._create_image_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'label':
                        self._create_label_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'stat_block':
                        self._create_stat_block_widget(parent, widget_config, row, col, colspan)
                    elif widget_type == 'preview':
                        self._create_preview_widget(parent, widget_config, row, col, colspan)
                    else:
                        logger.warning(f"Unsupported widget type: {widget_type}")
                        self._create_placeholder_widget(parent, widget_config, row, col, colspan)
                    
                    # Update position
                    col += colspan
                    if isinstance(columns, int) and col >= columns:
                        col = 0
                        row += 1
                except Exception as e:
                    logger.error(f"Failed to create widget: {e}", exc_info=True)
                    # Create placeholder on error
                    self._create_placeholder_widget(parent, widget_config, row, col, 1)
                    col += 1
                    if isinstance(columns, int) and col >= columns:
                        col = 0
                        row += 1
        else:
            # Pack layout
            for widget_config in widgets:
                try:
                    widget_type = widget_config.get('type', 'field')
                    
                    if widget_type == 'field':
                        # For pack layout, create in a frame
                        frame = ttk.Frame(parent)
                        frame.pack(fill=tk.X, padx=5, pady=2)
                        self._create_field_widget(frame, widget_config, 0, 0, 1)
                    else:
                        logger.warning(f"Widget type {widget_type} not fully supported in pack layout")
                except Exception as e:
                    logger.error(f"Failed to create widget: {e}", exc_info=True)
    
    def _create_field_widget(self, parent, config, row, col, colspan):
        """Create a field widget (label + input)."""
        label_text = config.get('label', '')
        bind_path = config.get('bind', '')
        widget_type = config.get('widget', 'entry')
        hint = config.get('hint', '')
        
        # Create label
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=col, sticky='w', padx=5, pady=2)
        
        # Create input widget
        input_frame = ttk.Frame(parent)
        input_frame.grid(row=row+1, column=col, columnspan=colspan, sticky='ew', padx=5, pady=2)
        
        widget = None
        
        if widget_type == 'entry':
            widget = ttk.Entry(input_frame)
            widget.pack(fill=tk.X, expand=True)
        elif widget_type == 'textarea':
            height = config.get('height', 4)
            widget = scrolledtext.ScrolledText(input_frame, height=height, wrap=tk.WORD)
            widget.pack(fill=tk.BOTH, expand=True)
        elif widget_type == 'spin_int':
            min_val = config.get('min', 0)
            max_val = config.get('max', 999999)
            widget = ttk.Spinbox(input_frame, from_=min_val, to=max_val)
            widget.pack(fill=tk.X, expand=True)
        elif widget_type == 'check':
            var = tk.BooleanVar()
            widget = ttk.Checkbutton(input_frame, variable=var)
            widget.var = var
            widget.pack(anchor=tk.W)
        elif widget_type == 'tags':
            # Tags widget (comma-separated list)
            widget = ttk.Entry(input_frame)
            widget.pack(fill=tk.X, expand=True)
            widget._is_tags = True
        elif widget_type == 'int_list_csv':
            # Integer list CSV
            widget = ttk.Entry(input_frame)
            widget.pack(fill=tk.X, expand=True)
            widget._is_int_list_csv = True
        elif widget_type == 'readonly_entry':
            widget = ttk.Entry(input_frame, state='readonly')
            widget.pack(fill=tk.X, expand=True)
        else:
            logger.warning(f"Unsupported widget type: {widget_type}")
            widget = ttk.Entry(input_frame, state='disabled')
            widget.pack(fill=tk.X, expand=True)
        
        if widget and bind_path:
            self.widgets[bind_path] = widget
        
        # Add hint if provided
        if hint:
            hint_label = ttk.Label(input_frame, text=hint, font=('TkDefaultFont', 8))
            hint_label.pack(anchor=tk.W)
    
    def _create_table_widget(self, parent, config, row, col, colspan):
        """Create a table widget for list editing."""
        title = config.get('title', '')
        bind_path = config.get('bind', '')
        
        # Create labeled frame
        table_frame = ttk.LabelFrame(parent, text=title)
        table_frame.grid(row=row, column=col, columnspan=colspan, rowspan=3, sticky='nsew', padx=5, pady=5)
        
        # Create treeview for table
        columns_config = config.get('columns', [])
        column_ids = [c.get('key', '') for c in columns_config]
        column_labels = [c.get('label', '') for c in columns_config]
        column_widths = [c.get('width', 10) for c in columns_config]
        
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree = ttk.Treeview(tree_frame, columns=column_ids, show='headings', height=5)
        
        for cid, label, width in zip(column_ids, column_labels, column_widths):
            tree.heading(cid, text=label)
            tree.column(cid, width=width*10, minwidth=width*5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Store table widget
        if bind_path:
            tree._table_config = config
            tree._column_ids = column_ids
            self.widgets[bind_path] = tree
        
        # Add buttons for row editing
        row_editor = config.get('row_editor', {})
        if row_editor:
            button_frame = ttk.Frame(table_frame)
            button_frame.pack(fill=tk.X, padx=5, pady=5)
            
            buttons = row_editor.get('buttons', ['add', 'update', 'delete'])
            if 'add' in buttons:
                ttk.Button(button_frame, text="Add", command=lambda: self._table_add_row(tree, config)).pack(side=tk.LEFT, padx=2)
            if 'update' in buttons:
                ttk.Button(button_frame, text="Edit", command=lambda: self._table_edit_row(tree, config)).pack(side=tk.LEFT, padx=2)
            if 'delete' in buttons:
                ttk.Button(button_frame, text="Delete", command=lambda: self._table_delete_row(tree)).pack(side=tk.LEFT, padx=2)
    
    def _create_table_inline_widget(self, parent, config, row, col, colspan):
        """Create an inline table widget (fixed rows, editable cells)."""
        bind_path = config.get('bind', '')
        columns_config = config.get('columns', [])
        mode = config.get('mode', 'list')
        
        # Create frame for table
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=row, column=col, columnspan=colspan, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Create headers
        header_frame = ttk.Frame(table_frame)
        header_frame.pack(fill=tk.X)
        
        col_idx = 0
        for column in columns_config:
            label = column.get('label', '')
            width = column.get('width', 10)
            header = ttk.Label(header_frame, text=label, width=width)
            header.grid(row=0, column=col_idx, padx=2, pady=2)
            col_idx += 1
        
        # Create data frame
        data_frame = ttk.Frame(table_frame)
        data_frame.pack(fill=tk.BOTH, expand=True)
        
        # Store reference for later data binding
        if bind_path:
            data_frame._table_inline_config = config
            data_frame._columns_config = columns_config
            data_frame._mode = mode
            self.widgets[bind_path] = data_frame
    
    def _create_group_widget(self, parent, config, row, col, colspan):
        """Create a group widget (nested fields)."""
        title = config.get('title', '')
        group_frame = ttk.LabelFrame(parent, text=title)
        group_frame.grid(row=row, column=col, columnspan=colspan, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        widgets = config.get('widgets', [])
        layout = config.get('layout', {})
        
        self._build_widgets_with_layout(group_frame, widgets, layout)
    
    def _create_button_widget(self, parent, config, row, col, colspan):
        """Create a button widget."""
        text = config.get('text', 'Button')
        command_name = config.get('command', '')
        
        button = ttk.Button(parent, text=text, command=lambda: self._handle_command(command_name))
        button.grid(row=row, column=col, columnspan=colspan, sticky='ew', padx=5, pady=5)
    
    def _create_image_widget(self, parent, config, row, col, colspan):
        """Create an image widget (portrait)."""
        bind_path = config.get('bind', '')
        placeholder_text = config.get('placeholder', 'No image')
        max_size = config.get('max_size', [200, 240])
        
        image_frame = ttk.Frame(parent)
        image_frame.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=5, pady=5)
        
        # Create label for image
        image_label = ttk.Label(image_frame, text=placeholder_text, relief=tk.SUNKEN)
        image_label.pack(fill=tk.BOTH, expand=True)
        
        if bind_path:
            image_label._max_size = max_size
            image_label._placeholder = placeholder_text
            self.widgets[bind_path] = image_label
    
    def _create_label_widget(self, parent, config, row, col, colspan):
        """Create a label widget."""
        text = config.get('text', '')
        label = ttk.Label(parent, text=text, wraplength=200)
        label.grid(row=row, column=col, columnspan=colspan, sticky='w', padx=5, pady=2)
    
    def _create_preview_widget(self, parent, config, row, col, colspan):
        """Create a preview widget (read-only text area for displaying data)."""
        bind_path = config.get('bind', '')
        height = config.get('height', 10)
        
        # Create preview text area
        preview_text = scrolledtext.ScrolledText(parent, height=height, wrap=tk.WORD, state='disabled')
        preview_text.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=5, pady=2)
        
        # Register widget for data binding
        if bind_path:
            self.widgets[bind_path] = preview_text
    
    def _create_placeholder_widget(self, parent, config, row, col, colspan):
        """Create a placeholder for unsupported widgets."""
        label_text = config.get('label', 'Unsupported')
        widget_type = config.get('type', 'unknown')
        
        label = ttk.Label(parent, text=f"{label_text} [{widget_type}]", foreground='gray')
        label.grid(row=row, column=col, columnspan=colspan, sticky='w', padx=5, pady=2)
    
    def _build_panel_widgets(self, parent, widgets):
        """Build widgets for a panel (left panel)."""
        for widget_config in widgets:
            widget_type = widget_config.get('type', 'label')
            
            if widget_type == 'image':
                self._create_image_widget_pack(parent, widget_config)
            elif widget_type == 'button':
                self._create_button_widget_pack(parent, widget_config)
            elif widget_type == 'label':
                self._create_label_widget_pack(parent, widget_config)
    
    def _create_image_widget_pack(self, parent, config):
        """Create image widget with pack layout."""
        bind_path = config.get('bind', '')
        placeholder_text = config.get('placeholder', 'No image')
        max_size = config.get('max_size', [200, 240])
        
        image_label = ttk.Label(parent, text=placeholder_text, relief=tk.SUNKEN, width=25, anchor=tk.CENTER)
        image_label.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        
        if bind_path:
            image_label._max_size = max_size
            image_label._placeholder = placeholder_text
            self.widgets[bind_path] = image_label
    
    def _create_button_widget_pack(self, parent, config):
        """Create button widget with pack layout."""
        text = config.get('text', 'Button')
        command_name = config.get('command', '')
        
        button = ttk.Button(parent, text=text, command=lambda: self._handle_command(command_name))
        button.pack(padx=5, pady=5, fill=tk.X)
    
    def _create_label_widget_pack(self, parent, config):
        """Create label widget with pack layout."""
        text = config.get('text', '')
        label = ttk.Label(parent, text=text, wraplength=200)
        label.pack(padx=5, pady=5, anchor=tk.W)
    
    def _create_stat_block_widget(self, parent, config, row, col, colspan):
        """Create a stat block widget for grid layout (large value + small label)."""
        label_text = config.get('label', '')
        bind_path = config.get('bind', '')
        
        # Create a frame for the stat block
        stat_frame = ttk.Frame(parent)
        stat_frame.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=5, pady=2)
        
        # Label on top (small)
        label = ttk.Label(stat_frame, text=label_text, font=('TkDefaultFont', 8))
        label.pack()
        
        # Value entry below (larger)
        value_entry = ttk.Entry(stat_frame, width=6, font=('TkDefaultFont', 10, 'bold'),
                               justify='center')
        value_entry.pack()
        
        # Register widget for data binding
        if bind_path:
            self.widgets[bind_path] = value_entry
    
    def _handle_command(self, command_name: str):
        """Handle menu/button commands."""
        logger.info(f"Command: {command_name}")
        
        try:
            if command_name == 'file_new':
                self.reset_to_defaults()
            elif command_name == 'file_open':
                self.load_character()
            elif command_name == 'file_save':
                self.save_character()
            elif command_name == 'file_save_as':
                self.save_character_as()
            elif command_name == 'app_exit':
                self.root.quit()
            elif command_name == 'select_portrait_from_dir':
                self.select_portrait()
            elif command_name == 'import_base_data' or command_name == 'import_character_data':
                self.show_import_dialog()
            elif command_name == 'export_character_data':
                self.export_character_data()
            elif command_name == 'import_choose_json':
                self.import_choose_json()
            elif command_name == 'import_apply':
                self.import_apply()
            elif command_name == 'dialog_close':
                self.close_dialog()
            else:
                logger.warning(f"Unknown command: {command_name}")
                messagebox.showwarning("Warning", f"Command not implemented: {command_name}")
        except Exception as e:
            logger.error(f"Error handling command {command_name}: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to execute command: {e}")
    
    def get_state(self) -> Dict:
        """Extract current UI state into a dictionary."""
        state = {}
        
        for bind_path, widget in self.widgets.items():
            try:
                value = self._get_widget_value(widget)
                self._set_nested_value(state, bind_path, value)
            except Exception as e:
                logger.error(f"Failed to extract value from widget at {bind_path}: {e}")
        
        return state
    
    def _get_widget_value(self, widget):
        """Get value from a widget."""
        if isinstance(widget, ttk.Entry):
            value = widget.get()
            if hasattr(widget, '_is_tags'):
                # Parse comma-separated tags
                return [t.strip() for t in value.split(',') if t.strip()]
            elif hasattr(widget, '_is_int_list_csv'):
                # Parse comma-separated integers
                parts = [p.strip() for p in value.split(',') if p.strip()]
                return [int(p) for p in parts if p.isdigit() or (p.startswith('-') and p[1:].isdigit())]
            return value
        elif isinstance(widget, scrolledtext.ScrolledText):
            return widget.get('1.0', tk.END).strip()
        elif isinstance(widget, ttk.Spinbox):
            val = widget.get()
            try:
                return int(val) if val else 0
            except ValueError:
                return 0
        elif isinstance(widget, ttk.Checkbutton):
            return widget.var.get()
        elif isinstance(widget, ttk.Treeview):
            # Table widget - get all rows
            items = []
            for item_id in widget.get_children():
                values = widget.item(item_id)['values']
                column_ids = widget._column_ids
                row_dict = {cid: val for cid, val in zip(column_ids, values)}
                items.append(row_dict)
            return items
        elif isinstance(widget, ttk.Frame) and hasattr(widget, '_table_inline_config'):
            # Inline table - get values from child widgets
            return self._get_inline_table_values(widget)
        elif isinstance(widget, ttk.Label) and hasattr(widget, '_bind_path') and 'portrait' in widget._bind_path:
            # Portrait image widget - return stored path
            if hasattr(widget, '_current_path'):
                return widget._current_path
            # Fallback to text content if no path stored
            text = widget.cget('text')
            return text if text and text != getattr(widget, '_placeholder', '') else ''
        elif isinstance(widget, ttk.Label):
            # Image widget - just return the path
            return widget.cget('text') if hasattr(widget, '_placeholder') else ''
        else:
            return None
    
    def _get_inline_table_values(self, frame):
        """Get values from an inline table widget."""
        # This is complex - would need to iterate through child widgets
        # For now, return empty or existing data
        return []
    
    def set_state(self, state: Dict):
        """Apply a dictionary state to the UI."""
        for bind_path, widget in self.widgets.items():
            try:
                value = self._get_nested_value(state, bind_path)
                if value is not None:
                    self._set_widget_value(widget, value)
            except Exception as e:
                logger.warning(f"Failed to set widget value at {bind_path}: {e}")
    
    def _set_widget_value(self, widget, value):
        """Set value to a widget."""
        if isinstance(widget, ttk.Entry):
            widget.delete(0, tk.END)
            if hasattr(widget, '_is_tags') and isinstance(value, list):
                widget.insert(0, ', '.join(str(v) for v in value))
            elif hasattr(widget, '_is_int_list_csv') and isinstance(value, list):
                widget.insert(0, ', '.join(str(v) for v in value))
            else:
                widget.insert(0, str(value) if value is not None else '')
        elif isinstance(widget, scrolledtext.ScrolledText):
            # Enable widget temporarily if disabled
            original_state = widget.cget('state')
            if original_state == 'disabled':
                widget.config(state='normal')
            widget.delete('1.0', tk.END)
            widget.insert('1.0', str(value) if value is not None else '')
            # Restore original state
            if original_state == 'disabled':
                widget.config(state='disabled')
        elif isinstance(widget, ttk.Spinbox):
            widget.delete(0, tk.END)
            widget.insert(0, str(value) if value is not None else '0')
        elif isinstance(widget, ttk.Checkbutton):
            widget.var.set(bool(value))
        elif isinstance(widget, ttk.Treeview):
            # Clear and populate table
            for item in widget.get_children():
                widget.delete(item)
            if isinstance(value, list):
                column_ids = widget._column_ids
                for row in value:
                    values = [row.get(cid, '') for cid in column_ids]
                    widget.insert('', tk.END, values=values)
        elif isinstance(widget, ttk.Frame) and hasattr(widget, '_table_inline_config'):
            # Set inline table values
            self._set_inline_table_values(widget, value)
        elif isinstance(widget, ttk.Label) and hasattr(widget, '_bind_path') and 'portrait' in widget._bind_path:
            # Portrait image widget with PIL support
            if value and isinstance(value, str):
                widget._current_path = value  # Store path for get_state
                self._load_portrait_image(widget, value)
            else:
                # Show placeholder
                widget._current_path = ''
                placeholder = getattr(widget, '_placeholder', 'No portrait')
                widget.config(text=placeholder, image='')
        elif isinstance(widget, ttk.Label) and hasattr(widget, '_placeholder'):
            # Generic image widget
            if value:
                widget.config(text=str(value))
            else:
                widget.config(text=widget._placeholder)
    
    def _load_portrait_image(self, label_widget, image_path):
        """Load and display a portrait image with PIL, or show path as fallback."""
        if not image_path or not Path(image_path).exists():
            # File doesn't exist, show placeholder
            placeholder = getattr(label_widget, '_placeholder', 'No portrait')
            label_widget.config(text=placeholder, image='')
            return
        
        # Check if PIL is available
        if not _PIL_AVAILABLE or not hasattr(label_widget, '_has_pil') or not label_widget._has_pil:
            # Fallback: show filename
            label_widget.config(text=Path(image_path).name)
            return
        
        try:
            # Get target size
            target_size = getattr(label_widget, '_size', [320, 200])
            target_width, target_height = target_size
            
            # Load image
            img = _PIL_IMAGE.open(image_path)
            
            # Calculate aspect ratios
            img_aspect = img.width / img.height
            target_aspect = target_width / target_height
            
            # Letterbox approach: fit image inside target size maintaining aspect ratio
            if img_aspect > target_aspect:
                # Image is wider - fit to width
                new_width = target_width
                new_height = int(target_width / img_aspect)
            else:
                # Image is taller - fit to height
                new_height = target_height
                new_width = int(target_height * img_aspect)
            
            # Resize image
            img = img.resize((new_width, new_height), _PIL_IMAGE.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = _PIL_IMAGETK.PhotoImage(img)
            
            # Update label
            label_widget.config(image=photo, text='')
            # Keep a reference to prevent garbage collection
            label_widget.image = photo
            
        except Exception as e:
            logger.error(f"Failed to load portrait image {image_path}: {e}")
            # Fallback to showing filename
            label_widget.config(text=Path(image_path).name, image='')
    
    def _set_inline_table_values(self, frame, values):
        """Set values to an inline table widget."""
        config = frame._table_inline_config
        columns_config = frame._columns_config
        mode = frame._mode
        
        # Clear existing widgets
        for child in frame.winfo_children():
            child.destroy()
        
        if mode == 'keyed_object' and isinstance(values, dict):
            # Fixed rows based on spec
            rows_config = config.get('rows', [])
            row_idx = 0
            
            for row_config in rows_config:
                key = row_config.get('key', '')
                label = row_config.get('label', key)
                
                # Row label
                row_label = ttk.Label(frame, text=label, width=15)
                row_label.grid(row=row_idx, column=0, padx=2, pady=1, sticky='w')
                
                # Get row data
                row_data = values.get(key, {})
                
                # Create input widgets for each column
                col_idx = 1
                for column in columns_config:
                    col_key = column.get('key', '')
                    width = column.get('width', 10)
                    widget_type = column.get('widget', 'entry')
                    
                    if widget_type == 'check':
                        var = tk.BooleanVar(value=row_data.get(col_key, False))
                        widget = ttk.Checkbutton(frame, variable=var)
                        widget.var = var
                    else:
                        widget = ttk.Entry(frame, width=width)
                        widget.insert(0, str(row_data.get(col_key, '')))
                        
                        if column.get('readonly'):
                            widget.config(state='readonly')
                    
                    widget.grid(row=row_idx, column=col_idx, padx=2, pady=1)
                    
                    # Store widget reference
                    widget._inline_key = key
                    widget._inline_col = col_key
                    
                    col_idx += 1
                
                row_idx += 1
        
        elif isinstance(values, list):
            # List mode - similar to table
            row_idx = 0
            for row_data in values:
                col_idx = 0
                for column in columns_config:
                    col_key = column.get('key', '')
                    width = column.get('width', 10)
                    readonly = column.get('readonly', False)
                    widget_type = column.get('widget', 'entry')
                    
                    if widget_type == 'check':
                        var = tk.BooleanVar(value=row_data.get(col_key, False))
                        widget = ttk.Checkbutton(frame, variable=var)
                        widget.var = var
                    else:
                        widget = ttk.Entry(frame, width=width)
                        widget.insert(0, str(row_data.get(col_key, '')))
                        
                        if readonly:
                            widget.config(state='readonly')
                    
                    widget.grid(row=row_idx, column=col_idx, padx=2, pady=1)
                    col_idx += 1
                
                row_idx += 1
    
    def reset_to_defaults(self):
        """Reset UI to default values from spec."""
        try:
            default_data = self.spec.get('data', {}).get('default_character', {})
            self.character_data = deepcopy(default_data)
            self.set_state(self.character_data)
            self.status_var.set("Reset to defaults")
            logger.info("Reset to defaults")
        except Exception as e:
            logger.error(f"Error resetting to defaults: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to reset: {e}")
    
    def deep_merge(self, base: Dict, overlay: Dict, overwrite: bool = True) -> Dict:
        """
        Deep merge two dictionaries.
        
        Args:
            base: Base dictionary (e.g., default_character schema)
            overlay: Overlay dictionary (e.g., imported data)
            overwrite: If True, overlay values replace base values.
                      If False, only fill missing/empty fields in base.
        
        Returns:
            Merged dictionary
        """
        result = deepcopy(base)
        
        for key, value in overlay.items():
            if key not in result:
                # Key doesn't exist in base, add it
                result[key] = deepcopy(value)
            elif isinstance(value, dict) and isinstance(result[key], dict):
                # Both are dicts, merge recursively
                result[key] = self.deep_merge(result[key], value, overwrite)
            elif isinstance(value, list) and isinstance(result[key], list):
                # Both are lists
                if overwrite:
                    result[key] = deepcopy(value)
                elif len(result[key]) == 0:
                    # Only overwrite if base list is empty
                    result[key] = deepcopy(value)
            else:
                # Scalar values
                if overwrite:
                    result[key] = deepcopy(value)
                elif result[key] in ('', None):
                    # Only overwrite if base value is empty string or None
                    # Preserves legitimate falsy values like 0, False, []
                    result[key] = deepcopy(value)
        
        return result
    
    def load_character(self):
        """Load character from JSON file."""
        try:
            filename = filedialog.askopenfilename(
                title="Load Character",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.character_data = data
            self.set_state(data)
            self.status_var.set(f"Loaded: {Path(filename).name}")
            logger.info(f"Loaded character from {filename}")
        except Exception as e:
            logger.error(f"Error loading character: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to load character: {e}")
    
    def save_character(self):
        """Save character to the current file or prompt for new file."""
        # For now, always prompt
        self.save_character_as()
    
    def save_character_as(self):
        """Save character to a new JSON file."""
        try:
            filename = filedialog.asksaveasfilename(
                title="Save Character",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Get current state
            state = self.get_state()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            self.status_var.set(f"Saved: {Path(filename).name}")
            logger.info(f"Saved character to {filename}")
            messagebox.showinfo("Success", "Character saved successfully")
        except Exception as e:
            logger.error(f"Error saving character: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to save character: {e}")
    
    def export_character_data(self):
        """
        Export character data to JSON file.
        
        This is a wrapper around save_character_as() to provide a distinct
        menu entry for export operations. Per requirements, it uses the same
        underlying save functionality but maintains menu separation for clarity.
        """
        self.save_character_as()
    
    def show_import_dialog(self):
        """Show the import character data dialog."""
        try:
            # Find the import_window spec
            import_window_spec = None
            for window in self.spec.get('windows', []):
                if window.get('id') == 'import_window':
                    import_window_spec = window
                    break
            
            if not import_window_spec:
                messagebox.showerror("Error", "Import window spec not found")
                return
            
            # Create dialog
            self.import_dialog = tk.Toplevel(self.root)
            self.import_dialog.title(import_window_spec.get('title', 'Import Character Data'))
            self.import_dialog.transient(self.root)
            self.import_dialog.grab_set()
            
            # Initialize dialog state
            self.dialog_state = {
                'selected_path': '',
                'preview': '',
                'overwrite': True,
                'loaded_data': None
            }
            
            # Store original widgets dict and create a new one for dialog
            self.original_widgets = self.widgets
            self.dialog_widgets = {}
            self.widgets = self.dialog_widgets
            
            # Build dialog widgets
            layout = import_window_spec.get('layout', {'type': 'grid', 'columns': 2})
            widgets_config = import_window_spec.get('widgets', [])
            self._build_widgets_with_layout(self.import_dialog, widgets_config, layout)
            
            # Set dialog state
            self._set_dialog_state(self.dialog_state)
            
            # Restore original widgets
            self.widgets = self.original_widgets
            
        except Exception as e:
            logger.error(f"Error showing import dialog: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to show import dialog: {e}")
            if hasattr(self, 'original_widgets'):
                self.widgets = self.original_widgets
    
    def import_choose_json(self):
        """Choose a JSON file for import."""
        try:
            filename = filedialog.askopenfilename(
                title="Choose Character JSON",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Load the JSON
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update dialog state
            self.dialog_state['selected_path'] = filename
            self.dialog_state['loaded_data'] = data
            
            # Generate preview
            preview_text = json.dumps(data, indent=2, ensure_ascii=False)
            # Truncate if too large
            if len(preview_text) > 2000:
                preview_text = preview_text[:2000] + "\n... (truncated)"
            
            self.dialog_state['preview'] = preview_text
            
            # Update dialog widgets
            self._set_dialog_state(self.dialog_state)
            
        except Exception as e:
            logger.error(f"Error choosing JSON: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to load JSON: {e}")
    
    def import_apply(self):
        """Apply the import with the selected options."""
        try:
            if not self.dialog_state.get('loaded_data'):
                messagebox.showwarning("Warning", "No file selected")
                return
            
            # Get default character schema
            default_data = self.spec.get('data', {}).get('default_character', {})
            
            # Get loaded data and overwrite setting
            loaded_data = self.dialog_state['loaded_data']
            overwrite = self.dialog_state.get('overwrite', True)
            
            # Merge with deep_merge
            merged_data = self.deep_merge(default_data, loaded_data, overwrite=overwrite)
            
            # Restore original widgets
            self.widgets = self.original_widgets
            
            # Apply to UI
            self.character_data = merged_data
            self.set_state(merged_data)
            
            # Close dialog
            self.import_dialog.destroy()
            
            # Update status
            filename = Path(self.dialog_state['selected_path']).name
            self.status_var.set(f"Imported: {filename}")
            logger.info(f"Imported character from {self.dialog_state['selected_path']}")
            messagebox.showinfo("Success", "Character data imported successfully")
            
        except Exception as e:
            logger.error(f"Error importing character: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to import character: {e}")
            if hasattr(self, 'original_widgets'):
                self.widgets = self.original_widgets
    
    def close_dialog(self):
        """Close the current dialog."""
        try:
            if hasattr(self, 'import_dialog'):
                # Restore original widgets
                if hasattr(self, 'original_widgets'):
                    self.widgets = self.original_widgets
                self.import_dialog.destroy()
        except Exception as e:
            logger.error(f"Error closing dialog: {e}", exc_info=True)
    
    def _set_dialog_state(self, state: Dict):
        """Set values in dialog widgets from state dict."""
        for bind_path, value in state.items():
            widget_path = f"$dialog.{bind_path}"
            if widget_path in self.dialog_widgets:
                widget = self.dialog_widgets[widget_path]
                self._set_widget_value(widget, value)
    
    def select_portrait(self):
        """Select portrait from directory."""
        try:
            portrait_dir = self.spec.get('data', {}).get('portrait_dir', 'uesrpg_sm/assets/portraits')
            portrait_path = Path(portrait_dir)
            
            # Try to use portrait directory if it exists
            initial_dir = str(portrait_path) if portrait_path.exists() else None
            
            filename = filedialog.askopenfilename(
                title="Select Portrait",
                initialdir=initial_dir,
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Store the full path
            portrait_path_str = filename
            
            # Update the portrait field
            portrait_bind = "$.portrait.file"
            if portrait_bind in self.widgets:
                portrait_widget = self.widgets[portrait_bind]
                # Load and display the image
                self._load_portrait_image(portrait_widget, portrait_path_str)
                # Also update the text value for state management
                if hasattr(portrait_widget, '_current_path'):
                    portrait_widget._current_path = portrait_path_str
            
            self.status_var.set(f"Portrait selected: {Path(filename).name}")
        except Exception as e:
            logger.error(f"Error selecting portrait: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to select portrait: {e}")
    
    def _table_add_row(self, tree, config):
        """Add new row to table."""
        try:
            # Show dialog to add row
            dialog = tk.Toplevel(self.root)
            dialog.title("Add Row")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Get row editor configuration
            row_editor = config.get('row_editor', {})
            fields = row_editor.get('fields', [])
            columns_config = config.get('columns', [])
            
            # If no explicit fields, use columns
            if not fields:
                fields = [{'label': col.get('label', ''), 'key': col.get('key', ''), 'widget': 'entry'} 
                          for col in columns_config]
            
            # Create input fields
            entries = {}
            row = 0
            for field in fields:
                label = field.get('label', '')
                key = field.get('key', '')
                widget_type = field.get('widget', 'entry')
                
                ttk.Label(dialog, text=label).grid(row=row, column=0, padx=5, pady=5, sticky='e')
                
                if widget_type == 'entry':
                    entry = ttk.Entry(dialog)
                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
                    entries[key] = entry
                elif widget_type == 'spin_int':
                    min_val = field.get('min', 0)
                    max_val = field.get('max', 999)
                    entry = ttk.Spinbox(dialog, from_=min_val, to=max_val)
                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
                    entries[key] = entry
                elif widget_type == 'tags':
                    entry = ttk.Entry(dialog)
                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
                    entry._is_tags = True
                    entries[key] = entry
                
                row += 1
            
            dialog.columnconfigure(1, weight=1)
            
            # Add buttons
            def on_add():
                values = []
                for col in columns_config:
                    key = col.get('key', '')
                    if key in entries:
                        entry = entries[key]
                        if hasattr(entry, '_is_tags'):
                            value = [t.strip() for t in entry.get().split(',') if t.strip()]
                        else:
                            value = entry.get()
                        values.append(value)
                    else:
                        values.append('')
                
                tree.insert('', tk.END, values=values)
                dialog.destroy()
            
            button_frame = ttk.Frame(dialog)
            button_frame.grid(row=row, column=0, columnspan=2, pady=10)
            ttk.Button(button_frame, text="Add", command=on_add).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            logger.error(f"Error adding row: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to add row: {e}")
    
    def _table_edit_row(self, tree, config):
        """Edit selected row in table."""
        try:
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a row to edit")
                return
            
            item_id = selection[0]
            values = tree.item(item_id)['values']
            
            # Show dialog to edit row
            dialog = tk.Toplevel(self.root)
            dialog.title("Edit Row")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Get row editor configuration
            row_editor = config.get('row_editor', {})
            fields = row_editor.get('fields', [])
            columns_config = config.get('columns', [])
            
            # If no explicit fields, use columns
            if not fields:
                fields = [{'label': col.get('label', ''), 'key': col.get('key', ''), 'widget': 'entry'} 
                          for col in columns_config]
            
            # Create input fields
            entries = {}
            row = 0
            for idx, field in enumerate(fields):
                label = field.get('label', '')
                key = field.get('key', '')
                widget_type = field.get('widget', 'entry')
                
                # Get existing value
                existing_value = values[idx] if idx < len(values) else ''
                
                ttk.Label(dialog, text=label).grid(row=row, column=0, padx=5, pady=5, sticky='e')
                
                if widget_type == 'entry':
                    entry = ttk.Entry(dialog)
                    entry.insert(0, str(existing_value))
                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
                    entries[key] = entry
                elif widget_type == 'spin_int':
                    min_val = field.get('min', 0)
                    max_val = field.get('max', 999)
                    entry = ttk.Spinbox(dialog, from_=min_val, to=max_val)
                    entry.insert(0, str(existing_value))
                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
                    entries[key] = entry
                elif widget_type == 'tags':
                    entry = ttk.Entry(dialog)
                    if isinstance(existing_value, list):
                        entry.insert(0, ', '.join(str(v) for v in existing_value))
                    else:
                        entry.insert(0, str(existing_value))
                    entry.grid(row=row, column=1, padx=5, pady=5, sticky='ew')
                    entry._is_tags = True
                    entries[key] = entry
                
                row += 1
            
            dialog.columnconfigure(1, weight=1)
            
            # Add buttons
            def on_update():
                new_values = []
                for col in columns_config:
                    key = col.get('key', '')
                    if key in entries:
                        entry = entries[key]
                        if hasattr(entry, '_is_tags'):
                            value = [t.strip() for t in entry.get().split(',') if t.strip()]
                        else:
                            value = entry.get()
                        new_values.append(value)
                    else:
                        new_values.append('')
                
                tree.item(item_id, values=new_values)
                dialog.destroy()
            
            button_frame = ttk.Frame(dialog)
            button_frame.grid(row=row, column=0, columnspan=2, pady=10)
            ttk.Button(button_frame, text="Update", command=on_update).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            logger.error(f"Error editing row: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to edit row: {e}")
    
    def _table_delete_row(self, tree):
        """Delete selected row from table."""
        try:
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a row to delete")
                return
            
            if messagebox.askyesno("Confirm", "Delete selected row?"):
                for item_id in selection:
                    tree.delete(item_id)
        except Exception as e:
            logger.error(f"Error deleting row: {e}", exc_info=True)
            messagebox.showerror("Error", f"Failed to delete row: {e}")
    
    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get value from nested dict using path like '$.name' or '$.xp.current'."""
        if not path or path == '$':
            return data
        
        # Remove leading $. if present
        if path.startswith('$.'):
            path = path[2:]
        elif path.startswith('$'):
            path = path[1:]
        
        parts = path.split('.')
        current = data
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
                if current is None:
                    return None
            else:
                return None
        
        return current
    
    def _set_nested_value(self, data: Dict, path: str, value: Any):
        """Set value in nested dict using path like '$.name' or '$.xp.current'."""
        if not path or path == '$':
            return
        
        # Remove leading $. if present
        if path.startswith('$.'):
            path = path[2:]
        elif path.startswith('$'):
            path = path[1:]
        
        parts = path.split('.')
        current = data
        
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value


if __name__ == "__main__":
    # For testing
    root = tk.Tk()
    ui = CharacterWindowUI(root)
    root.mainloop()
