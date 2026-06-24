# Chanda Desktop - Sanskrit Meter Analyzer

A modern Windows desktop application for identifying and analyzing Sanskrit poetic meters using the Chanda library.

## Features

- 🎨 Modern GUI with dark/light themes
- 📝 Real-time Sanskrit meter identification
- 🌐 Multi-script support (7 transliteration schemes: Devanagari, IAST, ITRANS, Harvard-Kyoto, SLP1, Velthuis, WX)
- 🎨 **Color-coded Laghu-Guru visualization (Phase 4 ✅)** - Blue for Laghu, Red for Guru, Green for exact matches
- 📊 **Syllable pattern grid display (Phase 4 ✅)** - Visual grid with colored syllables and pattern indicators
- 🔍 Fuzzy matching with similarity scoring (Top-K results up to 50)
- ⭐ History tracking (50 items) and favorites (100 items) with persistence
- ⚙️ 10 keyboard shortcuts for efficient workflow
- 📁 Clipboard integration (paste/copy)
- 💾 Persistent configuration across sessions

## Requirements

- Python 3.8+
- Windows 10/11
- Chanda library v1.1.0+ (auto-installed from requirements.txt)

## Installation

See [INSTALLATION.md](INSTALLATION.md) for detailed setup instructions.

### Quick Start (Development)

```powershell
# 1. Navigate to chanda_desktop folder
cd chanda_desktop

# 2. Install all dependencies (includes chanda library)
pip install -r requirements.txt

# 3. Run the application
python main.py
```

### Key Installation Notes

- **Efficient Updates**: Chanda library is installed in editable mode (`-e ../`), so any updates to the parent library are immediately available
- **Standalone Capable**: Once dependencies are installed, the chanda_desktop folder can run independently
- **Fallback Import**: If chanda isn't installed via pip, the app will attempt to import from the parent directory

### For End Users

Download the standalone executable from the [Releases](https://github.com/ManojSethuraman/chanda-desktop-app/releases) page.

## Quick Start

1. Launch the application
2. Enter Sanskrit text in the input area
3. Click "Analyze" or press Ctrl+Enter
4. View results with meter identification, patterns, and analysis

## Project Structure

```
chanda_desktop/
├── main.py                 # Application entry point
├── app/                    # Core application logic
├── ui/                     # User interface components
├── models/                 # Data models
├── controllers/            # Business logic controllers
├── resources/              # Icons, fonts, themes
└── tests/                  # Test suite
```

## Technology Stack

- **GUI Framework**: CustomTkinter (MIT License)
- **Meter Analysis**: Chanda Library (AGPL-3.0)
- **Packaging**: PyInstaller
- **All dependencies**: 100% free/open-source

## Documentation

Full documentation is available in the parent directory:
- [Implementation Plan](../DESKTOP_APP_PLAN.md)
- [Quick Start Guide](../DESKTOP_APP_QUICKSTART.md)
- [Technical Architecture](../DESKTOP_APP_ARCHITECTURE.md)

## Development Status

This project is under active development. Current version: **v0.1.0-alpha**

See the [project board](https://github.com/hrishikeshrt/chanda/projects) for current status and roadmap.

## License

GNU Affero General Public License v3.0 - see [LICENSE](../LICENSE) file for details.

## Acknowledgments

- Based on the excellent [Chanda](https://github.com/hrishikeshrt/chanda) library by Hrishikesh Terdalkar
- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Author

**Hrishikesh Terdalkar**
- Email: hrishikeshrt@proton.me
- GitHub: [@hrishikeshrt](https://github.com/hrishikeshrt)
