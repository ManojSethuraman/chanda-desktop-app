#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application Class for Chanda Desktop.

This module contains the main ChandaDesktopApp class that manages
the application lifecycle and main window.
"""

import customtkinter as ctk
from typing import Optional
from ui.widgets import SanskritTextInput, ResultsDisplay
from controllers import AnalysisController


class ChandaDesktopApp:
    """
    Main application class for Chanda Desktop.
    
    This class manages the application lifecycle, main window,
    and coordinates between different components.
    
    Attributes:
        root: Main window (CTk instance)
        title: Application title
        geometry: Window size (width x height)
    """
    
    def __init__(self):
        """Initialize the Chanda Desktop Application."""
        self.root: Optional[ctk.CTk] = None
        self.title = "Chanda - Sanskrit Meter Analyzer"
        self.geometry = "1000x700"
        
        # Initialize analysis controller
        self.analysis_controller = AnalysisController()
        
        # Initialize the main window
        self._setup_window()
        self._setup_theme()
        self._create_ui()
    
    def _setup_window(self):
        """Create and configure the main window."""
        self.root = ctk.CTk()
        self.root.title(self.title)
        self.root.geometry(self.geometry)
        
        # Set minimum window size
        self.root.minsize(800, 600)
        
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _setup_theme(self):
        """Configure the application theme."""
        # Set appearance mode (light, dark, or system)
        ctk.set_appearance_mode("system")
        
        # Set color theme
        ctk.set_default_color_theme("blue")
    
    def _create_ui(self):
        """Create the user interface components."""
        # Create toolbar at the top
        self._create_toolbar()
        
        # Create main content area with three panels
        self._create_main_area()
        
        # Create status bar at the bottom
        self._create_statusbar()
        
        # Bind keyboard shortcuts
        self._bind_shortcuts()
    
    def _create_toolbar(self):
        """Create the top toolbar with buttons."""
        toolbar = ctk.CTkFrame(self.root, height=60)
        toolbar.pack(side="top", fill="x", padx=5, pady=5)
        
        # Left side buttons
        btn_frame_left = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame_left.pack(side="left", padx=5)
        
        # Paste button
        self.btn_paste = ctk.CTkButton(
            btn_frame_left,
            text="Paste",
            width=100,
            command=self._on_paste
        )
        self.btn_paste.pack(side="left", padx=2)
        
        # Clear button
        self.btn_clear = ctk.CTkButton(
            btn_frame_left,
            text="Clear",
            width=100,
            command=self._on_clear
        )
        self.btn_clear.pack(side="left", padx=2)
        
        # Analyze button (prominent)
        self.btn_analyze = ctk.CTkButton(
            btn_frame_left,
            text="Analyze",
            width=120,
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self._on_analyze
        )
        self.btn_analyze.pack(side="left", padx=5)
        
        # Right side controls
        btn_frame_right = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame_right.pack(side="right", padx=5)
        
        # Fuzzy checkbox
        self.fuzzy_var = ctk.BooleanVar(value=True)
        self.chk_fuzzy = ctk.CTkCheckBox(
            btn_frame_right,
            text="Fuzzy",
            variable=self.fuzzy_var,
            width=80
        )
        self.chk_fuzzy.pack(side="left", padx=5)
        
        # K value label and entry
        ctk.CTkLabel(btn_frame_right, text="K:").pack(side="left", padx=(10, 2))
        self.k_var = ctk.StringVar(value="10")
        self.entry_k = ctk.CTkEntry(
            btn_frame_right,
            textvariable=self.k_var,
            width=50
        )
        self.entry_k.pack(side="left", padx=2)
        
        # Theme toggle button
        self.btn_theme = ctk.CTkButton(
            btn_frame_right,
            text="Theme",
            width=50,
            command=self._toggle_theme
        )
        self.btn_theme.pack(side="left", padx=10)
    
    def _create_main_area(self):
        """Create the main content area with three resizable panels."""
        import tkinter as tk
        
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create horizontal PanedWindow for resizable panels
        # Note: Using tk.PanedWindow as CustomTkinter doesn't have one
        self.paned_window = tk.PanedWindow(
            main_container,
            orient=tk.HORIZONTAL,
            sashwidth=5,
            sashrelief=tk.RAISED,
            bg="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#dbdbdb"
        )
        self.paned_window.pack(fill="both", expand=True)
        
        # Create frame containers for each panel
        # These will hold our custom widgets
        self.left_container = ctk.CTkFrame(self.paned_window)
        self.center_container = ctk.CTkFrame(self.paned_window)
        
        # Add panels to PanedWindow
        self.paned_window.add(self.left_container, minsize=250)
        self.paned_window.add(self.center_container, minsize=400)
        
        # Create the actual panel content
        self._create_input_panel(self.left_container)
        self._create_results_panel(self.center_container)
        
        # Set initial position after window is rendered (40% for input)
        self.root.after(100, self._set_initial_panel_position)
        
        # Restore saved panel sizes
        self._restore_panel_sizes()
        
        # Bind sash position changes to save config
        self.paned_window.bind("<ButtonRelease-1>", lambda e: self._save_panel_sizes())
    
    def _create_input_panel(self, parent):
        """Create the input panel (left side)."""
        # Create SanskritTextInput widget with config manager
        # Initialize config_manager if not already present
        if not hasattr(self, 'config_manager'):
            from app.config import ConfigManager
            self.config_manager = ConfigManager()
        
        self.text_input = SanskritTextInput(
            parent,
            config_manager=self.config_manager
        )
        self.text_input.pack(fill="both", expand=True)
    
    def _create_results_panel(self, parent):
        """Create the results panel (right side)."""
        self.results_display = ResultsDisplay(parent)
        self.results_display.pack(fill="both", expand=True)
    
    def _create_statusbar(self):
        """Create the status bar at the bottom."""
        statusbar = ctk.CTkFrame(self.root, height=30)
        statusbar.pack(side="bottom", fill="x", padx=5, pady=5)
        
        # Status indicators
        self.status_label = ctk.CTkLabel(
            statusbar,
            text="Ready",
            font=("Arial", 10)
        )
        self.status_label.pack(side="left", padx=10)
        
        # Scheme indicator
        self.scheme_label = ctk.CTkLabel(
            statusbar,
            text="Scheme: Devanagari",
            font=("Arial", 10)
        )
        self.scheme_label.pack(side="left", padx=10)
        
        # Version indicator
        version_label = ctk.CTkLabel(
            statusbar,
            text="v0.1.0-alpha",
            font=("Arial", 10),
            text_color="gray"
        )
        version_label.pack(side="right", padx=10)
    
    def _bind_shortcuts(self):
        """Bind keyboard shortcuts."""
        # Essential shortcuts
        self.root.bind("<Control-q>", lambda e: self.quit())
        self.root.bind("<Control-Return>", lambda e: self._on_analyze())
        self.root.bind("<Control-l>", lambda e: self._on_clear())
        
        # Clipboard operations
        self.root.bind("<Control-v>", lambda e: self._on_paste())
        self.root.bind("<Control-c>", lambda e: self._on_copy_results())
        
        # New/Clear all
        self.root.bind("<Control-n>", lambda e: self._on_new())
        
        # Toggle fuzzy matching
        self.root.bind("<Control-f>", lambda e: self._toggle_fuzzy())
        
        # Help shortcuts (placeholders for Phase 4+)
        self.root.bind("<Control-h>", lambda e: self._show_keyboard_help())
        self.root.bind("<F1>", lambda e: self._show_help())
        
        # Refresh/Re-analyze
        self.root.bind("<F5>", lambda e: self._on_analyze())
    
    # Command handlers (placeholders)
    def _on_paste(self):
        """Handle paste button click."""
        if self.text_input.paste_from_clipboard():
            self._update_status("Text pasted from clipboard")
        else:
            self._update_status("Clipboard paste not available or failed")
    
    def _on_clear(self):
        """Handle clear button click."""
        self.text_input.clear()
        self._update_status("Input cleared")
    
    def _on_analyze(self):
        """Handle analyze button click."""
        text = self.text_input.get_text()
        if not text:
            self._update_status("Please enter text to analyze")
            return
        
        # Get analysis settings
        scheme = self.text_input.get_script()
        fuzzy = self.fuzzy_var.get()
        k = int(self.k_var.get()) if self.k_var.get().isdigit() else 10
        verse_mode = '\n' in text  # Auto-detect verse mode
        
        # Clear previous results
        self.results_display.clear()
        
        # Update status
        self._update_status("Analyzing...")
        
        # Perform analysis
        result = self.analysis_controller.analyze(
            text=text,
            scheme=scheme,
            fuzzy=fuzzy,
            k=k,
            verse_mode=verse_mode
        )
        
        # Display results
        if result.success:
            # Prepare data for color-coded display
            result_data = {
                'lines': result.lines,
                'verse_info': result.verse_info,
                'timestamp': result.timestamp.strftime('%Y-%m-%d %H:%M:%S') if result.timestamp else None
            }
            
            # Display with colors
            self.results_display.display_result_with_colors(result_data)
            
            self._update_status("Analysis complete")
        else:
            # Display error
            self.results_display.display_error(result.error_message)
            self._update_status(f"Analysis failed: {result.error_message}")
    
    def _on_meter_browser(self):
        """Handle meter browser button click."""
        self._update_status("Meter browser coming in Phase 6...")
    
    def _on_copy_results(self):
        """Handle copy results shortcut (Ctrl+C)."""
        if self.results_display.copy_to_clipboard():
            self._update_status("Results copied to clipboard")
        else:
            self._update_status("Clipboard copy not available or no results to copy")
    
    def _on_new(self):
        """Handle new/clear all shortcut (Ctrl+N)."""
        self.text_input.clear()
        self.results_display.set_placeholder()
        self._update_status("Cleared all")
    
    def _toggle_fuzzy(self):
        """Handle toggle fuzzy matching shortcut (Ctrl+F)."""
        current = self.fuzzy_var.get()
        self.fuzzy_var.set(not current)
        status = "enabled" if not current else "disabled"
        self._update_status(f"Fuzzy matching {status}")
    
    def _show_keyboard_help(self):
        """Handle keyboard help shortcut (Ctrl+H) - placeholder."""
        self._update_status("Keyboard shortcuts help coming in Phase 4...")
    
    def _show_help(self):
        """Handle help shortcut (F1) - placeholder."""
        self._update_status("Help documentation coming in Phase 4...")
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self._update_status(f"Switched to {new_mode} theme")
    
    def _update_status(self, message: str):
        """Update the status bar message."""
        self.status_label.configure(text=message)
    
    def _save_panel_sizes(self):
        """Save current panel sizes to config."""
        if hasattr(self, 'paned_window') and hasattr(self, 'config_manager'):
            try:
                # Get sash position (where the divider is)
                sash_pos = self.paned_window.sash_coord(0)[0]
                
                # Save to config
                self.config_manager.set('window', 'panel_sash_position', str(sash_pos))
                self.config_manager.save()
            except:
                pass  # Ignore errors during save
    
    def _restore_panel_sizes(self):
        """Restore panel sizes from config."""
        if hasattr(self, 'paned_window') and hasattr(self, 'config_manager'):
            try:
                # Get saved position (default 400 = 40% of 1000px window)
                sash_pos = self.config_manager.get('window', 'panel_sash_position', '400')
                
                # Apply position with a small delay to ensure window is fully rendered
                self.root.after(150, lambda: self._apply_panel_size(int(sash_pos)))
            except:
                pass  # Use default positions if restore fails
    
    def _set_initial_panel_position(self):
        """Set initial panel position to 40% of window width."""
        try:
            # Get current window width
            window_width = self.paned_window.winfo_width()
            if window_width > 100:  # Make sure window is rendered
                # Set input panel to 40% of window width
                sash_pos = int(window_width * 0.40)
                self.paned_window.sash_place(0, sash_pos, 0)
        except:
            pass  # Ignore errors
    
    def _apply_panel_size(self, sash_pos: int):
        """Apply panel size after window is rendered."""
        try:
            self.paned_window.sash_place(0, sash_pos, 0)
        except:
            pass  # Ignore errors
    
    def run(self):
        """
        Start the application main loop.
        
        This method starts the Tkinter event loop and blocks
        until the window is closed.
        """
        if self.root:
            self.root.mainloop()
    
    def quit(self):
        """Quit the application gracefully."""
        # Save panel sizes before quitting
        self._save_panel_sizes()
        
        if self.root:
            self.root.quit()
            self.root.destroy()
