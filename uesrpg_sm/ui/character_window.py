"""Main character window with tabs and sections."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from PIL import Image, ImageTk


class CharacterWindow:
    """Main character window with spec-driven UI."""
    
    def __init__(self, root, spec, spec_loader, renderer, character_model, importer):
        """Initialize the character window.
        
        Args:
            root: Tk root window
            spec: Window specification dictionary
            spec_loader: SpecLoader instance
            renderer: SpecRenderer instance
            character_model: CharacterModel instance
            importer: Importer instance
        """
        self.root = root
        self.spec = spec
        self.spec_loader = spec_loader
        self.renderer = renderer
        self.character_model = character_model
        self.importer = importer
        
        self.current_file = None
        self.portrait_image = None
        self.portrait_label = None
        
        # Configure window
        self._configure_window()
        
        # Create menu
        self._create_menu()
        
        # Create main layout
        self._create_layout()
        
        # Listen for character model changes
        self.character_model.add_observer(self._on_character_changed)
    
    def _configure_window(self):
        """Configure main window properties."""
        title = self.spec.get('title', 'Character')
        self.root.title(title)
        
        # Get window config
        app_config = self.spec_loader.get_app_config()
        window_config = app_config.get('window', {})
        
        # Set size
        size = window_config.get('size', [1100, 720])
        self.root.geometry(f"{size[0]}x{size[1]}")
        
        # Set minimum size
        min_size = window_config.get('min_size', [980, 640])
        self.root.minsize(min_size[0], min_size[1])
        
        # Set resizable
        resizable = window_config.get('resizable', True)
        self.root.resizable(resizable, resizable)
    
    def _create_menu(self):
        """Create menu bar from spec."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        menus = self.spec_loader.get_menus()
        for menu_spec in menus:
            menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=menu_spec.get('label', ''), menu=menu)
            
            for item in menu_spec.get('items', []):
                if item.get('type') == 'separator':
                    menu.add_separator()
                else:
                    label = item.get('label', '')
                    command = item.get('command', '')
                    menu.add_command(label=label, command=lambda cmd=command: self._handle_menu_command(cmd))
    
    def _handle_menu_command(self, command):
        """Handle menu command.
        
        Args:
            command: Command name from spec
        """
        if command == 'file_new':
            self._file_new()
        elif command == 'file_open':
            self._file_open()
        elif command == 'file_save':
            self._file_save()
        elif command == 'file_save_as':
            self._file_save_as()
        elif command == 'app_exit':
            self._app_exit()
        elif command == 'import_base_data':
            self._import_base_data()
    
    def _create_layout(self):
        """Create main layout with portrait panel and notebook."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True)
        
        # Configure grid
        main_container.grid_columnconfigure(0, weight=0, minsize=220)  # Left panel
        main_container.grid_columnconfigure(1, weight=1, minsize=760)  # Main panel
        main_container.grid_rowconfigure(0, weight=1)
        
        # Create left portrait panel
        self._create_portrait_panel(main_container)
        
        # Create main notebook panel
        self._create_notebook_panel(main_container)
    
    def _create_portrait_panel(self, parent):
        """Create left portrait panel.
        
        Args:
            parent: Parent widget
        """
        panel = ttk.Frame(parent, padding=10)
        panel.grid(row=0, column=0, sticky='nsew')
        
        # Title
        ttk.Label(panel, text="Portrait", style='Heading.TLabel').pack(pady=5)
        
        # Portrait image area
        self.portrait_label = ttk.Label(panel, text="No portrait selected", anchor='center',
                                       relief='sunken', width=20)
        self.portrait_label.pack(pady=10, fill='both', expand=True)
        
        # Select portrait button
        select_btn = ttk.Button(panel, text="Select Portrait…", command=self._select_portrait)
        select_btn.pack(fill='x', pady=5)
        
        # Hint label
        hint_label = ttk.Label(panel, text="Put images into\nassets/portraits\n(png/jpg/gif)",
                              justify='center', wraplength=180)
        hint_label.pack(pady=5)
        
        # Load current portrait if any
        self._update_portrait_display()
    
    def _create_notebook_panel(self, parent):
        """Create main notebook panel with tabs.
        
        Args:
            parent: Parent widget
        """
        notebook = ttk.Notebook(parent)
        notebook.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Get tabs from spec
        main_panel = self.spec.get('main_panel', {})
        tabs = main_panel.get('tabs', [])
        
        for tab_spec in tabs:
            tab_title = tab_spec.get('title', 'Tab')
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tab_title)
            
            # Create scrollable canvas for tab content
            canvas = tk.Canvas(tab_frame, bg=self.renderer.colors.get('bg', '#FFD5AF'))
            scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e, c=canvas: c.configure(scrollregion=c.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Bind mousewheel
            def _on_mousewheel(event, c=canvas):
                c.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            # Create sections in tab
            self._create_sections(scrollable_frame, tab_spec.get('sections', []))
    
    def _create_sections(self, parent, sections):
        """Create sections within a tab.
        
        Args:
            parent: Parent widget
            sections: List of section specifications
        """
        for section_spec in sections:
            # Section frame with title
            section_frame = ttk.LabelFrame(parent, text=section_spec.get('title', ''), padding=10)
            section_frame.pack(fill='x', padx=10, pady=5)
            
            # Get layout config
            layout = section_spec.get('layout', {})
            columns = layout.get('columns', 1)
            
            # Configure grid columns
            for col in range(columns):
                section_frame.grid_columnconfigure(col, weight=1)
            
            # Create widgets
            widgets = section_spec.get('widgets', [])
            self._create_widgets(section_frame, widgets, columns)
    
    def _create_widgets(self, parent, widgets, grid_columns):
        """Create widgets from spec.
        
        Args:
            parent: Parent widget
            widgets: List of widget specifications
            grid_columns: Number of grid columns
        """
        current_row = 0
        current_col = 0
        
        for widget_spec in widgets:
            widget_type = widget_spec.get('type', 'field')
            colspan = widget_spec.get('colspan', 1)
            
            if widget_type == 'field':
                self.renderer.render_field(parent, widget_spec, current_row, current_col)
                
                # Advance position
                current_col += colspan
                if current_col >= grid_columns:
                    current_col = 0
                    current_row += 1
            
            elif widget_type == 'table_inline':
                # Render inline table for characteristics or armor slots
                self._create_table_inline(parent, widget_spec, current_row, current_col)
                current_row += 1
                current_col = 0
            
            elif widget_type == 'table':
                # Render table with add/edit/delete
                self._create_table(parent, widget_spec, current_row, current_col)
                current_row += 1
                current_col = 0
            
            elif widget_type == 'group':
                # Create sub-group
                group_frame = ttk.LabelFrame(parent, text=widget_spec.get('title', ''), padding=5)
                group_frame.grid(row=current_row, column=current_col, columnspan=colspan, sticky='ew', pady=5)
                
                group_layout = widget_spec.get('layout', {})
                group_cols = group_layout.get('columns', 2)
                
                for col in range(group_cols):
                    group_frame.grid_columnconfigure(col, weight=1)
                
                self._create_widgets(group_frame, widget_spec.get('widgets', []), group_cols)
                
                current_col += colspan
                if current_col >= grid_columns:
                    current_col = 0
                    current_row += 1
    
    def _create_table_inline(self, parent, table_spec, row, col):
        """Create an inline table (for characteristics or armor).
        
        Args:
            parent: Parent widget
            table_spec: Table specification
            row: Grid row
            col: Grid column
        """
        bind_path = table_spec.get('bind', '')
        mode = table_spec.get('mode', 'list')
        
        # For MVP, render as a simple grid of entry fields
        frame = ttk.Frame(parent)
        frame.grid(row=row, column=col, columnspan=8, sticky='ew', pady=5)
        
        if mode == 'keyed_object':
            # Armor slots mode
            rows = table_spec.get('rows', [])
            columns = table_spec.get('columns', [])
            
            # Header row
            ttk.Label(frame, text="Slot", font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=0, padx=2)
            for i, col_spec in enumerate(columns):
                ttk.Label(frame, text=col_spec.get('label', ''), font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=i+1, padx=2)
            
            # Data rows
            for i, row_spec in enumerate(rows):
                row_key = row_spec.get('key', '')
                row_label = row_spec.get('label', '')
                
                ttk.Label(frame, text=row_label).grid(row=i+1, column=0, sticky='w', padx=2, pady=1)
                
                for j, col_spec in enumerate(columns):
                    col_key = col_spec.get('key', '')
                    bind = f"{bind_path}.{row_key}.{col_key}"
                    
                    entry = ttk.Entry(frame, width=10)
                    entry.grid(row=i+1, column=j+1, padx=2, pady=1)
                    
                    self.renderer._bind_widget(entry, bind, 'entry')
        else:
            # Characteristics inline table
            columns = table_spec.get('columns', [])
            
            # Header row
            for i, col_spec in enumerate(columns):
                ttk.Label(frame, text=col_spec.get('label', ''), font=('TkDefaultFont', 9, 'bold')).grid(row=0, column=i, padx=2)
            
            # Get characteristics data
            chars_data = self.character_model.get_value(bind_path)
            if isinstance(chars_data, list):
                for i, char in enumerate(chars_data):
                    for j, col_spec in enumerate(columns):
                        col_key = col_spec.get('key', '')
                        is_readonly = col_spec.get('readonly', False)
                        is_check = col_spec.get('widget') == 'check'
                        bind = f"{bind_path}[{i}].{col_key}"
                        
                        if is_check:
                            var = tk.BooleanVar()
                            check = ttk.Checkbutton(frame, variable=var)
                            check.var = var
                            check.grid(row=i+1, column=j, padx=2, pady=1)
                            self.renderer._bind_widget(check, bind, 'check')
                        else:
                            entry = ttk.Entry(frame, width=8, state='readonly' if is_readonly else 'normal')
                            entry.grid(row=i+1, column=j, padx=2, pady=1)
                            self.renderer._bind_widget(entry, bind, 'readonly_entry' if is_readonly else 'entry')
    
    def _create_table(self, parent, table_spec, row, col):
        """Create a table with treeview.
        
        Args:
            parent: Parent widget
            table_spec: Table specification
            row: Grid row
            col: Grid column
        """
        bind_path = table_spec.get('bind', '')
        columns_spec = table_spec.get('columns', [])
        style = table_spec.get('style', 'base')
        
        # Frame for table
        frame = ttk.LabelFrame(parent, text=table_spec.get('title', ''))
        frame.grid(row=row, column=col, columnspan=8, sticky='nsew', pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)
        
        # Create treeview
        columns = [col['key'] for col in columns_spec]
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=8)
        
        # Configure columns
        for col_spec in columns_spec:
            col_key = col_spec['key']
            col_label = col_spec.get('label', col_key)
            col_width = col_spec.get('width', 10)
            tree.heading(col_key, text=col_label)
            tree.column(col_key, width=col_width * 10, anchor='w')
        
        # Apply italic font for skills
        if style == 'skill':
            skill_font = self.renderer._get_font('skill')
            tree.tag_configure('skill', font=skill_font)
        
        tree.grid(row=0, column=0, sticky='nsew')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Buttons frame
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(btn_frame, text="Add", command=lambda: self._table_add(tree, bind_path, columns_spec)).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Delete", command=lambda: self._table_delete(tree, bind_path)).pack(side='left', padx=2)
        
        # Load data into tree
        self._refresh_table(tree, bind_path, columns_spec, style)
    
    def _refresh_table(self, tree, bind_path, columns_spec, style='base'):
        """Refresh table data from model.
        
        Args:
            tree: Treeview widget
            bind_path: JSONPath binding
            columns_spec: Column specifications
            style: Table style
        """
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Get data
        data = self.character_model.get_value(bind_path)
        if not isinstance(data, list):
            return
        
        # Add items
        for item in data:
            if isinstance(item, dict):
                values = [item.get(col['key'], '') for col in columns_spec]
                tags = ('skill',) if style == 'skill' else ()
                tree.insert('', 'end', values=values, tags=tags)
    
    def _table_add(self, tree, bind_path, columns_spec):
        """Add a row to a table.
        
        Args:
            tree: Treeview widget
            bind_path: JSONPath binding
            columns_spec: Column specifications
        """
        # For MVP, just add an empty row
        data = self.character_model.get_value(bind_path)
        if not isinstance(data, list):
            data = []
        
        # Create empty row
        new_row = {col['key']: '' for col in columns_spec}
        data.append(new_row)
        
        self.character_model.set_value(bind_path, data)
        self._refresh_table(tree, bind_path, columns_spec)
    
    def _table_delete(self, tree, bind_path):
        """Delete selected row from table.
        
        Args:
            tree: Treeview widget
            bind_path: JSONPath binding
        """
        selection = tree.selection()
        if not selection:
            return
        
        # Get index of selected item
        item_id = selection[0]
        index = tree.index(item_id)
        
        # Remove from model
        data = self.character_model.get_value(bind_path)
        if isinstance(data, list) and index < len(data):
            data.pop(index)
            self.character_model.set_value(bind_path, data)
            self._refresh_table(tree, bind_path, tree['columns'])
    
    def _select_portrait(self):
        """Open dialog to select portrait from directory."""
        portrait_dir = self.spec_loader.get_portrait_dir()
        
        # Ensure directory exists
        if not os.path.exists(portrait_dir):
            os.makedirs(portrait_dir, exist_ok=True)
        
        # List available images
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif')
        images = [f for f in os.listdir(portrait_dir) if f.lower().endswith(image_extensions)]
        
        if not images:
            messagebox.showinfo("No Portraits", 
                              "No portraits found.\nPlace PNG, JPG, or GIF images in:\n" + portrait_dir,
                              parent=self.root)
            return
        
        # Show selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Portrait")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Choose a portrait:").pack(pady=10)
        
        listbox = tk.Listbox(dialog, width=40, height=15)
        listbox.pack(padx=10, pady=5)
        
        for img in images:
            listbox.insert(tk.END, img)
        
        def select():
            selection = listbox.curselection()
            if selection:
                selected_file = images[selection[0]]
                self.character_model.set_value('$.portrait.file', selected_file)
                self._update_portrait_display()
                dialog.destroy()
        
        ttk.Button(dialog, text="Select", command=select).pack(pady=5)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)
    
    def _update_portrait_display(self):
        """Update the portrait image display."""
        portrait_file = self.character_model.get_value('$.portrait.file')
        
        if not portrait_file or not self.portrait_label:
            return
        
        portrait_dir = self.spec_loader.get_portrait_dir()
        portrait_path = os.path.join(portrait_dir, portrait_file)
        
        if os.path.exists(portrait_path):
            try:
                # Load and resize image
                img = Image.open(portrait_path)
                img.thumbnail((200, 240), Image.Resampling.LANCZOS)
                
                self.portrait_image = ImageTk.PhotoImage(img)
                self.portrait_label.config(image=self.portrait_image, text='')
            except Exception as e:
                self.portrait_label.config(text=f"Error loading\nportrait:\n{e}")
        else:
            self.portrait_label.config(text="Portrait file\nnot found")
    
    def _on_character_changed(self):
        """Handle character model changes."""
        # Refresh all bound widgets
        self.renderer.refresh_all_widgets()
        
        # Update portrait
        self._update_portrait_display()
    
    def _file_new(self):
        """Create a new character."""
        if messagebox.askyesno("New Character", "Create a new character?\nUnsaved changes will be lost.", parent=self.root):
            default_char = self.spec_loader.get_default_character()
            self.character_model.reset(default_char)
            self.current_file = None
            self.root.title("Character - New")
    
    def _file_open(self):
        """Open a character file."""
        filename = filedialog.askopenfilename(
            parent=self.root,
            title="Open Character",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.character_model.from_dict(data)
                self.current_file = filename
                self.root.title(f"Character - {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}", parent=self.root)
    
    def _file_save(self):
        """Save the current character."""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self._file_save_as()
    
    def _file_save_as(self):
        """Save the character to a new file."""
        filename = filedialog.asksaveasfilename(
            parent=self.root,
            title="Save Character As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self._save_to_file(filename)
            self.current_file = filename
            self.root.title(f"Character - {os.path.basename(filename)}")
    
    def _save_to_file(self, filename):
        """Save character data to a file.
        
        Args:
            filename: File path to save to
        """
        try:
            data = self.character_model.to_dict()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", "Character saved successfully!", parent=self.root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}", parent=self.root)
    
    def _app_exit(self):
        """Exit the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=self.root):
            self.root.quit()
    
    def _import_base_data(self):
        """Open the import dialog."""
        from .import_window import ImportWindow
        
        import_spec = self.spec_loader.get_window('import_window')
        if import_spec:
            import_win = ImportWindow(self.root, import_spec, self.importer, self.character_model)
            import_win.show()
