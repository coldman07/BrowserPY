# BrowserPY
Simple Browser using python
# 🌐 Simple Browser

A lightweight, tabbed web browser built with Python and PyQt5! 

## ✨ Features

- 📑 **Tabbed browsing** - Open multiple websites in a single window
- 🧭 **Navigation controls** - Back, forward, reload, and home buttons
- 📝 **Address bar** - Type URLs directly to navigate
- 🔄 **Loading indicators** - Progress bar and status messages
- 🏷️ **Dynamic tab titles** - Automatically updates based on page content
- ➕ **Simple tab management** - Add and close tabs with ease

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- PyQt5 and PyQtWebEngine packages

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/simple-browser.git
   cd simple-browser
   ```

2. Install required dependencies:
   ```bash
   pip install PyQt5 PyQtWebEngine
   ```

3. Run the browser:
   ```bash
   python browserpy.py
   ```

## 🚀 Usage

- **Navigate**: Enter a URL in the address bar and press Enter
- **New Tab**: Click the "+" button to open a new tab
- **Close Tab**: Click the "×" on a tab to close it
- **Go Back/Forward**: Use the "←" and "→" buttons
- **Reload Page**: Click the "↻" button
- **Home Page**: Click the "🏠" button to go to Google

## 🖼️ Screenshot

![Simple Browser Screenshot](./screenshot.png)

## 🧰 Technical Details

The browser is built on:
- **PyQt5** - For the graphical user interface
- **QtWebEngine** - Chromium-based web rendering engine

## 🔧 Customization

You can easily customize the browser by:
- Changing the default home page in the `navigate_home()` method
- Modifying the window size in the `__init__()` method
- Adding new navigation buttons to the toolbar

## 💡 Future Improvements

- Bookmarks management
- Browsing history
- Download manager
- Settings panel
- Extensions support
- Keyboard shortcuts


## 🙏 Acknowledgements

- PyQt5 team for their amazing framework
- The Chromium project for the web engine
- All open-source contributors who make projects like this possible

---

Made with ❤️ by a Python enthusiast
