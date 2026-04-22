# ==============================================================
# Smart 2FA Manager (Gui)
# https://github.com/smartlegionlab/smart-2fa-manager-desktop
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
# ==============================================================
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QGroupBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class GetCodeDialog(QDialog):
    def __init__(self, parent=None, service="", code=""):
        super().__init__(parent)
        self.setWindowTitle(f"Smart 2FA Manager - TOTP Code: {service}")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel(f"Service: {service}")
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        code_group = QGroupBox("Current TOTP Code")
        code_layout = QVBoxLayout()

        self.code_label = QLabel(code)
        code_font = QFont("Monospace", 24)
        code_font.setBold(True)
        self.code_label.setFont(code_font)
        self.code_label.setAlignment(Qt.AlignCenter)
        self.code_label.setStyleSheet("color: #2a82da; padding: 10px;")
        code_layout.addWidget(self.code_label)

        code_group.setLayout(code_layout)
        layout.addWidget(code_group)

        btn_layout = QHBoxLayout()

        copy_btn = QPushButton("📋 Copy to Clipboard")
        copy_btn.clicked.connect(lambda: self.copy_code(code))

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)

        btn_layout.addWidget(copy_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        self.code = code

    def copy_code(self, code):
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(code)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Copied")
        msg.setText("Code copied to clipboard!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, msg.accept)
