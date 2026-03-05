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
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](https://github.com/0xcgz/ExifXtract)

<br>

> A terminal-native forensic tool for extracting, analyzing, and sanitizing image metadata.  
> Built for OSINT researchers, privacy advocates, and digital forensics professionals.

<br>

![ExifXtract Demo](https://github.com/user-attachments/assets/14eaba2f-517e-4854-b76d-7ce29b8ce4d2)

</div>

---

## What It Does

Every image you take or receive carries invisible data embedded inside it — the device that took it, the exact GPS coordinates of where it was taken, the timestamp, software used, and more. Most people never see this data. ExifXtract surfaces all of it instantly.

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
| 📁 | **Bulk Folder Scan** | Recursively processes entire directories and consolidates results into one report |
| 🖼️ | **Thumbnail Preview** | Opens a quick image preview before scanning so you confirm the right file |
| ⚡ | **Headless CLI Mode** | Run fully without the GUI: `--path`, `--dir`, `--strip` flags for scripting/automation |
| 🎨 | **Color-Coded Output** | Metadata tags color-coded by category: device, timestamps, GPS, dimensions |
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
python exifxtract.py
```

> **Optional:** Install `geopy` to enable reverse geocoding (street address from GPS coordinates)
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
python exifxtract.py
```

You'll land on the main menu. Pick a module:

```
[ 1 ]  Deep Analysis       —  Single file, full forensic scan
[ 2 ]  Bulk Folder Scan    —  Entire directory, batch results
[ 3 ]  Metadata Remover    —  Strip all EXIF, output clean file
[ 4 ]  Thumbnail Preview   —  Preview image, then run analysis
[ 0 ]  Exit
```

### Headless / CLI Mode

No GUI needed. Pass flags directly for scripting or automation:

```bash
# Analyze a single image
python exifxtract.py --path photo.jpg

# Bulk scan a directory
python exifxtract.py --dir ./images/

# Strip all metadata from an image
python exifxtract.py --strip photo.jpg

# Open thumbnail preview during scan
python exifxtract.py --path photo.jpg --preview

# Show version info
python exifxtract.py --version
```

---

## Output

Every scan automatically generates two timestamped report files in the working directory:

**`Report_filename_20260305_143021.txt`** — Human-readable forensic log
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
      ...
```

**`Report_filename_20260305_143021.json`** — Machine-readable, ready to pipe into other tools
```json
{
  "tool": "ExifXtract",
  "version": "2.0.0",
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

## Session Summary

At the end of every session, ExifXtract prints a quick summary:

```
─────────────── Session Summary ───────────────
  Images scanned        12
  With GPS data         7
  Flagged (stego hint)  1
```

---

## How Steganography Detection Works

ExifXtract compares a file's actual byte size against the theoretical uncompressed size for its resolution `(width × height × 3 bytes)`. If the actual file is more than **1.5×** what it should be, it gets flagged with a warning:

```
⚠ STEGO  File is 2.3x larger than expected — possible hidden data
```

This is a heuristic, not a guarantee. Use it as a signal to investigate further.

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
