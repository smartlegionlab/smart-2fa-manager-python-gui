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
    QMessageBox,
    QGroupBox,
)


class InitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart 2FA Manager - Initialize Storage")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        info = QLabel("Create a new encrypted storage for your TOTP secrets.")
        info.setWordWrap(True)
        layout.addWidget(info)

        group = QGroupBox("Set Master Password")
        group_layout = QVBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        group_layout.addWidget(self.password_input)

        self.confirm_input = QLineEdit()
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setPlaceholderText("Confirm password")
        group_layout.addWidget(self.confirm_input)

        group.setLayout(group_layout)
        layout.addWidget(group)

        warning = QLabel("⚠️ WARNING: If you lose this password, your secrets are lost forever!")
        warning.setStyleSheet("color: #ff9800;")
        warning.setWordWrap(True)
        layout.addWidget(warning)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Create")
        btn_ok.setDefault(True)
        btn_ok.clicked.connect(self.check_and_accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

    def check_and_accept(self):
        password = self.password_input.text()
        confirm = self.confirm_input.text()

        if not password:
            QMessageBox.warning(self, "Error", "Password cannot be empty!")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        self.accept()

    def get_password(self):
        return self.password_input.text()
