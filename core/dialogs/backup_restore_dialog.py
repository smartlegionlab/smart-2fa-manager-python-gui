# ==============================================================
# Smart 2FA Manager (Gui)
# https://github.com/smartlegionlab/smart-2fa-manager-desktop
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
# ==============================================================
from pathlib import Path
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QGroupBox,
)


class BackupRestoreDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart 2FA Manager - Restore from Backup")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        info = QLabel("Restore encrypted backup to a new storage.")
        info.setWordWrap(True)
        layout.addWidget(info)

        group1 = QGroupBox("Backup File")
        group1_layout = QHBoxLayout()

        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #888;")
        group1_layout.addWidget(self.file_label)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_file)
        group1_layout.addWidget(browse_btn)

        group1.setLayout(group1_layout)
        layout.addWidget(group1)

        group2 = QGroupBox("New Password")
        group2_layout = QVBoxLayout()

        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setPlaceholderText("New master password")
        group2_layout.addWidget(self.new_password)

        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setPlaceholderText("Confirm new password")
        group2_layout.addWidget(self.confirm_password)

        group2.setLayout(group2_layout)
        layout.addWidget(group2)

        warning = QLabel("⚠️ This will overwrite your existing storage!")
        warning.setStyleSheet("color: #ff9800;")
        layout.addWidget(warning)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Restore")
        btn_ok.setDefault(True)
        btn_ok.clicked.connect(self.check_and_accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        self.backup_file = None

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Backup File",
            str(Path.home() / ".2fa" / "backups"),
            "GPG Files (*.gpg);;All Files (*)"
        )
        if file_path:
            self.backup_file = file_path
            self.file_label.setText(file_path)
            self.file_label.setStyleSheet("color: #2a82da;")

    def check_and_accept(self):
        if not self.backup_file:
            QMessageBox.warning(self, "Error", "Please select a backup file!")
            return

        new_pass = self.new_password.text()
        confirm = self.confirm_password.text()

        if not new_pass:
            QMessageBox.warning(self, "Error", "Password cannot be empty!")
            return

        if new_pass != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return

        self.accept()

    def get_values(self):
        return self.backup_file, self.new_password.text()
