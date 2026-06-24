# Installation Guide - Chanda Desktop App

## Prerequisites

- **Python 3.8 or higher**
- **pip** (Python package installer)
- **Windows 10/11** (primary target platform)

## Installation Options

### Option 1: Development Setup (Recommended for Contributors)

This setup allows you to modify both the chanda library and desktop app, with changes reflected immediately.

```bash
# 1. Clone the repository
git clone https://github.com/ManojSethuraman/chanda-desktop-app.git
cd chanda-desktop-app

# 2. Install dependencies
# Note: This assumes chanda library is at C:\Chandojnana\chanda
# If your chanda library is elsewhere, edit requirements.txt line 6
pip install -r requirements.txt

# 3. Run the application
python main.py
```

**Important:** The `requirements.txt` contains: `-e C:\Chandojnana\chanda`  
If your chanda library is in a different location, update this path before running `pip install`.

### Option 2: Standalone Installation

If you have the chanda library already installed system-wide:

```bash
# 1. Ensure chanda is installed
pip install chanda

# 2. Navigate to chanda_desktop folder
cd chanda_desktop

# 3. Install only the desktop app dependencies
pip install customtkinter pillow pyperclip darkdetect

# 4. Run the application
python main.py
```

## Updating the Chanda Library

### If installed in editable mode (Option 1):
```bash
# Simply pull/update the parent chanda folder
cd /path/to/parent/chanda
git pull

# Changes are automatically reflected - no reinstall needed!
```

### If installed from PyPI (Option 2):
```bash
# Upgrade to the latest version
pip install --upgrade chanda
```

## Verifying Installation

Test that everything is working:

```bash
# Test chanda library import
python -c "import chanda; print(f'Chanda v{chanda.__version__} installed')"

# Test desktop app (opens GUI window)
cd chanda_desktop
python main.py
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'chanda'"

**Solution:**
```bash
# Install the chanda library
pip install -e ../  # If parent folder contains chanda
# OR
pip install chanda  # From PyPI
```

### "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
```bash
# Install desktop app dependencies
pip install -r requirements.txt
```

### Application won't start

**Check Python version:**
```bash
python --version  # Should be 3.8 or higher
```

**Check dependencies:**
```bash
pip list | findstr "chanda customtkinter"
```

## Folder Structure

```
chanda/                          (Parent - contains chanda library)
├── chanda/                      (Core library package)
│   ├── analyzer.py
│   ├── core.py
│   ├── data/                    (200+ meter definitions)
│   └── ...
├── chanda_desktop/              (Desktop application - CAN BE STANDALONE)
│   ├── main.py                  (Entry point)
│   ├── requirements.txt         (Dependencies including 'chanda')
│   ├── app/                     (Application logic)
│   ├── ui/                      (User interface)
│   └── ...
├── setup.py                     (Chanda library setup)
└── pyproject.toml              (Chanda library config)
```

## Development Notes

- **Editable Install (`-e`)**: Links the package instead of copying files. Changes to source code are immediately available.
- **requirements.txt**: Contains `-e ../` which installs the parent chanda library in editable mode.
- **Fallback Import**: `main.py` includes fallback logic to add parent directory to path if chanda isn't installed.

## Distribution

When distributing the desktop app:

1. **Include parent chanda folder** OR
2. **Ensure chanda is installable** via `pip install chanda`

For standalone executable (future):
- Use PyInstaller to bundle everything
- See packaging instructions in main README.md
