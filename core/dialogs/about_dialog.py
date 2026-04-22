# ==============================================================
# Smart 2FA Manager (Gui)
# https://github.com/smartlegionlab/smart-2fa-manager-desktop
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
# ==============================================================
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from core import __version__ as ver


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Smart 2FA Manager")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        title = QLabel("🔐 Smart 2FA Manager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        version = QLabel(f"Version {ver}")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        layout.addSpacing(10)

        desc = QLabel(
            "A lightweight, offline TOTP 2FA manager for Linux.\n\n"
            "No cloud, no phone required. Store your secrets locally,\n"
            "generate codes, create encrypted backups, and sync with\n"
            "Google Authenticator via QR codes."
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addSpacing(10)

        author_label = QLabel(
            'Author: <a href="https://github.com/smartlegionlab/" style="color: #2a82da; text-decoration: none;">Alexander Suvorov</a>'
        )
        author_label.setOpenExternalLinks(True)
        author_label.setTextFormat(Qt.RichText)
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet("color: #888;")
        layout.addWidget(author_label)

        license_label = QLabel("License: BSD 3-Clause")
        license_label.setAlignment(Qt.AlignCenter)
        license_label.setStyleSheet("color: #888;")
        layout.addWidget(license_label)

        repo_label = QLabel(
            'Repository: <a href="https://github.com/smartlegionlab/smart-2fa-manager-desktop" style="color: #2a82da; text-decoration: none;">github.com/smartlegionlab/smart-2fa-manager-desktop</a>'
        )
        repo_label.setOpenExternalLinks(True)
        repo_label.setTextFormat(Qt.RichText)
        repo_label.setAlignment(Qt.AlignCenter)
        repo_label.setWordWrap(True)
        repo_label.setStyleSheet("color: #888;")
        layout.addWidget(repo_label)

        layout.addSpacing(10)

        btn_close = QPushButton("Close")
        btn_close.setMinimumHeight(35)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a72ca;
            }
        """)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
