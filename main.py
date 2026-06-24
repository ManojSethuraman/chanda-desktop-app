#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chanda Desktop Application - Main Entry Point.

A modern Windows desktop application for Sanskrit meter identification
and analysis.

Author: Hrishikesh Terdalkar
License: AGPL-3.0
"""

import sys
import os

# Try importing chanda library (should be installed via pip)
try:
    import chanda
except ImportError:
    # Fallback: Add parent directory to path if chanda not installed
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    try:
        import chanda
    except ImportError:
        print("Error: 'chanda' library not found!")
        print("Please install it with: pip install -e ../")
        print("Or ensure the parent 'chanda' package is accessible.")
        sys.exit(1)

from app.app import ChandaDesktopApp


def main():
    """
    Launch the Chanda Desktop Application.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    try:
        app = ChandaDesktopApp()
        app.run()
        return 0
    except KeyboardInterrupt:
        print("\nApplication interrupted by user.")
        return 0
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
