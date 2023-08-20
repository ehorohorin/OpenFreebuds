
![Icon](docs/logo.png) OpenFreebuds Desktop
=====================

![Last release](https://img.shields.io/github/v/release/melianmiko/openfreebuds)
![AUR last modified](https://img.shields.io/aur/last-modified/openfreebuds)
[![Crowdin](https://badges.crowdin.net/openfreebuds/localized.svg)](https://crowdin.com/project/openfreebuds)

Desktop application to manage your HUAWEI FreeBuds device.
Written in Python, available for Windows and Linux.

- [💿 **Download binaries**](https://mmk.pw/en/openfreebuds/)
- [🌍 Translate to your language](https://crowdin.com/project/openfreebuds)

Features:
- Toggle noise cancellation mode directly from PC
- Change device settings (like touch reactions)
- Hotkeys, web-server included
- Open source and free forever

Supported devices:
- HUAWEI FreeBuds 5i
- HUAWEI FreeBuds 4i
- HUAWEI FreeLace Pro
- HONOR Earbuds 2 Lite

Partially supported devices (some features are missing):
- HUAWEI FreeBuds 5i
- HUAWEI FreeBuds Pro 2 

Installation
-------------

**Windows**: 
get binary packages [here](https://mmk.pw/en/openfreebuds).

**Arch Linux**: 
[available in AUR](https://aur.archlinux.org/packages/openfreebuds)

**Debian, Ubuntu 22.04-23.04**:
```shell
curl -Sl https://deb.mmk.pw/setup | sudo bash -
sudo apt install openfreebuds
```

Build from source code
---------

### Windows

Requirements:
- Windows 10/11, with Microsoft-compatible Bluetooth adapter
- [Python 3.10-3.11](https://www.python.org/downloads/) (NOT from Microsoft Store, don't forgot to set 
  "Add to PATH" checkbox doing installation)
- [NSIS](https://nsis.sourceforge.io/Download) (optional, for installer)
- [UPX Packager](https://upx.github.io/) (optional)

Grab sources from here, if you don't. Open PowerShell or Windows 
Terminal in this directory. Create venv and install python packages:

```shell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Now, run pyinstaller to build an executable:
```shell
pyinstaller .\openfreebuds.spec
```

Optional, make an installer package:
```shell
& 'C:\Program Files (x86)\NSIS\Bin\makensis.exe' .\openfreebuds.nsi
```

Result files will appear in `dist` directory.

### Linux

Install dependencies:
Python3, Pip3, Python3 GObject bindings (`gi`), Python3 Tkinter, Python3 DBus,
Python3 Pillow with ImageTk, Appindicator3 or AyatanaAppindicator3, 
Bluez sources (libbluetooth-dev), UPX (optional), Gtk3, Git, gcc, make

For Debian/Ubuntu:
```bash
sudo apt install make git gcc upx-ucl python3 python3-pip python3-wheel \
  python3-gi python3-tk python3-dbus python3-pil python3-pil.imagetk \
  gir1.2-appindicator3-0.1 | gir1.2-ayatanaappindicator3-0.1 \
  libgtk-3-0 libbluetooth-dev
```

### Run from source code
`python3-venv` and `build-essentials` are required, also as big part of libraries listed above.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/ofb_launcher.py
```

### Install
Grab sources and run `make`:
```bash
git clone https://github.com/melianmiko/OpenFreebuds
cd OpenFreebuds
make
sudo make install # Install
```

### Build debian package
```bash
dpkg-buildpackage -b # binary pkg
dpkg-buildpackage -S # source pkg
```

That's all.
