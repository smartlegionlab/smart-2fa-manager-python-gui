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
    QGroupBox,
    QGridLayout,
)


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
