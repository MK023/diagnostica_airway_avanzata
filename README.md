# 🎯 Advanced Network Diagnostics Tool

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python) ![Windows](https://img.shields.io/badge/OS-Windows-blue?logo=windows) ![Linux](https://img.shields.io/badge/OS-Linux-yellow?logo=linux) ![MacOS](https://img.shields.io/badge/OS-macOS-lightgrey?logo=apple)  
![License](https://img.shields.io/badge/License-MIT-green.svg) ![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)  

---

## 🚀 Overview

**Advanced Network Diagnostics Tool** is a powerful Python script designed to provide real-time and in-depth diagnostics of your network connectivity. It combines multiple methods—ping, speedtest, traceroute, ICMP, and more—logging results automatically to a CSV for further analysis.  
Ideal for sysadmins, network engineers, and anyone who wants to monitor or debug network performance with automation, detail, and reliability!

---

## 🌟 Features

- **Real-time ping monitoring** with automatic diagnostics on high latency
- **Speedtest integration** for download, upload, and ping measurement
- **Pingparsing** advanced statistics
- **ICMP & Traceroute** via Scapy (for deep network path analysis)
- **Network interface stats** with psutil
- **Automatic CSV logging** for every diagnostic event
- **Cross-platform**: works on Windows, Linux, and macOS
- **Admin/root privilege check** for full feature access
- **Clear, colorful logging** for readability

---

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/advanced-network-diagnostics.git
cd advanced-network-diagnostics
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### Required Python packages

- `psutil`
- `pingparsing`
- `ping3`
- `speedtest-cli`
- `scapy`

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
- Each row includes timestamp, address, ping, speedtest, traceroute, interface stats, and more.

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

---

## 📦 Project Structure

```text
├── diagnostics.py        # Main script
├── requirements.txt      # Python dependencies
├── diagnostics.csv       # Output file (created automatically)
├── README.md             # This file!
```

---

## 💡 Customization

- You can change the output CSV filename by editing the `filename` parameter in `advanced_diagnostics`.
- Want to add more diagnostic methods? Modular functions make it easy!

---

## 🤝 Contributing

Pull requests and issues are welcome!  
Feel free to fork, star, and suggest improvements.

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

---

## 🎉 Happy Diagnosing!