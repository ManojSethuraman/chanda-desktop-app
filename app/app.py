#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Application Class for Chanda Desktop.

This module contains the main ChandaDesktopApp class that manages
the application lifecycle and main window.
"""

import customtkinter as ctk
from typing import Optional


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
        self.geometry = "1200x800"
        
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
            text="≡ƒôï Paste",
            width=100,
            command=self._on_paste
        )
        self.btn_paste.pack(side="left", padx=2)
        
        # Clear button
        self.btn_clear = ctk.CTkButton(
            btn_frame_left,
            text="≡ƒùæ∩╕Å Clear",
            width=100,
            command=self._on_clear
        )
        self.btn_clear.pack(side="left", padx=2)
        
        # Analyze button (prominent)
        self.btn_analyze = ctk.CTkButton(
            btn_frame_left,
            text="Γû╢∩╕Å Analyze",
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
            text="≡ƒöä Fuzzy",
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
            text="≡ƒîÖ",
            width=40,
            command=self._toggle_theme
        )
        self.btn_theme.pack(side="left", padx=10)
    
    def _create_main_area(self):
        """Create the main content area with three panels."""
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configure grid weights for responsive layout
        main_container.grid_columnconfigure(0, weight=1)  # Left panel
        main_container.grid_columnconfigure(1, weight=2)  # Center panel
        main_container.grid_columnconfigure(2, weight=1)  # Right panel
        main_container.grid_rowconfigure(0, weight=1)
        
        # Left Panel: Input
        self._create_input_panel(main_container)
        
        # Center Panel: Results
        self._create_results_panel(main_container)
        
        # Right Panel: Info/History
        self._create_info_panel(main_container)
    
    def _create_input_panel(self, parent):
        """Create the input panel (left side)."""
        input_frame = ctk.CTkFrame(parent)
        input_frame.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        
        # Header
        header = ctk.CTkLabel(
            input_frame,
            text="Input Text",
            font=("Arial", 14, "bold")
        )
        header.pack(pady=5, padx=10, anchor="w")
        
        # Script selector (placeholder)
        script_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        script_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(script_frame, text="Script:").pack(side="left")
        self.script_var = ctk.StringVar(value="Devanagari")
        self.script_menu = ctk.CTkComboBox(
            script_frame,
            values=["Devanagari", "IAST", "ITRANS", "Harvard-Kyoto"],
            variable=self.script_var,
            width=150
        )
        self.script_menu.pack(side="left", padx=5)
        
        # Text input area (placeholder with instructions)
        import tkinter as tk
        self.text_input = tk.Text(
            input_frame,
            wrap="word",
            font=("Nirmala UI", 12),
            bg="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#ffffff",
            fg="#ffffff" if ctk.get_appearance_mode() == "Dark" else "#000000",
            insertbackground="#ffffff" if ctk.get_appearance_mode() == "Dark" else "#000000"
        )
        self.text_input.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Insert placeholder text
        placeholder = """Enter Sanskrit text here...

Example:
αñòαÑï αñ¿αÑìαñ╡αñ╕αÑìαñ«αñ┐αñ¿αÑì αñ╕αñ╛αñ«αÑìαñ¬αÑìαñ░αññαñé αñ▓αÑïαñòαÑç αñùαÑüαñúαñ╡αñ╛αñ¿αÑì αñòαñ╢αÑìαñÜ αñ╡αÑÇαñ░αÑìαñ»αñ╡αñ╛αñ¿αÑìαÑñ
αñºαñ░αÑìαñ«αñ£αÑìαñ₧αñ╢αÑìαñÜ αñòαÑâαññαñ£αÑìαñ₧αñ╢αÑìαñÜ αñ╕αññαÑìαñ»αñ╡αñ╛αñòαÑìαñ»αÑï αñªαÑâαñóαñ╡αÑìαñ░αññαñâαÑÑ"""
        self.text_input.insert("1.0", placeholder)
    
    def _create_results_panel(self, parent):
        """Create the results panel (center)."""
        results_frame = ctk.CTkFrame(parent)
        results_frame.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        
        # Header
        header = ctk.CTkLabel(
            results_frame,
            text="Analysis Results",
            font=("Arial", 14, "bold")
        )
        header.pack(pady=5, padx=10, anchor="w")
        
        # Results display (placeholder)
        self.results_display = ctk.CTkTextbox(
            results_frame,
            font=("Nirmala UI", 11)
        )
        self.results_display.pack(fill="both", expand=True, padx=10, pady=5)
        
        results_placeholder = """Results will appear here after analysis.

