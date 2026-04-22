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
    QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


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
