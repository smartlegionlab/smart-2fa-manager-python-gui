# ============================================================
# Smart 2FA Manager (Gui)
# https://github.com/smartlegionlab/smart-2fa-manager-gui
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# License: BSD 3-Clause
# ============================================================
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

CONFIG_DIR = Path.home() / ".2fa"
SECRETS_ENC = CONFIG_DIR / "secrets.gpg"
BACKUP_DIR = CONFIG_DIR / "backups"
VERSION = "v1.0.0"


class TOTPManager:

    def __init__(self):
        CONFIG_DIR.mkdir(exist_ok=True)
        BACKUP_DIR.mkdir(exist_ok=True)
        self._password = None

    def set_password(self, password: str):
        self._password = password

    def _decrypt_store(self) -> Optional[str]:
        if not SECRETS_ENC.exists():
            return None

        try:
            result = subprocess.run(
                ['gpg', '--batch', '--yes', '--passphrase', self._password,
                 '--decrypt', str(SECRETS_ENC)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                return None
            return result.stdout
        except Exception:
            return None

    def _encrypt_store(self, content: str) -> bool:
        tmp_file = CONFIG_DIR / "secrets.tmp"
        try:
            tmp_file.write_text(content)
            result = subprocess.run(
                ['gpg', '--batch', '--yes', '--passphrase', self._password,
                 '--symmetric', '--cipher-algo', 'AES256',
                 '--output', str(SECRETS_ENC), str(tmp_file)],
                capture_output=True
            )
            tmp_file.unlink(missing_ok=True)
            return result.returncode == 0
        except Exception:
            tmp_file.unlink(missing_ok=True)
            return False

    def load_secrets(self) -> Optional[Dict[str, str]]:
        content = self._decrypt_store()
        if content is None:
            return None

        secrets = {}
        for line in content.strip().split('\n'):
            if ':' in line:
                service, secret = line.split(':', 1)
                secrets[service.strip()] = secret.strip()
        return secrets

    def save_secrets(self, secrets: Dict[str, str]) -> bool:
        content = '\n'.join([f"{k}:{v}" for k, v in sorted(secrets.items())])
        if content:
            content += '\n'
        return self._encrypt_store(content)

    def generate_totp(self, secret: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ['oathtool', '--totp', '-b', secret],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except FileNotFoundError:
            return None

    def check_storage_exists(self) -> bool:
        return SECRETS_ENC.exists()

    def create_backup(self) -> Optional[Path]:
        content = self._decrypt_store()
        if content is None:
            return None

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file = BACKUP_DIR / f"secrets.{timestamp}.gpg"

        try:
            result = subprocess.run(
                ['gpg', '--batch', '--yes', '--passphrase', self._password,
                 '--symmetric', '--cipher-algo', 'AES256',
                 '--output', str(backup_file)],
                input=content, text=True, capture_output=True
            )
            if result.returncode == 0:
                return backup_file
            return None
        except Exception:
            return None

    def restore_from_backup(self, backup_file: Path, new_password: str) -> bool:
        if not backup_file.exists():
            return False

        try:
            result = subprocess.run(
                ['gpg', '--batch', '--yes', '--decrypt', str(backup_file)],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                return False

            content = result.stdout
            if ':' not in content:
                return False

            self._password = new_password
            return self._encrypt_store(content)
        except Exception:
            return False
