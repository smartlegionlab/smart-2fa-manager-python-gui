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
    QLineEdit,
    QPushButton,
)


class UnlockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart 2FA Manager - Unlock Storage")
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        info = QLabel("Enter password to unlock your TOTP storage:")
        layout.addWidget(info)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Master password")
        layout.addWidget(self.password_input)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Exit")
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Unlock")
        btn_ok.setDefault(True)
        btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

    def get_password(self):
        return self.password_input.text()
