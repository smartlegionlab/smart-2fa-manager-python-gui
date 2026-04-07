# Smart 2FA Manager (GUI) <sup>v1.0.0</sup>

**Lightweight, offline, independent TOTP 2FA manager for Linux with graphical interface.**

No cloud, no phone required. Store your secrets locally, generate codes, create encrypted backups, and sync with Google Authenticator via QR codes.

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](DISCLAIMER.md)

---

## Installation

### Dependencies

```bash
# Arch Linux
sudo pacman -S python-pyqt5 oath-toolkit gnupg qrencode

# Debian/Ubuntu
sudo apt install python3-pyqt5 oathtool gpg qrencode

# Fedora/RHEL
sudo dnf install python3-pyqt5 oathtool gnupg2 qrencode
```

### Setup

1. Get the script from repository:
   ```bash
   cd ~
   git clone https://github.com/smartlegionlab/smart-2fa-manager-gui.git
   cd smart-2fa-manager-gui
   ```

2. Run:
   ```bash
   python3 main.py
   ```

3. Create desktop shortcut (optional):
   ```bash
   chmod +x main.py
   sudo cp main.py /usr/local/bin/2fa-gui
   # Now you can use: 2fa-gui
   ```

---

## Quick Start

```bash
# Run the application
python3 main.py

# Or if installed
2fa-gui
```

Then in the GUI:

1. Initialize storage (create master password)
2. Click "+ Add Service" to add a new service
3. Enter service name (e.g., "github") and TOTP secret
4. Click "Get" to see current code
5. Click "QR" to scan with phone
6. Use "Backup" to create encrypted backups

---

## Commands (GUI)

| Button | Description |
|--------|-------------|
| `+ Add Service` | Add a new TOTP service |
| `🔄 Refresh Codes` | Manually refresh all codes |
| `💾 Backup` | Create encrypted backup with timestamp |
| `📂 Restore` | Restore from encrypted backup |
| `Lock` (Ctrl+L) | Lock storage |
| `Exit` (Ctrl+Q) | Exit application |

### Table Actions

| Button | Description |
|--------|-------------|
| `📋 Copy` | Copy TOTP code to clipboard |
| `🔑 Get` | Show TOTP code in dialog |
| `📱 QR` | Show QR code for phone import |
| `🗑 Delete` | Delete service |

---

## File Structure

```
~/.2fa/
├── secrets.gpg          # Encrypted master storage
└── backups/
    └── secrets.2026-04-06_14-30-00.gpg
```

**Compatible with bash and Python CLI versions!**

---

## How It Works

- **Secrets are stored locally** in `~/.2fa/secrets.gpg` (AES-256 encrypted with GPG)
- **No internet connection required** - codes generated locally using `oathtool`
- **Backups are encrypted** with the same password
- **QR codes** let you import secrets into Google Authenticator / Aegis
- **Lost your phone?** Just re-scan QR codes from your Linux machine

---

## Security Notes

- Your GPG password is never stored
- Backup files are encrypted with the same password
- Lock storage when leaving your computer (Ctrl+L)
- Keep backups in a safe place (encrypted USB drive, offline storage)

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Lock storage |
| `Ctrl+Q` | Exit application |
| `F1` | About dialog |

---

## Migration from CLI Version

Your existing `~/.2fa/secrets.gpg` works **out of the box** with the GUI version!

```bash
# Just run GUI - it will detect existing storage
python main.py
# Enter your existing password
```

---

## Author & Repository

- **Author:** [@smartlegionlab](https://github.com/smartlegionlab/)
- **Repository:** [smartlegionlab/smart-2fa-manager-gui](https://github.com/smartlegionlab/smart-2fa-manager-gui)
- **Bash version:** [smart-2fa-manager-bash](https://github.com/smartlegionlab/smart-2fa-manager-bash)
- **Python CLI:** [smart-2fa-manager-python-cli](https://github.com/smartlegionlab/smart-2fa-manager-python-cli)
- **License:** [BSD 3-Clause](LICENSE)

---

## Requirements

- Python 3.6+
- PyQt5
- GPG (GNU Privacy Guard)
- oathtool (OATH Toolkit)
- qrencode (optional, for QR codes)

---

## License

BSD 3-Clause License - Copyright (c) 2026, Alexander Suvorov