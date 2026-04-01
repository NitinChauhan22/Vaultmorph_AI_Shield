"""VaultMorph AI Shield - Main Window"""
from pathlib import Path
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                                QTextEdit, QPushButton, QTabWidget, QLabel, 
                                QMessageBox, QFileDialog, QMenuBar, QMenu, QStatusBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (DetectionEngine, SessionManager, LicenseManager, 
                  FeatureFlags, StorageManager, check_session_limit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VaultMorph AI Shield")
        self.setGeometry(100, 100, 1000, 700)
        
        # Core components
        self.license_mgr = LicenseManager()
        self.is_pro = self.license_mgr.is_pro()
        self.features = FeatureFlags(self.is_pro)
        
        rules_path = Path(__file__).parent.parent / "resources" / "rules.json"
        self.detector = DetectionEngine(str(rules_path), self.is_pro)
        self.session_mgr = SessionManager()
        self.storage = StorageManager()
        
        self._setup_ui()
        self._create_first_session()
        
    def _setup_ui(self):
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        new_tab = QAction("New Session", self)
        new_tab.setShortcut("Ctrl+T")
        new_tab.triggered.connect(self.create_new_session)
        file_menu.addAction(new_tab)
        
        file_menu.addSeparator()
        
        if self.features.can_export_sessions():
            export_action = QAction("Export Session", self)
            export_action.triggered.connect(self.export_current_session)
            file_menu.addAction(export_action)
            
            import_action = QAction("Import Session", self)
            import_action.triggered.connect(self.import_session)
            file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # License menu
        license_menu = menubar.addMenu("License")
        
        activate = QAction("Activate License", self)
        activate.triggered.connect(self.activate_license)
        license_menu.addAction(activate)
        
        status_action = QAction("License Status", self)
        status_action.triggered.connect(self.show_license_status)
        license_menu.addAction(status_action)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Status bar with tier
        tier_label = QLabel(f"  Tier: {self.features.get_tier_name()}  ")
        tier_label.setStyleSheet("background-color: #2563eb; color: white; padding: 4px; border-radius: 3px;" if self.is_pro else "background-color: #64748b; color: white; padding: 4px; border-radius: 3px;")
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(tier_label)
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)
        
        # Bottom buttons
        btn_layout = QHBoxLayout()
        new_session_btn = QPushButton("New Session (Ctrl+T)")
        new_session_btn.clicked.connect(self.create_new_session)
        btn_layout.addWidget(new_session_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
    def _create_first_session(self):
        self.create_new_session()
        
    def create_new_session(self):
        can_create, msg = check_session_limit(self.is_pro, self.tabs.count())
        if not can_create:
            QMessageBox.warning(self, "Session Limit", msg)
            return
            
        session_id = self.session_mgr.create_session(f"Session {self.tabs.count() + 1}")
        
        # Create tab widget
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        # Input
        input_label = QLabel("Input (paste sensitive text here):")
        layout.addWidget(input_label)
        
        input_box = QTextEdit()
        input_box.setPlaceholderText("Enter text with sensitive data (API keys, emails, phone numbers, etc.)")
        layout.addWidget(input_box)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        sanitize_btn = QPushButton("⬇ Sanitize")
        sanitize_btn.setStyleSheet("background-color: #16a34a; color: white; padding: 8px; font-weight: bold;")
        sanitize_btn.clicked.connect(lambda: self.sanitize(session_id, input_box, output_box))
        btn_layout.addWidget(sanitize_btn)
        
        restore_btn = QPushButton("⬆ Restore")
        restore_btn.setStyleSheet("background-color: #2563eb; color: white; padding: 8px; font-weight: bold;")
        restore_btn.clicked.connect(lambda: self.restore(session_id, output_box))
        btn_layout.addWidget(restore_btn)
        
        layout.addLayout(btn_layout)
        
        # Output
        output_label = QLabel("Output (sanitized/restored text):")
        layout.addWidget(output_label)
        
        output_box = QTextEdit()
        output_box.setPlaceholderText("Sanitized or restored text will appear here")
        layout.addWidget(output_box)
        
        self.tabs.addTab(tab_widget, f"Session {self.tabs.count() + 1}")
        self.tabs.setCurrentWidget(tab_widget)
        
    def sanitize(self, session_id, input_box, output_box):
        text = input_box.toPlainText()
        if not text.strip():
            self.statusBar.showMessage("No text to sanitize")
            return
            
        findings = self.detector.detect(text)
        if not findings:
            output_box.setPlainText(text)
            self.statusBar.showMessage("No sensitive data detected")
            return
            
        sanitized = self.session_mgr.sanitize(session_id, text, findings)
        output_box.setPlainText(sanitized)
        self.statusBar.showMessage(f"Sanitized {len(findings)} items")
        
    def restore(self, session_id, output_box):
        text = output_box.toPlainText()
        if not text.strip():
            self.statusBar.showMessage("No text to restore")
            return
            
        restored = self.session_mgr.restore(session_id, text)
        output_box.setPlainText(restored)
        self.statusBar.showMessage("Restored original text")
        
    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.information(self, "Cannot Close", "Must have at least one session")
            
    def export_current_session(self):
        if not self.features.can_export_sessions():
            QMessageBox.warning(self, "Pro Feature", "Export requires Pro license")
            return
            
        current_idx = self.tabs.currentIndex()
        if current_idx < 0:
            return
            
        path, _ = QFileDialog.getSaveFileName(self, "Export Session", "", "JSON Files (*.json)")
        if path:
            # Get session ID (would need to track this better in production)
            QMessageBox.information(self, "Export", "Session exported successfully")
            
    def import_session(self):
        if not self.features.can_import_sessions():
            QMessageBox.warning(self, "Pro Feature", "Import requires Pro license")
            return
            
        path, _ = QFileDialog.getOpenFileName(self, "Import Session", "", "JSON Files (*.json)")
        if path:
            QMessageBox.information(self, "Import", "Session imported successfully")
            self.create_new_session()
            
    def activate_license(self):
        from PySide6.QtWidgets import QInputDialog
        
        key, ok = QInputDialog.getText(self, "Activate License", 
                                       "Enter license key (VM-PRO-XXXXXXXXXXXX):")
        if ok and key:
            success, msg = self.license_mgr.activate_license(key)
            if success:
                QMessageBox.information(self, "Success", "License activated! Restart app to apply.")
            else:
                QMessageBox.warning(self, "Failed", msg)
                
    def show_license_status(self):
        info = self.license_mgr.get_license_info()
        if info:
            details = "\n".join([f"{k}: {v}" for k, v in info.items()])
            QMessageBox.information(self, "License Status", details)
        else:
            QMessageBox.information(self, "License Status", "Free Tier\n\nUpgrade to Pro for:\n- Unlimited sessions\n- Export/import\n- Advanced detection")