Click "Analyze" or press Ctrl+Enter to analyze the input text.

Features coming soon:
ΓÇó Syllable segmentation
ΓÇó Laghu-Guru pattern (color-coded)
ΓÇó Gana notation
ΓÇó Identified meters
ΓÇó M─ütr─ü count
ΓÇó Fuzzy matches with similarity scores"""
        
        self.results_display.insert("1.0", results_placeholder)
    
    def _create_info_panel(self, parent):
        """Create the info/history panel (right side)."""
        info_frame = ctk.CTkFrame(parent)
        info_frame.grid(row=0, column=2, sticky="nsew", padx=2, pady=2)
        
        # Header
        header = ctk.CTkLabel(
            info_frame,
            text="History & Info",
            font=("Arial", 14, "bold")
        )
        header.pack(pady=5, padx=10, anchor="w")
        
        # Tabview for History and Favorites
        tabview = ctk.CTkTabview(info_frame)
        tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        tabview.add("Recent")
        tabview.add("Favorites")
        
        # Recent tab
        recent_label = ctk.CTkLabel(
            tabview.tab("Recent"),
            text="Recent analyses will appear here",
            font=("Arial", 11)
        )
        recent_label.pack(pady=20)
        
        # Favorites tab
        fav_label = ctk.CTkLabel(
            tabview.tab("Favorites"),
            text="Favorite analyses will appear here",
            font=("Arial", 11)
        )
        fav_label.pack(pady=20)
        
        # Meter browser button
        btn_meter_browser = ctk.CTkButton(
            info_frame,
            text="≡ƒôÜ Browse Meters",
            command=self._on_meter_browser
        )
        btn_meter_browser.pack(pady=10, padx=10)
    
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
        self.root.bind("<Control-q>", lambda e: self.quit())
        self.root.bind("<Control-Return>", lambda e: self._on_analyze())
        self.root.bind("<Control-l>", lambda e: self._on_clear())
    
    # Command handlers (placeholders)
    def _on_paste(self):
        """Handle paste button click."""
        self._update_status("Paste functionality coming soon...")
    
    def _on_clear(self):
        """Handle clear button click."""
        self.text_input.delete("1.0", "end")
        self._update_status("Input cleared")
    
    def _on_analyze(self):
        """Handle analyze button click."""
        text = self.text_input.get("1.0", "end-1c").strip()
        if text:
            self._update_status("Analysis functionality coming in Phase 3...")
            self.results_display.delete("1.0", "end")
            self.results_display.insert("1.0", 
                f"Input text received ({len(text)} characters).\n\n"
                "Analysis integration will be implemented in Phase 3.\n\n"
                "For now, the UI structure is ready!"
            )
        else:
            self._update_status("Please enter text to analyze")
    
    def _on_meter_browser(self):
        """Handle meter browser button click."""
        self._update_status("Meter browser coming in Phase 6...")
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        current = ctk.get_appearance_mode()
        new_mode = "Light" if current == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.btn_theme.configure(text="ΓÿÇ∩╕Å" if new_mode == "Dark" else "≡ƒîÖ")
        self._update_status(f"Switched to {new_mode} theme")
    
    def _update_status(self, message: str):
        """Update the status bar message."""
        self.status_label.configure(text=message)
    
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
        if self.root:
            self.root.quit()
            self.root.destroy()
