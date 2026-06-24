#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanskrit Text Input Widget for Chanda Desktop.

This module provides a custom widget for Sanskrit text input with
script selection, clipboard integration, and theme support.
"""

import tkinter as tk
import customtkinter as ctk
from typing import Optional, Callable
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class SanskritTextInput(ctk.CTkFrame):
    """
    Custom widget for Sanskrit text input.
    
    Features:
    - Script/transliteration scheme selector
    - Multi-line text input with proper font
    - Clipboard paste support
    - Theme-aware styling
    - Configurable placeholder text
    - Event callbacks for text changes
    
    Attributes:
        config_manager: Configuration manager instance
        on_text_change: Optional callback for text changes
    """
    
    AVAILABLE_SCRIPTS = [
        "Devanagari",
        "IAST",
        "ITRANS", 
        "Harvard-Kyoto",
        "SLP1",
        "Velthuis",
        "WX"
    ]
    
    DEFAULT_PLACEHOLDER = """Enter Sanskrit text here...

Example:
धर्मे च अर्थे च कामे च मोक्षे च भरतर्षभ।
यदिहास्ति तदन्यत्र यन्नेहास्ति न तत्क्वचित्॥"""
    
    def __init__(
        self,
        parent,
        config_manager=None,
        on_text_change: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize the Sanskrit text input widget.
        
        Args:
            parent: Parent widget
            config_manager: ConfigManager instance for persistence
            on_text_change: Optional callback when text changes
            **kwargs: Additional arguments passed to CTkFrame
        """
        super().__init__(parent, **kwargs)
        
        self.config_manager = config_manager
        self.on_text_change = on_text_change
        
        # Initialize variables
        self.script_var = ctk.StringVar(value=self._get_default_script())
        self.script_var.trace_add("write", self._on_script_change)
        
        # Build the UI
        self._create_ui()
        
    def _get_default_script(self) -> str:
        """Get default script from config or use Devanagari."""
        if self.config_manager:
            return self.config_manager.get('analysis', 'default_input_scheme', 'Devanagari')
        return "Devanagari"
    
    def _create_ui(self):
        """Create the UI components."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Input Text",
            font=("Arial", 14, "bold")
        )
        header.pack(pady=5, padx=10, anchor="w")
        
        # Script selector frame
        script_frame = ctk.CTkFrame(self, fg_color="transparent")
        script_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(script_frame, text="Script:").pack(side="left")
        self.script_menu = ctk.CTkComboBox(
            script_frame,
            values=self.AVAILABLE_SCRIPTS,
            variable=self.script_var,
            width=150,
            state="readonly"
        )
        self.script_menu.pack(side="left", padx=5)
        
        # Text input area
        self.text_widget = tk.Text(
            self,
            wrap="word",
            font=("Nirmala UI", 12),
            bg=self._get_bg_color(),
            fg=self._get_fg_color(),
            insertbackground=self._get_fg_color(),
            relief="flat",
            borderwidth=5,
            padx=5,
            pady=5
        )
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Bind text change events
        self.text_widget.bind('<<Modified>>', self._on_text_modified)
        
        # Insert placeholder text
        self.set_placeholder()
    
    def _get_bg_color(self) -> str:
        """Get background color based on current theme."""
        return "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#ffffff"
    
    def _get_fg_color(self) -> str:
        """Get foreground color based on current theme."""
        return "#ffffff" if ctk.get_appearance_mode() == "Dark" else "#000000"
    
    def _on_script_change(self, *args):
        """Handle script selection change."""
        script = self.script_var.get()
        if self.config_manager:
            self.config_manager.set('analysis', 'default_input_scheme', script)
    
    def _on_text_modified(self, event):
        """Handle text modification event."""
        if self.on_text_change and self.text_widget.edit_modified():
            self.on_text_change()
            self.text_widget.edit_modified(False)
    
    def get_text(self) -> str:
        """
        Get the current text content.
        
        Returns:
            Current text content (stripped of leading/trailing whitespace)
        """
        return self.text_widget.get("1.0", "end-1c").strip()
    
    def set_text(self, text: str):
        """
        Set the text content programmatically.
        
        Args:
            text: Text to set in the input area
        """
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)
    
    def clear(self):
        """Clear all text from the input area."""
        self.text_widget.delete("1.0", "end")
    
    def set_placeholder(self, text: Optional[str] = None):
        """
        Set placeholder text in the input area.
        
        Args:
            text: Placeholder text (uses default if None)
        """
        placeholder = text or self.DEFAULT_PLACEHOLDER
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", placeholder)
    
    def get_script(self) -> str:
        """
        Get the currently selected script/scheme.
        
        Returns:
            Selected script name
        """
        return self.script_var.get()
    
    def set_script(self, script: str):
        """
        Set the script/scheme programmatically.
        
        Args:
            script: Script name (must be in AVAILABLE_SCRIPTS)
        """
        if script in self.AVAILABLE_SCRIPTS:
            self.script_var.set(script)
    
    def paste_from_clipboard(self) -> bool:
        """
        Paste text from system clipboard.
        
        Returns:
            True if paste was successful, False otherwise
        """
        if not CLIPBOARD_AVAILABLE:
            return False
        
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text:
                # Insert at cursor position or replace selection
                try:
                    self.text_widget.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass  # No selection
                
                self.text_widget.insert("insert", clipboard_text)
                return True
        except Exception:
            pass
        
        return False
    
    def copy_to_clipboard(self) -> bool:
        """
        Copy selected text or all text to clipboard.
        
        Returns:
            True if copy was successful, False otherwise
        """
        if not CLIPBOARD_AVAILABLE:
            return False
        
        try:
            # Try to get selected text first
            try:
                selected_text = self.text_widget.get("sel.first", "sel.last")
            except tk.TclError:
                # No selection, copy all text
                selected_text = self.get_text()
            
            if selected_text:
                pyperclip.copy(selected_text)
                return True
        except Exception:
            pass
        
        return False
    
    def update_theme(self):
        """Update widget colors based on current theme."""
        self.text_widget.configure(
            bg=self._get_bg_color(),
            fg=self._get_fg_color(),
            insertbackground=self._get_fg_color()
        )
    
    def focus(self):
        """Set focus to the text input area."""
        self.text_widget.focus_set()
    
    def is_empty(self) -> bool:
        """
        Check if the input is empty.
        
        Returns:
            True if empty, False otherwise
        """
        return len(self.get_text()) == 0
