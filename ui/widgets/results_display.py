#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Results Display Widget for Chanda Desktop.

This module provides a custom widget for displaying Sanskrit meter
analysis results with formatting and color support.
"""

import tkinter as tk
import customtkinter as ctk
from typing import Optional, Dict, Any, List
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class ResultsDisplay(ctk.CTkFrame):
    """
    Custom widget for displaying analysis results.
    
    Features:
    - Formatted text display with custom styling
    - Color-coded pattern display support
    - Copy results to clipboard
    - Clear/reset methods
    - Custom fonts and colors from theme
    - Error message display
    - Theme-aware styling
    
    Attributes:
        theme_manager: Optional theme manager for color configuration
        textbox: Internal CTkTextbox for displaying content
    """
    
    DEFAULT_PLACEHOLDER = """Results will appear here after analysis.

Click "Analyze" or press Ctrl+Enter to analyze the input text.

Features coming soon:
• Syllable segmentation
• Laghu-Guru pattern (color-coded)
• Gana notation
• Identified meters
• Mātrā count
• Fuzzy matches with similarity scores"""
    
    def __init__(
        self,
        parent,
        theme_manager=None,
        **kwargs
    ):
        """
        Initialize the results display widget.
        
        Args:
            parent: Parent widget
            theme_manager: Optional ThemeManager instance for colors
            **kwargs: Additional arguments passed to CTkFrame
        """
        super().__init__(parent, **kwargs)
        
        self.theme_manager = theme_manager
        
        # Build the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI components."""
        # Header
        header = ctk.CTkLabel(
            self,
            text="Analysis Results",
            font=("Arial", 14, "bold")
        )
        header.pack(pady=5, padx=10, anchor="w")
        
        # Create a frame for the text widget (for scrollbar)
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Results textbox - using tk.Text for color tag support
        self.textbox = tk.Text(
            text_frame,
            wrap="word",
            font=("Nirmala UI", 11),
            bg=self._get_bg_color(),
            fg=self._get_fg_color(),
            relief="flat",
            borderwidth=0,
            padx=10,
            pady=10,
            state="disabled"  # Read-only
        )
        self.textbox.pack(fill="both", expand=True)
        
        # Configure color tags for Laghu-Guru visualization
        self._configure_tags()
        
        # Insert placeholder text
        self.set_placeholder()
    
    def _get_bg_color(self) -> str:
        """Get background color based on current theme."""
        return "#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#ffffff"
    
    def _get_fg_color(self) -> str:
        """Get foreground color based on current theme."""
        return "#dcdcdc" if ctk.get_appearance_mode() == "Dark" else "#000000"
    
    def _configure_tags(self):
        """Configure text tags for color-coded display."""
        # Laghu (light syllable) - Blue
        self.textbox.tag_config("laghu", foreground="#3b82f6", font=("Nirmala UI", 11, "bold"))
        
        # Guru (heavy syllable) - Red
        self.textbox.tag_config("guru", foreground="#ef4444", font=("Nirmala UI", 11, "bold"))
        
        # Header styles
        self.textbox.tag_config("header", font=("Arial", 12, "bold"), foreground="#1f6aa5")
        self.textbox.tag_config("subheader", font=("Arial", 10, "bold"))
        
        # Exact match indicator
        self.textbox.tag_config("exact", foreground="#10b981", font=("Nirmala UI", 11, "bold"))
        
        # Error
        self.textbox.tag_config("error", foreground="#ef4444", font=("Arial", 11, "bold"))
        
        # Info
        self.textbox.tag_config("info", foreground="#6b7280", font=("Arial", 10, "italic"))
    
    def display_result(self, result: Any, clear_first: bool = True):
        """
        Display formatted analysis result.
        
        Args:
            result: Analysis result to display (string or formatted object)
            clear_first: Whether to clear existing content first
        """
        if clear_first:
            self.clear()
        
        # Enable editing temporarily
        self.textbox.config(state="normal")
        
        if isinstance(result, str):
            self.textbox.insert("end", result)
        elif isinstance(result, dict):
            # Format dictionary results
            formatted = self._format_dict_result(result)
            self.textbox.insert("end", formatted)
        else:
            # Convert to string
            self.textbox.insert("end", str(result))
        
        # Disable editing
        self.textbox.config(state="disabled")
    
    def display_result_with_colors(self, result_data: Dict[str, Any]):
        """
        Display analysis result with color-coded patterns.
        
        Args:
            result_data: Dictionary containing analysis data with lines and patterns
        """
        self.clear()
        self.textbox.config(state="normal")
        
        # Header
        self.textbox.insert("end", "=== Analysis Results ===\n", "header")
        self.textbox.insert("end", "=" * 60 + "\n\n")
        
        # Display each line
        lines = result_data.get('lines', [])
        for i, line_data in enumerate(lines, 1):
            if 'error' in line_data:
                self.textbox.insert("end", f"Line {i}: ", "subheader")
                self.textbox.insert("end", f"ERROR - {line_data['error']}\n\n", "error")
                continue
            
            # Line text
            self.textbox.insert("end", f"Line {i}: ", "subheader")
            self.textbox.insert("end", f"{line_data['text']}\n")
            
            # Pattern with colors
            pattern = line_data.get('pattern', '')
            syllables = line_data.get('syllables', [])
            
            if pattern:
                self.textbox.insert("end", "  Pattern: ")
                self._insert_colored_pattern(pattern)
                self.textbox.insert("end", f" ({line_data.get('syllable_count', 0)} syllables)\n")
            
            # Syllable grid (if syllables available)
            if syllables and pattern:
                self.textbox.insert("end", "  Syllables:\n")
                self._insert_syllable_grid(syllables, pattern)
            
            # Meters
            meters = line_data.get('meters', [])
            if meters:
                self.textbox.insert("end", "  Identified Meters:\n")
                for j, meter in enumerate(meters[:5], 1):
                    meter_name = meter.get('name', 'Unknown')
                    similarity = meter.get('similarity', 1.0)
                    exact = meter.get('exact', False)
                    
                    if exact:
                        self.textbox.insert("end", f"    {j}. ")
                        self.textbox.insert("end", "[EXACT] ", "exact")
                        self.textbox.insert("end", f"{meter_name}\n")
                    else:
                        self.textbox.insert("end", f"    {j}. {meter_name} (similarity: {similarity:.2%})\n")
            else:
                self.textbox.insert("end", "  No matching meters found\n")
            
            self.textbox.insert("end", "\n")
        
        # Verse info
        verse_info = result_data.get('verse_info')
        if verse_info:
            self.textbox.insert("end", "=== Verse Structure ===\n", "header")
            self.textbox.insert("end", "-" * 60 + "\n")
            self.textbox.insert("end", f"Total Lines: {verse_info.get('total_lines', 0)}\n")
            
            if verse_info.get('uniform_pattern'):
                self.textbox.insert("end", "Pattern: Uniform (")
                self._insert_colored_pattern(verse_info.get('common_pattern', ''))
                self.textbox.insert("end", ")\n")
            else:
                self.textbox.insert("end", "Pattern: Non-uniform\n")
            
            common_meters = verse_info.get('common_meters', [])
            if common_meters:
                self.textbox.insert("end", f"Common Meters: {', '.join(common_meters)}\n")
            
            self.textbox.insert("end", "\n")
        
        # Timestamp and status
        timestamp = result_data.get('timestamp')
        if timestamp:
            self.textbox.insert("end", "\n" + "=" * 60 + "\n")
            self.textbox.insert("end", "✓ Analysis completed successfully\n", "exact")
            self.textbox.insert("end", f"Analyzed at: {timestamp}\n", "info")
        
        self.textbox.config(state="disabled")
    
    def _insert_colored_pattern(self, pattern: str):
        """
        Insert pattern string with color-coded L (Laghu) and G (Guru).
        
        Args:
            pattern: Pattern string (e.g., "LGGLGG")
        """
        for char in pattern:
            if char == 'L':
                self.textbox.insert("end", "L", "laghu")
            elif char == 'G':
                self.textbox.insert("end", "G", "guru")
            else:
                self.textbox.insert("end", char)
    
    def _insert_syllable_grid(self, syllables: List[str], pattern: str):
        """
        Insert syllable grid with pattern visualization.
        
        Args:
            syllables: List of syllable strings
            pattern: Laghu-Guru pattern string
        """
        if not syllables:
            return
        
        # Create grid (max 8 syllables per row for readability)
        syllables_per_row = 8
        
        for i in range(0, len(syllables), syllables_per_row):
            row_syllables = syllables[i:i+syllables_per_row]
            row_pattern = pattern[i:i+syllables_per_row] if i < len(pattern) else ''
            
            # Syllables row
            self.textbox.insert("end", "    ")
            for j, syllable in enumerate(row_syllables):
                # Determine tag based on pattern
                tag = None
                if i+j < len(pattern):
                    tag = "laghu" if pattern[i+j] == 'L' else "guru" if pattern[i+j] == 'G' else None
                
                syllable_display = f"{syllable:>4}"
                if tag:
                    self.textbox.insert("end", syllable_display, tag)
                else:
                    self.textbox.insert("end", syllable_display)
                self.textbox.insert("end", " ")
            self.textbox.insert("end", "\n")
            
            # Pattern row (L/G below syllables)
            self.textbox.insert("end", "    ")
            for k, char in enumerate(row_pattern):
                tag = "laghu" if char == 'L' else "guru" if char == 'G' else None
                char_display = f"({char})"
                if tag:
                    self.textbox.insert("end", f"{char_display:>4}", tag)
                else:
                    self.textbox.insert("end", f"{char_display:>4}")
                self.textbox.insert("end", " ")
            self.textbox.insert("end", "\n\n")
    
    def display_error(self, error_message: str):
        """
        Display error message in red.
        
        Args:
            error_message: Error message to display
        """
        self.clear()
        error_text = f"ERROR\n\n{error_message}"
        self.textbox.insert("1.0", error_text)
        # Note: CTkTextbox doesn't support tags like tk.Text
        # Color formatting will be added in Phase 4 with custom implementation
    
    def display_info(self, info_message: str):
        """
        Display informational message.
        
        Args:
            info_message: Info message to display
        """
        self.clear()
        self.textbox.insert("1.0", f"INFO: {info_message}")
    
    def display_error(self, error_message: str):
        """
        Display error message in red.
        
        Args:
            error_message: Error message to display
        """
        self.clear()
        self.textbox.config(state="normal")
        self.textbox.insert("end", "ERROR\n\n", "error")
        self.textbox.insert("end", error_message)
        self.textbox.config(state="disabled")
    
    def display_info(self, info_message: str):
        """
        Display informational message.
        
        Args:
            info_message: Info message to display
        """
        self.clear()
        self.textbox.config(state="normal")
        self.textbox.insert("end", f"INFO: {info_message}", "info")
        self.textbox.config(state="disabled")
    
    def append_result(self, text: str):
        """
        Append text to existing results.
        
        Args:
            text: Text to append
        """
        self.textbox.config(state="normal")
        self.textbox.insert("end", f"\n{text}")
        self.textbox.config(state="disabled")
    
    def clear(self):
        """Clear all displayed results."""
        self.textbox.config(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.config(state="disabled")
    
    def set_placeholder(self, text: Optional[str] = None):
        """
        Set placeholder text in the display area.
        
        Args:
            text: Placeholder text (uses default if None)
        """
        placeholder = text or self.DEFAULT_PLACEHOLDER
        self.clear()
        self.textbox.config(state="normal")
        self.textbox.insert("1.0", placeholder)
        self.textbox.config(state="disabled")
    
    def get_text(self) -> str:
        """
        Get the current displayed text.
        
        Returns:
            Current text content
        """
        return self.textbox.get("1.0", "end-1c")
    
    def copy_to_clipboard(self) -> bool:
        """
        Copy displayed results to clipboard.
        
        Returns:
            True if copy was successful, False otherwise
        """
        if not CLIPBOARD_AVAILABLE:
            return False
        
        try:
            text = self.get_text()
            if text:
                pyperclip.copy(text)
                return True
        except Exception:
            pass
        
        return False
    
    def _format_dict_result(self, result: Dict[str, Any]) -> str:
        """
        Format dictionary result for display.
        
        Args:
            result: Dictionary containing analysis results
            
        Returns:
            Formatted string for display
        """
        lines = []
        
        # Input text
        if 'input' in result:
            lines.append(f"Input: {result['input']}")
            lines.append("")
        
        # Meter identification
        if 'meter' in result:
            lines.append(f"📊 Identified Meter: {result['meter']}")
            lines.append("")
        
        # Pattern
        if 'pattern' in result:
            lines.append(f"Pattern: {result['pattern']}")
            lines.append("")
        
        # Matches (for fuzzy matching)
        if 'matches' in result and isinstance(result['matches'], list):
            lines.append("Fuzzy Matches:")
            for i, match in enumerate(result['matches'], 1):
                if isinstance(match, dict):
                    meter = match.get('meter', 'Unknown')
                    score = match.get('score', 0)
                    lines.append(f"  {i}. {meter} (similarity: {score:.2f})")
                else:
                    lines.append(f"  {i}. {match}")
            lines.append("")
        
        # Additional fields
        for key, value in result.items():
            if key not in ['input', 'meter', 'pattern', 'matches']:
                lines.append(f"{key.capitalize()}: {value}")
        
        return "\n".join(lines)
    
    def display_analysis_placeholder(self, text_length: int):
        """
        Display placeholder for analysis in progress.
        
        Args:
            text_length: Length of input text being analyzed
        """
        self.clear()
        placeholder = (
            f"Input text received ({text_length} characters).\n\n"
            "Analysis integration will be implemented in Phase 3.\n\n"
            "For now, the UI structure is ready!"
        )
        self.textbox.insert("1.0", placeholder)
    
    def update_theme(self):
        """Update widget colors based on current theme."""
        # CTkTextbox handles theme updates automatically
        # This method is for future custom color implementations
        pass
    
    def is_empty(self) -> bool:
        """
        Check if the display is empty.
        
        Returns:
            True if empty, False otherwise
        """
        return len(self.get_text().strip()) == 0
