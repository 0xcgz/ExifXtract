<div align="center">

```
███████╗██╗  ██╗██╗███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗
██╔════╝╚██╗██╔╝██║██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
█████╗   ╚███╔╝ ██║█████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║
██╔══╝   ██╔██╗ ██║██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║
███████╗██╔╝ ██╗██║██║     ██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║
╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝
```

**Image Forensics & Metadata Intelligence Framework**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Field](https://img.shields.io/badge/Field-OSINT%20%26%20Forensics-red?style=for-the-badge&logo=target&logoColor=white)](https://github.com/0xcgz/ExifXtract)
[![Version](https://img.shields.io/badge/Version-1.0.0-cyan?style=for-the-badge)](https://github.com/0xcgz/ExifXtract/releases)
[![VirusTotal](https://img.shields.io/badge/VirusTotal-5%2F71_false_positives-orange?style=for-the-badge&logo=virustotal&logoColor=white)](https://www.virustotal.com/gui/file/4bc52c2b4a4950b514f2e1d9dd086c571e5e282aa1904c95ff7061a2a3410ca3/detection)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](https://github.com/0xcgz/ExifXtract)

<br>

> A terminal-native forensic tool for extracting, analyzing, and sanitizing image metadata.
> Built for OSINT researchers, privacy advocates, and digital forensics professionals.

<br>

![ExifXtract Demo](https://github.com/user-attachments/assets/14eaba2f-517e-4854-b76d-7ce29b8ce4d2)

</div>

---

## What It Does

Every image you take or receive carries invisible data embedded inside it — the device that took it, the exact GPS coordinates, the timestamp, software used, and more. Most people never see this data. ExifXtract surfaces all of it instantly.

Whether you're tracing the origin of an image in an investigation, checking what metadata your own photos expose, or sanitizing files before sharing them — ExifXtract gives you a clean, fast, terminal-native interface to do it all in seconds.

---

## Features

| | Feature | Description |
|---|---|---|
| 🔍 | **Deep Metadata Extraction** | Parses IFD, Sub-IFD (camera settings), and GPS-IFD tags across JPG, PNG, TIFF, WEBP |
| 📍 | **Precision Geolocation** | Converts raw GPS coordinates to decimal format + generates a one-click Google Maps link |
| 🏠 | **Reverse Geocoding** | Resolves GPS coordinates into a full human-readable address (city, street, country) |
| 🔐 | **Triple Hash Verification** | Generates MD5, SHA1, and SHA256 fingerprints for threat intel and integrity checks |
| 🕵️ | **Steganography Detection** | Flags files whose size is anomalously large relative to resolution — possible hidden data |
| 🛡️ | **Privacy Shield** | Strips all EXIF metadata and outputs a clean, tracker-free copy of the image |
| 📊 | **Dual Report Export** | Saves both `.txt` (human-readable) and `.json` (machine-readable) forensic reports |
| 📁 | **Bulk Folder Scan** | Processes entire directories and consolidates results into one report |
| 🖼️ | **Thumbnail Preview** | Opens a quick image preview before scanning so you confirm the right file |
| ⚡ | **Headless CLI Mode** | Run fully without GUI: `--path`, `--dir`, `--strip` flags for scripting and automation |
| 🎨 | **Color-Coded Output** | Metadata tags color-coded by category — device, timestamps, GPS, dimensions |
| 📝 | **Session Logging** | Every operation appended to `exifxtract.log` for audit trails and replay |

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/0xcgz/ExifXtract.git
cd ExifXtract
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run it**
```bash
python ExifXtract.py
```

> **Optional:** Install `geopy` to enable reverse geocoding (resolves GPS to a real address)
> ```bash
> pip install geopy
> ```

---

## Requirements

```
Pillow>=9.0.0
rich>=13.0.0
geopy>=2.3.0        # optional — enables reverse geocoding
```

- Python `3.8+`
- Windows / macOS / Linux

---

## Usage

### Interactive Mode (default)

```bash
python ExifXtract.py
```

You'll land on the main menu:

```
[ 1 ]  Deep Analysis       —  Single file, full forensic scan
[ 2 ]  Bulk Folder Scan    —  Entire directory, batch results
[ 3 ]  Metadata Remover    —  Strip all EXIF, output clean file
[ 4 ]  Thumbnail Preview   —  Preview image, then run analysis
[ 0 ]  Exit
```

### Headless / CLI Mode

```bash
# Analyze a single image
python ExifXtract.py --path photo.jpg

# Bulk scan a directory
python ExifXtract.py --dir ./images/

# Strip all metadata from an image
python ExifXtract.py --strip photo.jpg

# Open thumbnail preview during scan
python ExifXtract.py --path photo.jpg --preview

# Show version info
python ExifXtract.py --version
```

---

## Output

Every scan generates two timestamped reports automatically:

**`.txt`** — Human-readable forensic log
```
[+] FILE   : DSCN0029.jpg
    SIZE   : 4,201.3 KB
    MD5    : 538949d6bac2091d202afc7721a83046
    SHA1   : f670f2bb6c54898894b06b083185b05086bd4e6e
    SHA256 : 941b9c7bfe35e0a3775f013e613748f55d...

    GPS COORDINATES : 43.468243, 11.880171
    GOOGLE MAPS     : https://maps.google.com/?q=43.468243,11.880171
    ADDRESS         : Via Senese, Tavarnelle Val di Pesa, Florence, Italy

    METADATA:
      Make                             NIKON
      Model                            COOLPIX P6000
      DateTime                         2008:11:01 21:15:09
```

**`.json`** — Machine-readable, ready to pipe into other tools
```json
{
  "tool": "ExifXtract",
  "version": "1.0.0",
  "author": "Ali Alaradi",
  "results": [
    {
      "file": "DSCN0029.jpg",
      "hashes": { "MD5": "...", "SHA1": "...", "SHA256": "..." },
      "gps": {
        "lat": 43.468243,
        "lon": 11.880171,
        "address": "Via Senese, Tavarnelle Val di Pesa, Florence, Italy",
        "maps": "https://maps.google.com/?q=43.468243,11.880171"
      }
    }
  ]
}
```

---

## Supported Formats

| Format | Extension | GPS Support | Full EXIF |
|--------|-----------|-------------|-----------|
| JPEG | `.jpg` `.jpeg` | ✅ | ✅ |
| PNG | `.png` | ✅ | ✅ |
| TIFF | `.tiff` | ✅ | ✅ |
| WebP | `.webp` | ✅ | ✅ |

---

## Antivirus & VirusTotal

[![VirusTotal](https://img.shields.io/badge/VirusTotal-5%2F71_false_positives-orange?style=for-the-badge&logo=virustotal&logoColor=white)](https://www.virustotal.com/gui/file/4bc52c2b4a4950b514f2e1d9dd086c571e5e282aa1904c95ff7061a2a3410ca3/detection)

`ExifXtract.exe` was scanned on VirusTotal and flagged by **5 out of 71 engines**.

**This is a known false positive — not a real threat.** Here is exactly why:

The `.exe` is compiled with **PyInstaller**, which bundles the Python interpreter and all libraries into a single executable. This packaging method is well-documented as a trigger for heuristic AV detections, regardless of what the actual code does. The flagging engines — Bkav Pro, Zillya, SecureAge, Fortinet, and Microsoft — are all known to produce high false-positive rates specifically on PyInstaller-compiled binaries.

Microsoft's `Trojan:Win32/Wacatac.B!ml` label in particular is a **machine-learning heuristic** triggered by file structure alone, not by any actual malicious behavior. It is one of the single most commonly reported false positives in the PyInstaller open-source community.

**All major engines are clean:**

| Engine | Result |
|--------|--------|
| Bitdefender | ✅ Undetected |
| Kaspersky | ✅ Undetected |
| ESET-NOD32 | ✅ Undetected |
| CrowdStrike Falcon | ✅ Undetected |
| Avast | ✅ Undetected |
| AVG | ✅ Undetected |
| Malwarebytes | ✅ Undetected |
| DrWeb | ✅ Undetected |
| Google | ✅ Undetected |
| + 57 others | ✅ Undetected |

🔗 [View the full VirusTotal scan](https://www.virustotal.com/gui/file/4bc52c2b4a4950b514f2e1d9dd086c571e5e282aa1904c95ff7061a2a3410ca3/detection)

The full source code is available in this repository — you can read every line, or run `python ExifXtract.py` directly instead of the `.exe` if you prefer.

**Verify your download hasn't been tampered with:**
```powershell
Get-FileHash ExifXtract.exe -Algorithm SHA256
```
Expected: `4bc52c2b4a4950b514f2e1d9dd086c571e5e282aa1904c95ff7061a2a3410ca3`


---

## Disclaimer

This tool is intended for **legal and ethical use only** — personal privacy auditing, authorized digital forensics, and OSINT research on images you own or have permission to analyze. The author is not responsible for any misuse.

---

<div align="center">

**Built by Ali Alaradi**

*Cybersecurity Specialist & Security Researcher*

[![GitHub](https://img.shields.io/badge/GitHub-0xcgz-181717?style=for-the-badge&logo=github)](https://github.com/0xcgz)

<br>

<sub>ExifXtract v1.0.0 · © 2026 · MIT License</sub>

</div>
