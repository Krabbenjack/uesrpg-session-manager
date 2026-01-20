"""Import dialog window."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class ImportWindow:
    """Dialog window for importing character data."""
    
    def __init__(self, parent, spec, importer, character_model):
        """Initialize the import window.
        
        Args:
            parent: Parent window
            spec: Import window specification
            importer: Importer instance
            character_model: CharacterModel instance
        """
        self.parent = parent
        self.spec = spec
        self.importer = importer
        self.character_model = character_model
        
        self.dialog = None
        self.selected_file = None
        self.selected_data = None
        self.overwrite_var = None
        self.preview_text = None
        self.file_label = None
    
    def show(self):
        """Show the import dialog."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.spec.get('title', 'Import'))
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Configure geometry
        self.dialog.geometry("500x400")
        
        # Apply theme colors
        bg = self.parent.cget('bg')
        self.dialog.configure(bg=bg)
        
        # Build UI
        self._build_ui()
        
        # Center on parent
        self.dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f"+{x}+{y}")
    
    def _build_ui(self):
        """Build the import dialog UI."""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Choose JSON button
        choose_btn = ttk.Button(main_frame, text="Choose JSON…", command=self._choose_file)
        choose_btn.pack(fill='x', pady=5)
        
        # Selected file label
        ttk.Label(main_frame, text="Selected file:").pack(anchor='w')
        self.file_label = ttk.Label(main_frame, text="(none)", relief='sunken')
        self.file_label.pack(fill='x', pady=5)
        
        # Preview area
        ttk.Label(main_frame, text="Preview:").pack(anchor='w', pady=(10, 0))
        
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill='both', expand=True, pady=5)
        
        self.preview_text = tk.Text(preview_frame, height=10, width=60, state='disabled',
                                    bg='white', fg='#000000')
        self.preview_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(preview_frame, command=self.preview_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.preview_text.config(yscrollcommand=scrollbar.set)
        
        # Overwrite checkbox
        self.overwrite_var = tk.BooleanVar(value=False)
        overwrite_check = ttk.Checkbutton(main_frame, text="Overwrite existing fields",
                                         variable=self.overwrite_var)
        overwrite_check.pack(anchor='w', pady=10)
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=5)
        
        import_btn = ttk.Button(btn_frame, text="Import", command=self._import_data)
        import_btn.pack(side='left', expand=True, fill='x', padx=2)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self._close)
        cancel_btn.pack(side='left', expand=True, fill='x', padx=2)
    
    def _choose_file(self):
        """Open file dialog to choose JSON file."""
        filename = filedialog.askopenfilename(
            parent=self.dialog,
            title="Choose JSON file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Load the file
                self.selected_data = self.importer.load_json(filename)
                self.selected_file = filename
                
                # Update file label
                import os
                self.file_label.config(text=os.path.basename(filename))
                
                # Update preview
                preview_info = self.importer.get_preview_info(self.selected_data)
                self.preview_text.config(state='normal')
                self.preview_text.delete('1.0', tk.END)
                self.preview_text.insert('1.0', preview_info)
                self.preview_text.config(state='disabled')
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{e}", parent=self.dialog)
    
    def _import_data(self):
        """Import the selected data into character model."""
        if not self.selected_data:
            messagebox.showwarning("No File", "Please choose a JSON file first.", parent=self.dialog)
            return
        
        try:
            # Import with overwrite setting
            overwrite = self.overwrite_var.get()
            self.importer.import_data(self.selected_data, self.character_model, overwrite)
            
            messagebox.showinfo("Success", "Data imported successfully!", parent=self.dialog)
            self._close()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data:\n{e}", parent=self.dialog)
    
    def _close(self):
        """Close the dialog."""
        if self.dialog:
            self.dialog.destroy()
