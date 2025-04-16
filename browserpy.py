#!/usr/bin/env python3
# Simple Standalone Web Browser using PyQt5
# Requirements: pip install PyQt5 PyQtWebEngine

import sys
from PyQt5.QtCore import QUrl, Qt, QSize
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QToolBar, QAction, QStatusBar, QProgressBar, QTabWidget, QWidget, QVBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class WebBrowserTab(QWidget):
    """Individual browser tab component"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        
        # Create a layout for this tab
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Connect signals
        self.browser.loadStarted.connect(self.load_started)
        self.browser.loadProgress.connect(self.load_progress)
        self.browser.loadFinished.connect(self.load_finished)
        self.browser.titleChanged.connect(self.title_changed)
    
    def navigate_to_url(self, url):
        """Navigate to the specified URL"""
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))
    
    def load_started(self):
        """Slot called when page load starts"""
        if self.parent() and hasattr(self.parent(), 'statusBar'):
            self.parent().statusBar().showMessage("Loading...")
            if hasattr(self.parent(), 'progress_bar'):
                self.parent().progress_bar.show()
    
    def load_progress(self, progress):
        """Slot to update progress bar during page load"""
        if self.parent() and hasattr(self.parent(), 'progress_bar'):
            self.parent().progress_bar.setValue(progress)
    
    def load_finished(self, success):
        """Slot called when page load finishes"""
        if self.parent():
            if hasattr(self.parent(), 'statusBar'):
                if success:
                    self.parent().statusBar().showMessage("Page loaded", 2000)
                else:
                    self.parent().statusBar().showMessage("Page failed to load", 2000)
            if hasattr(self.parent(), 'progress_bar'):
                self.parent().progress_bar.hide()
            
            # Update URL bar with current URL
            if hasattr(self.parent(), 'url_bar'):
                self.parent().url_bar.setText(self.browser.url().toString())
                
            # Update window title
            if hasattr(self.parent(), 'setWindowTitle'):
                title = self.browser.page().title()
                self.parent().setWindowTitle(f"{title} - Simple Browser")
    
    def title_changed(self, title):
        """Slot called when page title changes"""
        # Update the tab text
        if self.parent() and hasattr(self.parent(), 'tabs'):
            index = self.parent().tabs.indexOf(self)
            if index >= 0:
                self.parent().tabs.setTabText(index, title[:15] + "..." if len(title) > 15 else title)
                self.parent().setWindowTitle(f"{title} - Simple Browser")
    
    def current_url(self):
        """Get the current URL"""
        return self.browser.url().toString()
    
    def go_back(self):
        """Go back to the previous page"""
        self.browser.back()
    
    def go_forward(self):
        """Go forward to the next page"""
        self.browser.forward()
    
    def reload_page(self):
        """Reload the current page"""
        self.browser.reload()


class SimpleBrowser(QMainWindow):
    """Main browser window with navigation toolbar"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 1024, 768)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)
        
        # Create first tab
        self.add_new_tab()
        
        # Create a toolbar
        navigation_bar = QToolBar("Navigation")
        navigation_bar.setIconSize(QSize(16, 16))
        self.addToolBar(navigation_bar)
        
        # Add navigation buttons
        back_button = QAction("←", self)
        back_button.setStatusTip("Go back to the previous page")
        back_button.triggered.connect(self.navigate_back)
        navigation_bar.addAction(back_button)
        
        forward_button = QAction("→", self)
        forward_button.setStatusTip("Go forward to the next page")
        forward_button.triggered.connect(self.navigate_forward)
        navigation_bar.addAction(forward_button)
        
        reload_button = QAction("↻", self)
        reload_button.setStatusTip("Reload the current page")
        reload_button.triggered.connect(self.reload_current)
        navigation_bar.addAction(reload_button)
        
        home_button = QAction("🏠", self)
        home_button.setStatusTip("Go to the home page")
        home_button.triggered.connect(self.navigate_home)
        navigation_bar.addAction(home_button)
        
        # Add URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addWidget(self.url_bar)
        
        # Add new tab button
        new_tab_button = QAction("+", self)
        new_tab_button.setStatusTip("Open a new tab")
        new_tab_button.triggered.connect(self.add_new_tab)
        navigation_bar.addAction(new_tab_button)
        
        # Create status bar
        self.setStatusBar(QStatusBar())
        
        # Create progress bar for loading
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(120)
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()
        
        # Connect tab changed signal
        self.tabs.currentChanged.connect(self.tab_changed)
    
    def add_new_tab(self, url=None):
        """Add a new browser tab"""
        tab = WebBrowserTab(self)
        
        if url:
            tab.navigate_to_url(url)
            
        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)
        
        # Update URL bar when tab is added
        self.url_bar.setText(tab.current_url())
        return tab
    
    def close_tab(self, index):
        """Close the tab at the given index"""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            # Don't close the last tab, just navigate to home
            self.navigate_home()
    
    def tab_changed(self, index):
        """Called when the user switches tabs"""
        if index >= 0:
            current_tab = self.tabs.widget(index)
            self.url_bar.setText(current_tab.current_url())
            title = self.tabs.tabText(index)
            self.setWindowTitle(f"{title} - Simple Browser")
    
    def navigate_to_url(self):
        """Navigate to the URL in the URL bar"""
        url = self.url_bar.text()
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.navigate_to_url(url)
    
    def navigate_back(self):
        """Navigate back in the current tab"""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.go_back()
    
    def navigate_forward(self):
        """Navigate forward in the current tab"""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.go_forward()
    
    def reload_current(self):
        """Reload the current tab"""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.reload_page()
    
    def navigate_home(self):
        """Navigate to the home page (Google)"""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.navigate_to_url("https://www.google.com")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec_())
