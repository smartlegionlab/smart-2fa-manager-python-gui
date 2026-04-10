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
    QGridLayout,
    QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from core import __version__ as ver


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


class AddServiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Smart 2FA Manager - Add Service")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        group1 = QGroupBox("Service Information")
        group1_layout = QGridLayout()

        group1_layout.addWidget(QLabel("Service Name:"), 0, 0)
        self.service_input = QLineEdit()
        self.service_input.setPlaceholderText("e.g., github, google, aws")
        group1_layout.addWidget(self.service_input, 0, 1)

        group1.setLayout(group1_layout)
        layout.addWidget(group1)

        group2 = QGroupBox("TOTP Secret")
        group2_layout = QVBoxLayout()

        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("Enter secret key (base32)")
        group2_layout.addWidget(self.secret_input)

        note = QLabel("Secret is case-insensitive and spaces will be removed.")
        note.setStyleSheet("color: #888; font-size: 10px;")
        group2_layout.addWidget(note)

        group2.setLayout(group2_layout)
        layout.addWidget(group2)

        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_ok = QPushButton("Add")
        btn_ok.setDefault(True)
        btn_ok.setStyleSheet("background-color: #2a82da;")
        btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

    def get_values(self):
        service = self.service_input.text().strip().lower().replace(' ', '_')
        secret = ''.join(self.secret_input.text().split()).upper()
        return service, secret


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


class QRCodeDialog(QDialog):
    def __init__(self, parent=None, service="", secret=""):
        super().__init__(parent)
        self.setWindowTitle(f"Smart 2FA Manager - QR Code: {service}")
        self.setMinimumWidth(400)
        self.setMinimumHeight(450)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel(f"Scan QR code for: {service}")
        title_font = QFont()
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        uri = f"otpauth://totp/{service}?secret={secret}&issuer=Smart2FA"

        try:
            import subprocess
            result = subprocess.run(
                ['qrencode', '-t', 'utf8', uri],
                capture_output=True, text=True
            )
            if result.returncode == 0 and result.stdout:
                qr_label = QLabel(result.stdout)
                qr_label.setFont(QFont("Monospace", 10))
                qr_label.setAlignment(Qt.AlignCenter)
                qr_label.setStyleSheet("background-color: white; color: black; padding: 10px;")
                layout.addWidget(qr_label)
            else:
                raise Exception("qrencode failed")
        except:
            uri_label = QLabel(
                f"<b>QR code generator not available.</b><br><br>"
                f"Manual URI:<br>"
                f"<code>{uri}</code><br><br>"
                f"Install qrencode:<br>"
                f"<i>sudo apt install qrencode</i>"
            )
            uri_label.setWordWrap(True)
            uri_label.setAlignment(Qt.AlignCenter)
            uri_label.setStyleSheet("color: #888;")
            layout.addWidget(uri_label)

        secret_group = QGroupBox("TOTP Secret Key")
        secret_layout = QVBoxLayout()

        self.secret_display = QLineEdit(secret)
        self.secret_display.setReadOnly(True)
        self.secret_display.setFont(QFont("Monospace", 10))
        self.secret_display.setStyleSheet("background-color: #2a2a2a; color: #2a82da;")
        secret_layout.addWidget(self.secret_display)

        secret_group.setLayout(secret_layout)
        layout.addWidget(secret_group)

        btn_layout = QHBoxLayout()

        copy_secret_btn = QPushButton("📋 Copy Secret Key")
        copy_secret_btn.clicked.connect(lambda: self.copy_secret(secret))

        copy_uri_btn = QPushButton("🔗 Copy URI")
        copy_uri_btn.clicked.connect(lambda: self.copy_uri(uri))

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)

        btn_layout.addWidget(copy_secret_btn)
        btn_layout.addWidget(copy_uri_btn)
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)

        self.secret = secret
        self.uri = uri

    def copy_secret(self, secret):
        clipboard = QApplication.clipboard()
        clipboard.setText(secret)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Copied")
        msg.setText("TOTP secret key copied to clipboard!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, msg.accept)

    def copy_uri(self, uri):
        clipboard = QApplication.clipboard()
        clipboard.setText(uri)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Copied")
        msg.setText("OTP URI copied to clipboard!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, msg.accept)


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
