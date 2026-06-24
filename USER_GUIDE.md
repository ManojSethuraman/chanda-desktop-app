# Chanda Desktop - End User Guide

## For End Users (No Technical Setup Required)

### What You Need
- **Windows 10 or 11**
- **Nothing else!** No Python, no installation, no setup

### How to Run the App

#### Option 1: Download Pre-Built Executable (Easiest)

1. **Download** `ChandaDesktop.exe` from the releases page or from your distribution source
2. **Save** it anywhere on your computer (Desktop, Documents, etc.)
3. **Double-click** `ChandaDesktop.exe` to launch
4. **That's it!** The app will open immediately

#### Option 2: Build From Source (For Developers)

If you want to build the executable yourself:

1. **Install Python 3.8+** from python.org
2. **Clone or download** this repository
3. **Install dependencies:**
   ```powershell
   cd C:\Projects\chanda-desktop-app
   python -m pip install -r requirements.txt
   python -m pip install pyinstaller
   ```
4. **Build the executable:**
   ```powershell
   .\build_exe.ps1
   ```
5. **Find the executable** at `dist\ChandaDesktop.exe`

---

## Using the Application

### Quick Start

1. **Launch** the app by double-clicking `ChandaDesktop.exe`
2. **Select Script** - Choose your transliteration scheme from the dropdown (Devanagari, IAST, etc.)
   - Don't worry! The app auto-detects your input, this is just for reference
3. **Enter Text** - Type or paste Sanskrit text in the input area
4. **Click Analyze** (or press `Ctrl+Enter`)
5. **View Results** - See color-coded patterns and identified meters

### Understanding the Display

#### Color Code:
- **Blue (L)** = Laghu (light syllable) - Short vowel or consonant without heavy markers
- **Red (G)** = Guru (heavy syllable) - Long vowel, anusvara, visarga, or conjunct
- **Green Text** = Exact meter match found

#### Example Output:
```
Line 1: धर्मक्षेत्रे कुरुक्षेत्रे
  Pattern: GGGGLGGG (8 syllables)
  
  Syllables:
    ध र्म क्षे त्रे  कु  रु क्षे त्रे
   (G) (G) (G) (G)  (L) (G) (G) (G)
   
  Identified Meters:
    1. [EXACT] वक्त्र
    2. [EXACT] अनुष्टुभ्
```

### Features

#### Clipboard Integration
- **Paste Button** - Click to paste from clipboard (or `Ctrl+V`)
- **Copy Button** - Right-click results to copy (or `Ctrl+C`)

#### History & Favorites
- **Recent Analyses** - Last 50 analyses automatically saved
- **Favorites** - Double-click any history item to mark as favorite
- **Clear History** - Button to clear recent history (favorites remain)

#### Fuzzy Matching
- **Enable Fuzzy** - Check the "Fuzzy Match" box
- **Top K Value** - Select how many approximate matches to show (1-50)
- Use fuzzy matching when:
  - Text doesn't match known meters exactly
  - You want to find similar meters
  - Exploring variations and near-matches

#### Multi-Line Verses
- Paste multiple lines separated by Enter
- App analyzes verse structure automatically
- Shows uniform/non-uniform pattern detection
- Identifies common meters across lines

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Analyze text |
| `Ctrl+L` | Clear input |
| `Ctrl+V` | Paste from clipboard |
| `Ctrl+C` | Copy selected text |
| `Ctrl+N` | Clear results |
| `Ctrl+F` | Toggle fuzzy matching |
| `Ctrl+H` | Clear history |
| `Ctrl+Q` | Quit application |
| `F5` | Toggle theme (Dark/Light) |

### Settings

#### Theme
- Click the **Theme** button (top-right) to toggle Dark/Light mode
- Setting persists across sessions
- Auto-detects system theme on first launch

#### Script Selection
- Choose from 7 transliteration schemes:
  - Devanagari (default)
  - IAST (International Alphabet of Sanskrit Transliteration)
  - ITRANS (ASCII-based)
  - Harvard-Kyoto (ASCII-based)
  - SLP1 (Sanskrit Library Phonetic)
  - Velthuis (ASCII-based)
  - WX (Romanization)
- **Note:** Selection is for reference only - app auto-detects your input

---

## Troubleshooting

### "Windows protected your PC" message

**This is normal for unsigned executables.**

To run anyway:
1. Click "More info"
2. Click "Run anyway"

This appears because the .exe is not digitally signed (costs money). The app is safe.

### App won't start / Crashes immediately

**Try these:**
1. **Right-click** the .exe → **Properties** → **Compatibility**
2. Check "Run this program as an administrator"
3. Apply and try again

### Meter names show as boxes/gibberish

**Your system may need Devanagari font support.**

Install Devanagari fonts:
1. Open **Settings** → **Time & Language** → **Language**
2. Add **Hindi** language pack
3. Restart the app

### Analysis says "No matching meters found"

**This is normal!** It means:
- Text doesn't match any standard Sanskrit meter
- Try enabling **Fuzzy Matching** for approximate matches
- Check text for typos or incorrect syllable weights

### App is slow on first launch

**First launch takes 5-10 seconds** while loading 200+ meter definitions. Subsequent launches are faster.

---

## Example Analyses

### Example 1: Anuṣṭubh (Gītā Śloka)
```
Input: धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः

Result:
  Pattern: GGGGLGGG LLGGLGLG (16 syllables)
  Meter: अनुष्टुभ् (Anuṣṭubh) [EXACT]
```

### Example 2: Vasantatilakā
```
Input: वन्देऽहं देवमीशं तमसापारं

Result:
  Pattern: GLGGLGGLGGGLGL (14 syllables)
  Meter: वसन्ततिलका (Vasantatilakā) [EXACT]
```

### Example 3: Fuzzy Match
```
Input: कविता रचना है

Result (with Fuzzy enabled):
  Pattern: LLGLLGG (7 syllables)
  Fuzzy Matches:
    1. चित्रपदा (87.5% similar)
    2. हंसमाला (85.7% similar)
    3. रमणी (83.3% similar)
```

---

## About

**Chanda Desktop** is a Sanskrit meter analyzer that identifies and analyzes chandas (meters) in Sanskrit poetry.

**Features:**
- Analyzes single lines or complete verses
- Supports 7 transliteration schemes
- Color-coded syllable patterns
- Fuzzy matching for approximate meters
- History and favorites tracking
- Offline - no internet required

**Based on:**
- [Chanda Library](https://github.com/hrishikeshrt/chanda) by Hrishikesh Terdalkar
- Contains 200+ meter definitions from classical Sanskrit texts

**License:** AGPL-3.0 (Open source, free to use)

**Version:** 1.0.0

---

## Support

For issues, questions, or contributions:
- GitHub Issues: [Report a bug or request a feature]
- Documentation: See README.md for developer documentation

---

## Credits

- **Chanda Library:** Hrishikesh Terdalkar
- **Desktop App:** Development team
- **Meter Definitions:** Traditional Sanskrit prosody texts

Thank you for using Chanda Desktop! 🙏
