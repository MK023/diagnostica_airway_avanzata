# 🎯 Advanced Network Diagnostics Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python) ![Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows) ![Linux](https://img.shields.io/badge/OS-Linux-yellow?logo=linux) ![MacOS](https://img.shields.io/badge/OS-macOS-lightgrey?logo=apple)
![License](https://img.shields.io/badge/License-MIT-green.svg) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)
[![pre-commit checks](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![isort](https://img.shields.io/badge/imports-isort%20checked-blue.svg)](https://pycqa.github.io/isort/)
[![security](https://img.shields.io/badge/security-bandit%20%26%20pip--audit-green)](https://bandit.readthedocs.io/en/latest/)

---

## 🚀 Overview

**Advanced Network Diagnostics Tool** is a powerful Python script designed for real-time and in-depth diagnostics of your network connectivity.
It combines ping, speedtest, traceroute, ICMP, DNS, interface stats, and more—logging results automatically to CSV for further analysis.
Ideal for sysadmins, network engineers, and anyone who wants to monitor or debug network performance with automation, detail, and reliability!

---

## 🌟 Features

- **Real-time ping monitoring** with auto diagnostics on high latency
- **Speedtest integration** for download, upload, ping
- **Pingparsing** advanced statistics
- **ICMP & Traceroute** via Scapy (deep path analysis)
- **Network interface stats** with psutil
- **DNS checks** (dnspython)
- **Automatic CSV logging** for every diagnostic event
- **Cross-platform**: Windows, Linux, macOS
- **Admin/root privilege check** for full feature access
- **Clear, colorful logging** for readability
- **Security static analysis** and dependency audit (Bandit & pip-audit, CI-integrated)
- **Pre-commit hooks** for code quality (black, flake8, isort, mypy, bandit)
- **Import ordering checked** (isort)
- **YAML and INI syntax checked** (pre-commit)

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MK023/cloudsec.git
cd cloudsec
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

- **Production:**
  `pip install -r requirements.txt`
- **Development (recommended for contributors):**
  `pip install -r requirements-dev.txt`
  `pre-commit install`  # Optional: activate pre-commit hooks

#### Required Python packages

- `psutil`
- `pingparsing`
- `ping3`
- `speedtest-cli`
- `scapy`
- `dnspython`

---

## 🚦 Usage

### Run the script

```bash
python diagnostics.py
```

**Note:**
Some features (ICMP, traceroute) require **admin/root privileges**:
- On Windows: Right-click → “Run as administrator”
- On Linux/macOS: Run with `sudo`

### Interactive prompt

You'll be asked for the IP address or domain to diagnose:

```
Enter IP address or domain to ping: 8.8.8.8
```

---

## 📊 Output

- All diagnostics are **automatically logged** to `diagnostics.csv`.
- Each row includes timestamp, address, ping, speedtest, traceroute, DNS, interface stats, and more.

---

## 🎨 Example Log Output

```text
[2025-07-11 11:45:03] [INFO] Listening to ping output...
[2025-07-11 11:45:04] [SUCCESS] Advanced diagnostics written to CSV (3 row(s)).
```

---

## 🔒 Permissions

- The script will **automatically check for admin/root permissions** and exit if not sufficient.
- This is essential for raw socket operations (ICMP, traceroute).

---

## ⚡ Troubleshooting

- **Permission errors?** Run as administrator (Windows) or with `sudo` (Linux/macOS).
- **Missing modules?** Run `pip install -r requirements.txt` again in your virtualenv.
- **Scapy not working on Windows?** Install Winpcap/Npcap.
- **Pre-commit errors?** Run `pre-commit run --all-files` to check and fix code style/security issues.

---

## 📦 Project Structure

```text
├── diagnostics.py
├── requirements.txt
├── requirements-dev.txt
├── .pre-commit-config.yaml
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── SECURITY.md
│   └── CONTRIBUTING.md
├── diagnostics.csv
├── README.md
```

---

## 🛡️ Security & Quality

- **Static analysis:** Bandit (integrated in CI & pre-commit)
- **Dependency audit:** pip-audit (integrated in CI)
- **Pre-commit hooks:** black, flake8, isort, mypy, bandit
- **Import order checked:** isort
- **YAML/INI checked:** pre-commit hooks
- **Coverage:** pytest & coverage (CI, badge ready)
- **All checks auto-run in CI and before PR merges!**

---

## 💡 Customization

- Change output CSV filename in the code (`filename` parameter).
- Modular functions — add more diagnostics easily!

---

## 🤝 Contributing

Pull requests and issues are welcome!
See [`CONTRIBUTING.md`](.github/CONTRIBUTING.md) for guidelines and setup instructions.

---

## 📜 License

MIT License — see [`LICENSE`](LICENSE) for details.

---

## 🙋‍♂️ Author

Made with ❤️ by [MK023](https://github.com/MK023) and Copilot.

---

## 🔗 Links

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [Pingparsing](https://pypi.org/project/pingparsing/)
- [Speedtest CLI](https://github.com/sivel/speedtest-cli)
- [psutil](https://psutil.readthedocs.io/)
- [ping3](https://github.com/kyan001/ping3)
- [Bandit](https://bandit.readthedocs.io/en/latest/)
- [pip-audit](https://github.com/pypa/pip-audit)
- [pre-commit](https://pre-commit.com/)
- [isort](https://pycqa.github.io/isort/)

---

## 🎉 Happy Diagnosing!
