# Smart 2FA Manager (GUI) <sup>v1.0.2</sup>

---

**Offline, independent TOTP 2FA manager for Linux with graphical interface.**

---

[![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/smart-2fa-manager-python-gui)](https://github.com/smartlegionlab/smart-2fa-manager-python-gui)
[![GitHub license](https://img.shields.io/github/license/smartlegionlab/smart-2fa-manager-python-gui)](https://github.com/smartlegionlab/smart-2fa-manager-python-gui/blob/master/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/smartlegionlab/smart-2fa-manager-python-gui)](https://github.com/smartlegionlab/smart-2fa-manager-python-gui/)
[![GitHub stars](https://img.shields.io/github/stars/smartlegionlab/smart-2fa-manager-python-gui?style=social)](https://github.com/smartlegionlab/smart-2fa-manager-python-gui/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/smartlegionlab/smart-2fa-manager-python-gui?style=social)](https://github.com/smartlegionlab/smart-2fa-manager-python-gui/network/members)

---

No cloud, no phone required. Store your secrets locally, generate codes, create encrypted backups, and sync with Google Authenticator via QR codes.

---

## ⚠️ Disclaimer

**By using this software, you agree to the full disclaimer terms.**

**Summary:** Software provided "AS IS" without warranty. You assume all risks.

**Full legal disclaimer:** See [DISCLAIMER.md](DISCLAIMER.md)

---

## Interface

![Main Interface](https://github.com/smartlegionlab/smart-2fa-manager-python-gui/raw/master/data/images/logo.png)

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

1. Clone repository:
   ```bash
   git clone https://github.com/smartlegionlab/smart-2fa-manager-python-gui.git
   cd smart-2fa-manager-python-gui
   ```

2. Run:
   ```bash
   python main.py
   ```

3. Create desktop launcher (optional):
   
   Create file `~/Desktop/smart-2fa.sh`:
   ```bash
   #!/bin/bash
   cd ~/smart-2fa-manager-python-gui
   python main.py
   ```
   
   Make it executable:
   ```bash
   chmod +x ~/Desktop/smart-2fa.sh
   ```
   
   Now double-click the script on your desktop to run the application.

---

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

### Table Actions

| Button | Description |
|--------|-------------|
| `📋 Copy` | Copy TOTP code to clipboard |
| `🔑 Get` | Show TOTP code in dialog |
| `📱 QR` | Show QR code for phone import |
| `🗑 Delete` | Delete service |

---

## Keyboard Shortcuts

### Global Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + L` | Lock storage |
| `Ctrl + E` | Exit application |
| `F1` | Show About dialog |
| `Ctrl + /` | Show Keyboard Shortcuts |

### Services Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + N` | Add new service |
| `Ctrl + R` | Refresh all codes |
| `Ctrl + B` | Create backup |
| `Ctrl + Shift + R` | Restore from backup |

### Table Actions (when row selected)

| Shortcut | Action |
|----------|--------|
| `Ctrl + C` | Copy code to clipboard |
| `Ctrl + G` | Show code in dialog |
| `Ctrl + Q` | Show QR code dialog |
| `Del` | Delete service |

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
- Lock storage when leaving your computer (`Ctrl + L`)
- Keep backups in a safe place (encrypted USB drive, offline storage)

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
- **Repository:** [smartlegionlab/smart-2fa-manager-python-gui](https://github.com/smartlegionlab/smart-2fa-manager-python-gui)
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

BSD 3-Clause License - Copyright (c) 2026, [Alexander Suvorov](https://github.com/smartlegionlab)