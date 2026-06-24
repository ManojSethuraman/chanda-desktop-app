#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager for Chanda Desktop.

This module handles application themes and appearance settings.
"""

import customtkinter as ctk
from typing import Dict, Any


class ThemeManager:
    """
    Manage application themes and color schemes.
    
    Supports light, dark, and system themes with customizable color schemes
    for Laghu-Guru visualization.
    
    Attributes:
        current_theme: Current theme mode (light, dark, or system)
        color_scheme: Custom color scheme for analysis display
    """
    
    def __init__(self, config_manager=None):
        """
        Initialize the theme manager.
        
        Args:
            config_manager: Optional ConfigManager instance for persistence
        """
        self.config_manager = config_manager
        self.current_theme = "system"
        self.color_scheme = self._default_color_scheme()
        
        # Load from config if available
        if config_manager:
            self._load_from_config()
    
    def _default_color_scheme(self) -> Dict[str, str]:
        """
        Get default color scheme.
        
        Returns:
            Dictionary with color definitions
        """
        return {
            # Laghu-Guru colors
            'laghu': '#3b82f6',  # Blue
            'guru': '#ef4444',   # Red
            
            # Theme colors
            'bg_light': '#ffffff',
            'bg_dark': '#1e1e1e',
            'fg_light': '#000000',
            'fg_dark': '#ffffff',
            
            # Accent colors
            'accent_blue': '#1f6aa5',
            'accent_blue_hover': '#144870',
            'accent_green': '#10b981',
            'accent_red': '#ef4444',
            'accent_yellow': '#f59e0b',
            
            # UI element colors
            'button_primary': '#1f6aa5',
            'button_primary_hover': '#144870',
            'button_secondary': '#6b7280',
            'button_secondary_hover': '#4b5563',
            
            # Text colors
            'text_primary': '#1f2937',
            'text_secondary': '#6b7280',
            'text_disabled': '#9ca3af',
            
            # Border colors
            'border_light': '#e5e7eb',
            'border_dark': '#374151'
        }
    
    def _load_from_config(self):
        """Load theme settings from configuration."""
        if self.config_manager:
            appearance = self.config_manager.get_section('appearance')
            self.current_theme = appearance.get('theme', 'system')
            self.color_scheme['laghu'] = appearance.get('lg_color_laghu', '#3b82f6')
            self.color_scheme['guru'] = appearance.get('lg_color_guru', '#ef4444')
    
    def _save_to_config(self):
        """Save theme settings to configuration."""
        if self.config_manager:
            self.config_manager.set('appearance', 'theme', self.current_theme)
            self.config_manager.set('appearance', 'lg_color_laghu', self.color_scheme['laghu'])
            self.config_manager.set('appearance', 'lg_color_guru', self.color_scheme['guru'])
            self.config_manager.save()
    
    def set_theme(self, theme: str):
        """
        Set the application theme.
        
        Args:
            theme: Theme mode ('light', 'dark', or 'system')
        """
        if theme.lower() in ('light', 'dark', 'system'):
            self.current_theme = theme.lower()
            ctk.set_appearance_mode(self.current_theme)
            self._save_to_config()
    
    def get_theme(self) -> str:
        """
        Get the current theme mode.
        
        Returns:
            Current theme mode string
        """
        return self.current_theme
    
    def toggle_theme(self) -> str:
        """
        Toggle between light and dark themes.
        
        Returns:
            New theme mode
        """
        current = ctk.get_appearance_mode()
        new_mode = "light" if current == "Dark" else "dark"
        self.set_theme(new_mode)
        return new_mode
    
    def get_color(self, color_key: str) -> str:
        """
        Get a color from the color scheme.
        
        Args:
            color_key: Key for the color in the scheme
        
        Returns:
            Hex color string
        """
        return self.color_scheme.get(color_key, '#000000')
    
    def set_color(self, color_key: str, hex_color: str):
        """
        Set a custom color in the scheme.
        
        Args:
            color_key: Key for the color in the scheme
            hex_color: Hex color string (e.g., '#3b82f6')
        """
        if self._is_valid_hex_color(hex_color):
            self.color_scheme[color_key] = hex_color
            self._save_to_config()
    
    def set_laghu_guru_colors(self, laghu_color: str, guru_color: str):
        """
        Set custom colors for Laghu-Guru visualization.
        
        Args:
            laghu_color: Hex color for Laghu (light) syllables
            guru_color: Hex color for Guru (heavy) syllables
        """
        if self._is_valid_hex_color(laghu_color):
            self.color_scheme['laghu'] = laghu_color
        if self._is_valid_hex_color(guru_color):
            self.color_scheme['guru'] = guru_color
        self._save_to_config()
    
    def get_laghu_color(self) -> str:
        """Get the Laghu syllable color."""
        return self.color_scheme['laghu']
    
    def get_guru_color(self) -> str:
        """Get the Guru syllable color."""
        return self.color_scheme['guru']
    
    def reset_colors(self):
        """Reset color scheme to defaults."""
        self.color_scheme = self._default_color_scheme()
        self._save_to_config()
    
    def apply_to_widget(self, widget, widget_type: str = 'default'):
        """
        Apply theme colors to a widget.
        
        Args:
            widget: The widget to apply colors to
            widget_type: Type of widget ('button', 'label', 'entry', etc.)
        """
        # This method can be extended to apply colors based on current theme
        # and widget type
        pass
    
    @staticmethod
    def _is_valid_hex_color(color: str) -> bool:
        """
        Validate hex color string.
        
        Args:
            color: Hex color string to validate
        
        Returns:
            True if valid hex color
        """
        if not color.startswith('#'):
            return False
        if len(color) not in (4, 7):  # #RGB or #RRGGBB
            return False
        try:
            int(color[1:], 16)
            return True
        except ValueError:
            return False
    
    def get_theme_icon(self) -> str:
        """
        Get the appropriate icon for current theme.
        
        Returns:
            Emoji/icon string for theme toggle button
        """
        current = ctk.get_appearance_mode()
        return "☀️" if current == "Dark" else "🌙"
    
    def __repr__(self) -> str:
        """String representation of theme manager."""
        return f"ThemeManager(theme={self.current_theme})"
