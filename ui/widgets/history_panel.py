#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
History Panel Widget for Chanda Desktop.

This module provides a custom widget for managing analysis history
and favorites with persistent storage.
"""

import customtkinter as ctk
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime


class HistoryPanel(ctk.CTkFrame):
    """
    Custom widget for managing analysis history and favorites.
    
    Features:
    - Tabbed interface with Recent and Favorites tabs
    - Session history list (recent analyses)
    - Favorites management (save/remove)
    - Click to restore previous analysis
    - Clear history option
    - Persistence to config file
    - Meter browser button
    
    Attributes:
        config_manager: Configuration manager for persistence
        on_item_select: Optional callback when history item is selected
        on_meter_browser: Optional callback for meter browser button
        history_items: List of recent analysis items
        favorite_items: List of favorite items
    """
    
    MAX_HISTORY = 10
    MAX_FAVORITES = 100
    
    def __init__(
        self,
        parent,
        config_manager=None,
        on_item_select: Optional[Callable] = None,
        on_meter_browser: Optional[Callable] = None,
        **kwargs
    ):
        """
        Initialize the history panel widget.
        
        Args:
            parent: Parent widget
            config_manager: Optional ConfigManager instance for persistence
            on_item_select: Optional callback when item is selected
            on_meter_browser: Optional callback for meter browser button
            **kwargs: Additional arguments passed to CTkFrame
        """
        super().__init__(parent, **kwargs)
        
        self.config_manager = config_manager
        self.on_item_select = on_item_select
        self.on_meter_browser_callback = on_meter_browser
        
        # Initialize data
        self.history_items: List[Dict[str, Any]] = []
        self.favorite_items: List[Dict[str, Any]] = []
        
        # Build the UI
        self._create_ui()
        
        # Load saved history and favorites
        self._load_from_config()
    
    def _create_ui(self):
        """Create the UI components."""
        # Header with count badge
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=5, padx=10, fill="x")
        
        header = ctk.CTkLabel(
            header_frame,
            text="History & Info",
            font=("Arial", 14, "bold")
        )
        header.pack(side="left")
        
        self.count_label = ctk.CTkLabel(
            header_frame,
            text="(0)",
            font=("Arial", 10),
            text_color="gray"
        )
        self.count_label.pack(side="left", padx=5)
        
        # Tabview for History and Favorites
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add tabs
        self.tabview.add("Recent")
        self.tabview.add("Favorites")
        
        # Recent tab - scrollable frame for history items
        self.recent_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("Recent"),
            fg_color="transparent"
        )
        self.recent_frame.pack(fill="both", expand=True, pady=5, padx=5)
        
        self.recent_placeholder = ctk.CTkLabel(
            self.recent_frame,
            text="Recent analyses will appear here",
            font=("Arial", 11),
            text_color="gray"
        )
        self.recent_placeholder.pack(pady=20)
        
        # Favorites tab - scrollable frame for favorite items
        self.favorites_frame = ctk.CTkScrollableFrame(
            self.tabview.tab("Favorites"),
            fg_color="transparent"
        )
        self.favorites_frame.pack(fill="both", expand=True, pady=5, padx=5)
        
        self.favorites_placeholder = ctk.CTkLabel(
            self.favorites_frame,
            text="Favorite analyses will appear here",
            font=("Arial", 11),
            text_color="gray"
        )
        self.favorites_placeholder.pack(pady=20)
        
        # Meter browser button
        self.btn_meter_browser = ctk.CTkButton(
            self,
            text="Browse Meters",
            command=self._on_meter_browser_click
        )
        self.btn_meter_browser.pack(pady=10, padx=10)
    
    def add_to_history(self, text: str, result: Any = None, metadata: Optional[Dict] = None):
        """
        Add analysis to history.
        
        Args:
            text: Input text that was analyzed
            result: Analysis result (can be any type)
            metadata: Optional metadata (script, fuzzy settings, etc.)
        """
        item = {
            'text': text[:100],  # Store first 100 chars
            'full_text': text,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # Add to beginning of list
        self.history_items.insert(0, item)
        
        # Limit history size
        if len(self.history_items) > self.MAX_HISTORY:
            self.history_items = self.history_items[:self.MAX_HISTORY]
        
        # Update UI
        self._refresh_history_display()
        
        # Update count badge
        self.count_label.configure(text=f"({len(self.history_items)})")
        
        # Save to config
        self._save_to_config()
    
    def add_to_favorites(self, text: str, result: Any = None, metadata: Optional[Dict] = None):
        """
        Add to favorites.
        
        Args:
            text: Input text
            result: Analysis result
            metadata: Optional metadata
        """
        item = {
            'text': text[:100],
            'full_text': text,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        # Check if already in favorites
        for fav in self.favorite_items:
            if fav.get('full_text') == text:
                return  # Already favorited
        
        self.favorite_items.insert(0, item)
        
        # Limit favorites size
        if len(self.favorite_items) > self.MAX_FAVORITES:
            self.favorite_items = self.favorite_items[:self.MAX_FAVORITES]
        
        # Update UI
        self._refresh_favorites_display()
        
        # Save to config
        self._save_to_config()
    
    def remove_from_favorites(self, index: int):
        """
        Remove item from favorites by index.
        
        Args:
            index: Index of item to remove
        """
        if 0 <= index < len(self.favorite_items):
            self.favorite_items.pop(index)
            self._refresh_favorites_display()
            self._save_to_config()
    
    def clear_history(self):
        """Clear all history."""
        self.history_items = []
        self._refresh_history_display()
        self.count_label.configure(text="(0)")
        self._save_to_config()
    
    def clear_favorites(self):
        """Clear all favorites."""
        self.favorite_items = []
        self._refresh_favorites_display()
        self._save_to_config()
    
    def get_selected(self) -> Optional[Dict[str, Any]]:
        """
        Return selected history item (placeholder for future implementation).
        
        Returns:
            Selected history item or None
        """
        # This will be implemented when we add item selection UI
        return None
    
    def _refresh_history_display(self):
        """Refresh the history tab display."""
        # Clear existing widgets
        for widget in self.recent_frame.winfo_children():
            widget.destroy()
        
        if not self.history_items:
            # Show placeholder
            self.recent_placeholder = ctk.CTkLabel(
                self.recent_frame,
                text="Recent analyses will appear here",
                font=("Arial", 11),
                text_color="gray"
            )
            self.recent_placeholder.pack(pady=20)
        else:
            # Display history items
            for i, item in enumerate(self.history_items[:20]):  # Show last 20
                self._create_history_item_widget(self.recent_frame, item, i)
    
    def _refresh_favorites_display(self):
        """Refresh the favorites tab display."""
        # Clear existing widgets
        for widget in self.favorites_frame.winfo_children():
            widget.destroy()
        
        if not self.favorite_items:
            # Show placeholder
            self.favorites_placeholder = ctk.CTkLabel(
                self.favorites_frame,
                text="Favorite analyses will appear here",
                font=("Arial", 11),
                text_color="gray"
            )
            self.favorites_placeholder.pack(pady=20)
        else:
            # Display favorite items
            for i, item in enumerate(self.favorite_items):
                self._create_favorite_item_widget(self.favorites_frame, item, i)
    
    def _create_history_item_widget(self, parent, item: Dict, index: int):
        """Create a widget for a history item."""
        frame = ctk.CTkFrame(parent, fg_color=("#d0d0d0", "#2d2d2d"), border_width=1, border_color=("#b0b0b0", "#404040"))
        frame.pack(fill="x", pady=3, padx=2)
        
        # Text preview (truncated)
        text_preview = item['text'][:50] + "..." if len(item['text']) > 50 else item['text']
        
        # Timestamp
        timestamp = datetime.fromisoformat(item['timestamp']).strftime('%H:%M')
        
        btn = ctk.CTkButton(
            frame,
            text=f"[{timestamp}] {text_preview}",
            font=("Arial", 10),
            height=32,
            fg_color="transparent",
            text_color=("#000000", "#ffffff"),
            hover_color=("#c0c0c0", "#3d3d3d"),
            anchor="w",
            command=lambda: self._on_history_item_click(item)
        )
        btn.pack(fill="x", side="left", expand=True, padx=5, pady=2)
    
    def _create_favorite_item_widget(self, parent, item: Dict, index: int):
        """Create a widget for a favorite item."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=2, padx=2)
        
        # Text preview (truncated)
        text_preview = item['text'][:40] + "..." if len(item['text']) > 40 else item['text']
        
        btn = ctk.CTkButton(
            frame,
            text=f"* {text_preview}",
            font=("Arial", 9),
            height=25,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            anchor="w",
            command=lambda: self._on_favorite_item_click(item)
        )
        btn.pack(fill="x", side="left", expand=True)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            frame,
            text="×",
            width=25,
            height=25,
            fg_color="transparent",
            hover_color=("red", "darkred"),
            command=lambda: self.remove_from_favorites(index)
        )
        remove_btn.pack(side="right")
    
    def _on_history_item_click(self, item: Dict):
        """Handle history item click."""
        if self.on_item_select:
            self.on_item_select(item)
    
    def _on_favorite_item_click(self, item: Dict):
        """Handle favorite item click."""
        if self.on_item_select:
            self.on_item_select(item)
    
    def _on_meter_browser_click(self):
        """Handle meter browser button click."""
        if self.on_meter_browser_callback:
            self.on_meter_browser_callback()
    
    def _load_from_config(self):
        """Load history and favorites from config (placeholder)."""
        # This will be implemented in Phase 3 when we integrate with ConfigManager
        # For now, just placeholder
        pass
    
    def _save_to_config(self):
        """Save history and favorites to config (placeholder)."""
        # This will be implemented in Phase 3 when we integrate with ConfigManager
        # For now, just placeholder
        pass
