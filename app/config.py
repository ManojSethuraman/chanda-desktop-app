#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Manager for Chanda Desktop.

This module handles application settings persistence and management.
"""

import configparser
import os
from pathlib import Path
from typing import Any, Dict, Optional


class ConfigManager:
    """
    Manage application configuration and settings.
    
    Configuration is stored in a .ini file in the user's home directory.
    Settings are organized into sections: analysis, appearance, advanced, window.
    
    Attributes:
        config_file: Path to the configuration file
        config: Dictionary containing all configuration values
    """
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_file = self._get_config_file()
        self.config = self._default_config()
        self.load()
    
    @staticmethod
    def _get_config_file() -> Path:
        """
        Get the configuration file path.
        
        Returns:
            Path to config.ini in user's home directory
        """
        config_dir = Path.home() / '.chanda_desktop'
        config_dir.mkdir(exist_ok=True)
        return config_dir / 'config.ini'
    
    def _default_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Get default configuration values.
        
        Returns:
            Dictionary with default settings for all sections
        """
        return {
            'analysis': {
                'default_input_scheme': 'devanagari',
                'default_output_scheme': 'devanagari',
                'fuzzy_enabled': True,
                'fuzzy_k': 10,
                'verse_mode': False,
                'auto_analyze': False
            },
            'appearance': {
                'theme': 'system',  # system, light, dark
                'font_family': 'Nirmala UI',
                'font_size': 12,
                'lg_color_laghu': '#3b82f6',
                'lg_color_guru': '#ef4444'
            },
            'advanced': {
                'data_path': '',  # Empty = use default
                'language': 'sanskrit',
                'history_limit': 100
            },
            'window': {
                'width': 1200,
                'height': 800,
                'maximized': False,
                'position_x': 0,
                'position_y': 0
            }
        }
    
    def load(self):
        """
        Load configuration from file.
        
        If the file doesn't exist, default values are used.
        """
        if not self.config_file.exists():
            return
        
        parser = configparser.ConfigParser()
        parser.read(self.config_file, encoding='utf-8')
        
        # Update config from file
        for section in parser.sections():
            if section in self.config:
                for key, value in parser[section].items():
                    # Type conversion
                    if value.lower() in ('true', 'false'):
                        value = value.lower() == 'true'
                    elif value.isdigit():
                        value = int(value)
                    elif self._is_float(value):
                        value = float(value)
                    
                    self.config[section][key] = value
    
    def save(self):
        """Save configuration to file."""
        parser = configparser.ConfigParser()
        
        for section, settings in self.config.items():
            parser[section] = {}
            for key, value in settings.items():
                parser[section][key] = str(value)
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            parser.write(f)
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section name
            key: Setting key within the section
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        return self.config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any):
        """
        Set a configuration value.
        
        Args:
            section: Configuration section name
            key: Setting key within the section
            value: Value to set
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get all settings in a section.
        
        Args:
            section: Configuration section name
        
        Returns:
            Dictionary of settings in the section
        """
        return self.config.get(section, {}).copy()
    
    def update_section(self, section: str, settings: Dict[str, Any]):
        """
        Update multiple settings in a section.
        
        Args:
            section: Configuration section name
            settings: Dictionary of settings to update
        """
        if section not in self.config:
            self.config[section] = {}
        self.config[section].update(settings)
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.config = self._default_config()
        self.save()
    
    def reset_section(self, section: str):
        """
        Reset a specific section to default values.
        
        Args:
            section: Configuration section name
        """
        defaults = self._default_config()
        if section in defaults:
            self.config[section] = defaults[section].copy()
            self.save()
    
    @staticmethod
    def _is_float(value: str) -> bool:
        """
        Check if a string represents a float.
        
        Args:
            value: String to check
        
        Returns:
            True if string represents a float
        """
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"ConfigManager(file={self.config_file}, sections={list(self.config.keys())})"
