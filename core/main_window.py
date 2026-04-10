# ==============================================================
# Smart 2FA Manager (Gui)
# https://github.com/smartlegionlab/smart-2fa-manager-python-gui
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
# ==============================================================
import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QLabel,
    QStatusBar,
    QAction,
    QDialog,
    QFrame,
    QDesktopWidget,
    QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from core.totp_manager import TOTPManager
from core.dialogs import (
    InitDialog,
    UnlockDialog,
    AddServiceDialog,
    GetCodeDialog,
    BackupRestoreDialog,
    AboutDialog
)
from core import __version__ as ver


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.totp_manager = TOTPManager()
        self.secrets = {}
        self.is_unlocked = False

        self.setWindowTitle(f"Smart 2FA Manager {ver}")
        self.resize(900, 500)

        self.setup_ui()
        self.center_window()

        if not self.totp_manager.check_storage_exists():
            self.show_init_dialog()
        else:
            self.show_unlock_dialog()

    def get_totp_time_remaining(self) -> int:
        current_time = int(time.time())
        return 30 - (current_time % 30)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        header_layout = QHBoxLayout()
        title = QLabel("🔐 Smart 2FA Manager")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2a82da;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.status_indicator = QLabel("🔒 Locked")
        self.status_indicator.setStyleSheet("color: #ff7d7d;")
        header_layout.addWidget(self.status_indicator)

        main_layout.addLayout(header_layout)

        self.setup_menu_bar()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Service", "Current Code", "Actions"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2a2a2a;
                gridline-color: #444;
            }
            QHeaderView::section {
                background-color: #353535;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.table)

        self.setup_table_shortcuts()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_add = QPushButton("+ Add Service")
        self.btn_add.setMinimumHeight(35)
        self.btn_add.clicked.connect(self.add_service)
        self.btn_add.setEnabled(False)

        self.btn_refresh = QPushButton("🔄 Refresh Codes")
        self.btn_refresh.setMinimumHeight(35)
        self.btn_refresh.clicked.connect(self.refresh_codes)
        self.btn_refresh.setEnabled(False)

        self.btn_lock = QPushButton("🔒  Lock (Ctrl + L)")
        self.btn_lock.setMinimumHeight(35)
        self.btn_lock.clicked.connect(self.lock_storage)
        self.btn_lock.setEnabled(True)

        self.btn_backup = QPushButton("💾 Backup")
        self.btn_backup.setMinimumHeight(35)
        self.btn_backup.clicked.connect(self.create_backup)
        self.btn_backup.setEnabled(False)

        self.btn_restore = QPushButton("📂 Restore")
        self.btn_restore.setMinimumHeight(35)
        self.btn_restore.clicked.connect(self.restore_backup)

        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_refresh)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_lock)
        button_layout.addWidget(self.btn_backup)
        button_layout.addWidget(self.btn_restore)

        main_layout.addLayout(button_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #444;")
        main_layout.addWidget(line)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.countdown_label = QLabel("")
        self.status_bar.addPermanentWidget(self.countdown_label)
        self.status_bar.showMessage("Ready")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_codes_and_countdown)

    def setup_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        lock_action = QAction("Lock", self)
        lock_action.setShortcut("Ctrl+L")
        lock_action.triggered.connect(self.lock_storage)
        file_menu.addAction(lock_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+E")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        services_menu = menubar.addMenu("Services")

        add_action = QAction("Add Service", self)
        add_action.setShortcut("Ctrl+N")
        add_action.triggered.connect(self.add_service)
        services_menu.addAction(add_action)

        refresh_action = QAction("Refresh Codes", self)
        refresh_action.setShortcut("Ctrl+R")
        refresh_action.triggered.connect(self.refresh_codes)
        services_menu.addAction(refresh_action)

        services_menu.addSeparator()

        backup_action = QAction("Create Backup", self)
        backup_action.setShortcut("Ctrl+B")
        backup_action.triggered.connect(self.create_backup)
        services_menu.addAction(backup_action)

        restore_action = QAction("Restore from Backup", self)
        restore_action.setShortcut("Ctrl+Shift+R")
        restore_action.triggered.connect(self.restore_backup)
        services_menu.addAction(restore_action)

        help_menu = menubar.addMenu("Help")

        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.setShortcut("Ctrl+/")
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

        help_menu.addSeparator()

        about_action = QAction("About", self)
        about_action.setShortcut("F1")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_shortcuts(self):
        from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QFrame

        dialog = QDialog(self)
        dialog.setWindowTitle("Smart 2FA Manager - Keyboard Shortcuts")
        dialog.setMinimumWidth(550)
        dialog.setMinimumHeight(500)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        header = QLabel("Keyboard Shortcuts")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #2a82da; padding: 10px;")
        layout.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #2a2a2a;
            }
            QScrollBar:vertical {
                background-color: #353535;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #2a82da;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(15, 15, 15, 15)

        def add_shortcut_table(title, shortcuts):
            title_label = QLabel(title)
            title_font = QFont()
            title_font.setPointSize(12)
            title_font.setBold(True)
            title_label.setFont(title_font)
            title_label.setStyleSheet("color: #2a82da; padding-top: 10px;")
            content_layout.addWidget(title_label)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("background-color: #444; max-height: 1px;")
            content_layout.addWidget(line)

            for key, desc in shortcuts:
                item_widget = QWidget()
                item_layout = QHBoxLayout(item_widget)
                item_layout.setContentsMargins(10, 5, 10, 5)
                item_layout.setSpacing(20)

                key_label = QLabel(key)
                key_label.setFont(QFont("Monospace", 11))
                key_label.setStyleSheet("""
                    color: #2a82da;
                    background-color: #353535;
                    padding: 4px 10px;
                    border-radius: 4px;
                    min-width: 120px;
                """)
                key_label.setAlignment(Qt.AlignCenter)

                desc_label = QLabel(desc)
                desc_label.setStyleSheet("color: #cccccc;")

                item_layout.addWidget(key_label)
                item_layout.addWidget(desc_label)
                item_layout.addStretch()

                content_layout.addWidget(item_widget)

        add_shortcut_table("🌐 Global Shortcuts", [
            ("Ctrl + L", "Lock Storage"),
            ("Ctrl + E", "Exit Application"),
            ("F1", "About"),
            ("Ctrl + /", "Show this help"),
        ])

        add_shortcut_table("🔧 Services Shortcuts", [
            ("Ctrl + N", "Add New Service"),
            ("Ctrl + R", "Refresh Codes"),
            ("Ctrl + B", "Create Backup"),
            ("Ctrl + Shift + R", "Restore from Backup"),
        ])

        add_shortcut_table("📋 Table Actions (when row selected)", [
            ("Ctrl + C", "Copy Code"),
            ("Ctrl + G", "Get Code Dialog"),
            ("Ctrl + Q", "Show QR Code"),
            ("Del", "Delete Service"),
        ])

        note_label = QLabel("💡 Tip: Select a service row in the table to use Table Actions shortcuts")
        note_label.setStyleSheet("color: #ff9800; padding: 10px; margin-top: 10px;")
        note_label.setWordWrap(True)
        content_layout.addWidget(note_label)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

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
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)

        dialog.setStyleSheet("""
            QDialog {
                background-color: #2a2a2a;
            }
            QLabel {
                color: #ffffff;
            }
        """)

        dialog.exec_()

    def center_window(self):
        frame = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    def show_init_dialog(self):
        dialog = InitDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_password()
            self.totp_manager.set_password(password)
            if self.totp_manager.save_secrets({}):
                QMessageBox.information(self, "Success", "Storage created successfully!")
                self.show_unlock_dialog()
            else:
                QMessageBox.critical(self, "Error", "Failed to create storage!")
                sys.exit(1)
        else:
            sys.exit(0)

    def show_unlock_dialog(self):
        dialog = UnlockDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_password()
            self.totp_manager.set_password(password)
            self.secrets = self.totp_manager.load_secrets()

            if self.secrets is not None:
                self.is_unlocked = True
                self.status_indicator.setText("🔓 Unlocked")
                self.status_indicator.setStyleSheet("color: #2e7d32;")
                self.btn_add.setEnabled(True)
                self.btn_refresh.setEnabled(True)
                self.btn_backup.setEnabled(True)
                self.build_table()
                self.timer.start(1000)
                self.status_bar.showMessage(f"Loaded {len(self.secrets)} services", 3000)
            else:
                self.timer.stop()
                self.is_unlocked = False
                self.secrets = {}
                self.table.setRowCount(0)
                self.countdown_label.setText("")
                QMessageBox.critical(self, "Error", "Wrong password or corrupted storage!")
                self.show_unlock_dialog()
        else:
            sys.exit(0)

    def lock_storage(self):
        self.is_unlocked = False
        self.secrets = {}
        self.status_indicator.setText("🔒 Locked")
        self.status_indicator.setStyleSheet("color: #ff7d7d;")
        self.btn_add.setEnabled(False)
        self.btn_refresh.setEnabled(False)
        self.btn_backup.setEnabled(False)
        self.table.setRowCount(0)
        self.timer.stop()
        self.countdown_label.setText("")
        self.status_bar.showMessage("Locked", 2000)
        self.show_unlock_dialog()

    def build_table(self):
        self.table.setRowCount(0)

        for service, secret in sorted(self.secrets.items()):
            row = self.table.rowCount()
            self.table.insertRow(row)

            service_item = QTableWidgetItem(service)
            self.table.setItem(row, 0, service_item)

            code = self.totp_manager.generate_totp(secret)
            code_item = QTableWidgetItem(code if code else "ERROR")
            code_item.setTextAlignment(Qt.AlignCenter)
            code_item.setFont(QFont("Monospace", 11))
            if not code:
                code_item.setForeground(Qt.red)
            self.table.setItem(row, 1, code_item)

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)

            copy_btn = QPushButton("📋 Copy")
            copy_btn.setMaximumWidth(70)
            copy_btn.clicked.connect(lambda checked, svc=service, c=code: self.copy_code(svc, c))

            get_btn = QPushButton("🔑 Get")
            get_btn.setMaximumWidth(60)
            get_btn.clicked.connect(lambda checked, svc=service: self.show_code_dialog(svc))

            qr_btn = QPushButton("📱 QR")
            qr_btn.setMaximumWidth(60)
            qr_btn.setStyleSheet("background-color: #ff9800;")
            qr_btn.clicked.connect(lambda checked, svc=service, sec=secret: self.show_qr_dialog(svc, sec))

            del_btn = QPushButton("🗑 Delete")
            del_btn.setMaximumWidth(70)
            del_btn.setStyleSheet("background-color: #da2a2a;")
            del_btn.clicked.connect(lambda checked, svc=service: self.delete_service(svc))

            actions_layout.addWidget(copy_btn)
            actions_layout.addWidget(get_btn)
            actions_layout.addWidget(qr_btn)
            actions_layout.addWidget(del_btn)

            self.table.setCellWidget(row, 2, actions_widget)

    def setup_table_shortcuts(self):
        copy_shortcut = QAction(self)
        copy_shortcut.setShortcut("Ctrl+C")
        copy_shortcut.triggered.connect(self.copy_selected_code)
        self.addAction(copy_shortcut)

        get_shortcut = QAction(self)
        get_shortcut.setShortcut("Ctrl+G")
        get_shortcut.triggered.connect(self.get_selected_code)
        self.addAction(get_shortcut)

        qr_shortcut = QAction(self)
        qr_shortcut.setShortcut("Ctrl+Q")
        qr_shortcut.triggered.connect(self.qr_selected_code)
        self.addAction(qr_shortcut)

        delete_shortcut = QAction(self)
        delete_shortcut.setShortcut(Qt.Key_Delete)
        delete_shortcut.triggered.connect(self.delete_selected_service)
        self.addAction(delete_shortcut)

    def get_selected_service(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            service_item = self.table.item(current_row, 0)
            if service_item:
                return service_item.text()
        return None

    def copy_selected_code(self):
        service = self.get_selected_service()
        if service and service in self.secrets:
            code = self.totp_manager.generate_totp(self.secrets[service])
            if code:
                self.copy_code(service, code)

    def get_selected_code(self):
        service = self.get_selected_service()
        if service:
            self.show_code_dialog(service)

    def qr_selected_code(self):
        service = self.get_selected_service()
        if service and service in self.secrets:
            self.show_qr_dialog(service, self.secrets[service])

    def delete_selected_service(self):
        service = self.get_selected_service()
        if service:
            self.delete_service(service)

    def show_qr_dialog(self, service: str, secret: str):
        if not self.is_unlocked:
            return

        from core.dialogs import QRCodeDialog
        dialog = QRCodeDialog(self, service, secret)
        dialog.exec_()

    def update_codes_and_countdown(self):
        if not self.is_unlocked:
            return

        remaining = self.get_totp_time_remaining()
        if remaining <= 3:
            self.countdown_label.setText(f"⚠️ Code expires in: {remaining}s")
            self.countdown_label.setStyleSheet("color: #ff7d7d; padding-right: 10px;")
        elif remaining <= 10:
            self.countdown_label.setText(f"Code expires in: {remaining}s")
            self.countdown_label.setStyleSheet("color: #ff9800; padding-right: 10px;")
        else:
            self.countdown_label.setText(f"Code expires in: {remaining}s")
            self.countdown_label.setStyleSheet("color: #888; padding-right: 10px;")

        for row in range(self.table.rowCount()):
            service_item = self.table.item(row, 0)
            if service_item:
                service = service_item.text()
                secret = self.secrets.get(service)
                if secret:
                    code = self.totp_manager.generate_totp(secret)
                    if code:
                        self.table.item(row, 1).setText(code)

    def refresh_codes(self):
        self.update_codes_and_countdown()
        self.status_bar.showMessage("Codes refreshed", 1000)

    def add_service(self):
        if not self.is_unlocked:
            return

        dialog = AddServiceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            service, secret = dialog.get_values()

            if service in self.secrets:
                reply = QMessageBox.question(
                    self, "Confirm",
                    f"Service '{service}' already exists. Overwrite?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply != QMessageBox.Yes:
                    return

            self.secrets[service] = secret
            if self.totp_manager.save_secrets(self.secrets):
                self.build_table()
                self.status_bar.showMessage(f"Service '{service}' added", 3000)
            else:
                QMessageBox.critical(self, "Error", "Failed to save secrets!")

    def copy_code(self, service: str, code: str):
        if code and code != "ERROR":
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            self.status_bar.showMessage(f"Code for '{service}' copied to clipboard", 2000)

    def show_code_dialog(self, service: str):
        if not self.is_unlocked:
            return

        secret = self.secrets.get(service)
        if secret:
            code = self.totp_manager.generate_totp(secret)
            if code:
                dialog = GetCodeDialog(self, service, code)
                dialog.exec_()
            else:
                QMessageBox.critical(self, "Error", "Failed to generate code!")

    def delete_service(self, service: str):
        if not self.is_unlocked:
            return

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete service '{service}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            del self.secrets[service]
            if self.totp_manager.save_secrets(self.secrets):
                self.build_table()
                self.status_bar.showMessage(f"Service '{service}' deleted", 3000)
            else:
                QMessageBox.critical(self, "Error", "Failed to delete service!")

    def create_backup(self):
        if not self.is_unlocked:
            return

        backup_file = self.totp_manager.create_backup()
        if backup_file:
            QMessageBox.information(
                self, "Backup Created",
                f"Backup saved to:\n{backup_file}"
            )
            self.status_bar.showMessage("Backup created", 3000)
        else:
            QMessageBox.critical(self, "Error", "Failed to create backup!")

    def restore_backup(self):
        if self.is_unlocked:
            self.lock_storage()

        dialog = BackupRestoreDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            backup_file, new_password = dialog.get_values()
            if backup_file and new_password:
                if self.totp_manager.restore_from_backup(Path(backup_file), new_password):
                    QMessageBox.information(self, "Success", "Restore completed! Please unlock with new password.")
                    self.show_unlock_dialog()
                else:
                    QMessageBox.critical(self, "Error", "Restore failed! Check backup file and password.")

    def show_about(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def closeEvent(self, event):
        if self.is_unlocked:
            reply = QMessageBox.question(
                self, "Exit",
                "Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.timer.stop()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
