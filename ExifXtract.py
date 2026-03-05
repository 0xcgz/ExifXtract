"""
ExifXtract Framework
Author  : Ali Alaradi
Version : 1.0.0
Build   : 2026-03-05
Contact : github.com/0xcgz
"""

import argparse
import hashlib
import json
import logging
import os
import sys
import tkinter as tk
import warnings
from datetime import datetime
from tkinter import filedialog

warnings.filterwarnings("ignore", category=DeprecationWarning)

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.prompt import Prompt
from rich.rule import Rule
from rich.table import Table

# ──────────────────────────────────────────────
#  Constants
# ──────────────────────────────────────────────
VERSION       = "1.0.0"
BUILD_DATE    = "2026-03-05"
AUTHOR        = "Ali Alaradi"
GITHUB        = "github.com/0xcgz"
SUPPORTED_EXT = (".jpg", ".jpeg", ".png", ".webp", ".tiff")

# If actual file size > (w * h * 3 * threshold) flag as suspicious
STEGO_THRESHOLD = 1.5


#  Logging  (appends to exifxtract.log)

logging.basicConfig(
    filename="exifxtract.log",
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("exifxtract")

console = Console()


#  Session counters

SESSION = {"scanned": 0, "with_gps": 0, "flagged": 0}



#  UI helpers

def clear_screen():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass


_BANNER_PRINTED = False


def print_banner(force=False):
    global _BANNER_PRINTED
    if _BANNER_PRINTED and not force:
        return
    _BANNER_PRINTED = True

    art = r"""
███████╗██╗  ██╗██╗███████╗██╗  ██╗████████╗██████╗  █████╗  ██████╗████████╗
██╔════╝╚██╗██╔╝██║██╔════╝╚██╗██╔╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝
█████╗   ╚███╔╝ ██║█████╗   ╚███╔╝    ██║   ██████╔╝███████║██║        ██║
██╔══╝   ██╔██╗ ██║██╔══╝   ██╔██╗    ██║   ██╔══██╗██╔══██║██║        ██║
███████╗██╔╝ ██╗██║██║     ██╔╝ ██╗   ██║   ██║  ██║██║  ██║╚██████╗   ██║
╚══════╝╚═╝  ╚═╝╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝"""

    subtitle = (
        f"[bold cyan]ExifXtract Framework[/bold cyan]  "
        f"[dim]v{VERSION}  ·  {BUILD_DATE}[/dim]\n"
        f"[dim]Developed by {AUTHOR}  ·  {GITHUB}[/dim]"
    )
    panel = Panel(
        Align.center(f"[bold white]{art}[/bold white]\n\n{subtitle}"),
        border_style="cyan",
        box=box.SIMPLE,
        expand=False,
    )
    console.print(Align.center(panel))


def print_version():
    console.print(
        f"\n[bold cyan]ExifXtract[/bold cyan]  v{VERSION}  ·  {BUILD_DATE}\n"
        f"[dim]Author : {AUTHOR}\n"
        f"Contact: {GITHUB}[/dim]\n"
    )


def print_summary():
    t = Table(show_header=False, box=box.SIMPLE, border_style="cyan")
    t.add_column("", style="dim", width=22)
    t.add_column("", style="bold white")
    t.add_row("Images scanned",      str(SESSION["scanned"]))
    t.add_row("With GPS data",       f"[green]{SESSION['with_gps']}[/green]")
    t.add_row("Flagged (stego hint)", f"[red]{SESSION['flagged']}[/red]")
    console.print(Rule("[bold cyan]Session Summary[/bold cyan]"))
    console.print(Align.center(t))


#  File dialog

def open_file_browser(mode="file"):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        if mode == "dir":
            path = filedialog.askdirectory(title="Select Directory for Bulk Scan")
        else:
            path = filedialog.askopenfilename(
                title="Select Target Image",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *.tiff *.webp")],
            )
    except Exception as e:
        log.error(f"File dialog error: {e}")
        console.print(f"[red]File dialog error: {e}[/red]")
        path = ""
    finally:
        root.destroy()
    return path



#  Hashing  (MD5 + SHA1 + SHA256)

def get_hashes(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        hashes = {
            "MD5":    hashlib.md5(data).hexdigest(),
            "SHA1":   hashlib.sha1(data).hexdigest(),
            "SHA256": hashlib.sha256(data).hexdigest(),
        }
        log.info(f"Hashed {os.path.basename(filepath)} ({len(data)} bytes)")
        return hashes, len(data)
    except Exception as e:
        log.error(f"Hashing failed for {filepath}: {e}")
        console.print(f"[red]Hashing error: {e}[/red]")
        return {"MD5": "N/A", "SHA1": "N/A", "SHA256": "N/A"}, 0


#  GPS helpers

def _to_float(v):
    """Handle IFDRational, plain float/int, or (num, den) tuple."""
    if isinstance(v, tuple):
        return float(v[0]) / float(v[1]) if v[1] != 0 else 0.0
    return float(v)


def _convert_to_degrees(value):
    try:
        return _to_float(value[0]) + _to_float(value[1]) / 60.0 + _to_float(value[2]) / 3600.0
    except Exception:
        return None


def _extract_gps_ifd(exif):
    gps = {}
    try:
        gps_raw = exif.get_ifd(34853)
        for tag, val in gps_raw.items():
            gps[GPSTAGS.get(tag, tag)] = val
    except Exception as e:
        log.debug(f"GPS IFD read: {e}")
    return gps


def _parse_lat_lon(gps_dict):
    try:
        lat_raw = gps_dict.get("GPSLatitude")
        lat_ref = gps_dict.get("GPSLatitudeRef")
        lon_raw = gps_dict.get("GPSLongitude")
        lon_ref = gps_dict.get("GPSLongitudeRef")
        if not (lat_raw and lat_ref and lon_raw and lon_ref):
            return None, None
        lat = _convert_to_degrees(lat_raw)
        lon = _convert_to_degrees(lon_raw)
        if lat is None or lon is None:
            return None, None
        if lat_ref != "N":
            lat = -lat
        if lon_ref != "E":
            lon = -lon
        return lat, lon
    except Exception as e:
        log.warning(f"Lat/Lon parse failed: {e}")
        return None, None


#  Reverse geocoding  (Nominatim — no API key)

def reverse_geocode(lat, lon):
    try:
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent=f"exifxtract/{VERSION}")
        location = geolocator.reverse((lat, lon), language="en", timeout=6)
        return location.address if location else None
    except ImportError:
        log.debug("geopy not installed — reverse geocoding skipped")
        return None
    except Exception as e:
        log.warning(f"Reverse geocode failed: {e}")
        return None


# ══════════════════════════════════════════════
#  Steganography size check
# ══════════════════════════════════════════════

def stego_check(filepath, width, height, file_bytes):
    try:
        expected = width * height * 3
        if expected > 0 and file_bytes > expected * STEGO_THRESHOLD:
            ratio = round(file_bytes / expected, 2)
            log.warning(f"Stego hint on {os.path.basename(filepath)}: ratio={ratio}")
            return True, ratio
    except Exception:
        pass
    return False, None


#  Thumbnail preview


def show_thumbnail(filepath):
    try:
        img = Image.open(filepath)
        img.thumbnail((320, 320))
        img.show()
        log.info(f"Thumbnail shown: {os.path.basename(filepath)}")
    except Exception as e:
        log.warning(f"Thumbnail failed: {e}")
        console.print(f"[dim]  Thumbnail unavailable: {e}[/dim]")



#  Core EXIF extraction


def extract_data(filepath):
    metadata, gps = {}, {}
    try:
        img = Image.open(filepath)
        metadata.update({
            "Width":  img.width,
            "Height": img.height,
            "Format": img.format,
            "Mode":   img.mode,
        })

        exif = img.getexif()
        if exif:
            for tag, val in exif.items():
                name = TAGS.get(tag, tag)
                if not isinstance(val, bytes):
                    metadata[name] = val

            if hasattr(exif, "get_ifd"):
                # SubExif IFD
                try:
                    sub = exif.get_ifd(34665)
                    for tag, val in sub.items():
                        name = TAGS.get(tag, tag)
                        if not isinstance(val, bytes):
                            if isinstance(val, tuple) and len(val) == 2 and val[1] not in (0, None):
                                val = f"{val[0]}/{val[1]}"
                            metadata[name] = str(val)
                except Exception as e:
                    log.debug(f"SubExif: {e}")

                gps = _extract_gps_ifd(exif)

        img.close()

        lat, lon = _parse_lat_lon(gps) if gps else (None, None)
        if lat is not None:
            metadata["GeoLatitude"]  = lat
            metadata["GeoLongitude"] = lon

        log.info(f"Extracted {len(metadata)} tags from {os.path.basename(filepath)}, GPS={'yes' if lat else 'no'}")
        return metadata, gps, lat, lon

    except Exception as e:
        log.error(f"extract_data failed for {filepath}: {e}")
        console.print(f"[red]  Extraction error: {e}[/red]")
        return metadata, {}, None, None



#  Metadata removal


def remove_metadata(filepath):
    try:
        img   = Image.open(filepath)
        # Rebuild image pixel-by-pixel without any EXIF — compatible with all Pillow versions
        clean = Image.new(img.mode, img.size)
        clean.putdata(list(img.getdata()) if not hasattr(img, 'get_flattened_data') else img.get_flattened_data())
        ts  = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = os.path.join(
            os.path.dirname(filepath),
            f"CLEANED_{ts}_{os.path.basename(filepath)}"
        )
        clean.save(out)
        img.close()
        clean.close()
        log.info(f"Stripped: {out}")
        return out
    except Exception as e:
        log.error(f"remove_metadata failed: {e}")
        console.print(f"[red]  Error stripping metadata: {e}[/red]")
        return None



#  Report writers


_HEADER = (
    "######################################################################\n"
    f"#  ExifXtract Forensic Intelligence Report                          #\n"
    f"#  Developed by {AUTHOR:<51}#\n"
    f"#  {GITHUB:<68}#\n"
    f"#  Version : {VERSION:<59}#\n"
    "######################################################################\n"
)


def save_txt_report(results, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(_HEADER)
            f.write(f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Files     : {len(results)}\n")

            for r in results:
                f.write(f"\n{'='*70}\n")
                f.write(f"[+] FILE   : {r['name']}\n")
                f.write(f"    SIZE   : {r['size']} KB\n")
                for algo in ("MD5", "SHA1", "SHA256"):
                    f.write(f"    {algo:<6} : {r['hashes'].get(algo, 'N/A')}\n")

                if r.get("stego_flagged"):
                    f.write(f"    ** STEGO HINT : ratio {r['stego_ratio']}x — file unusually large **\n")

                lat, lon = r.get("lat"), r.get("lon")
                if lat is not None and lon is not None:
                    f.write(f"\n    GPS COORDINATES : {lat:.6f}, {lon:.6f}\n")
                    f.write(f"    GOOGLE MAPS     : https://maps.google.com/?q={lat:.6f},{lon:.6f}\n")
                    if r.get("address"):
                        f.write(f"    ADDRESS         : {r['address']}\n")
                else:
                    f.write("\n    GPS : No geolocation data\n")

                f.write("\n    METADATA:\n")
                for k, v in r["meta"].items():
                    f.write(f"      {str(k):<32} {v}\n")

            f.write(f"\n{'='*70}\n")
            f.write(f"-- End of Report  |  ExifXtract v{VERSION}  |  {AUTHOR} --\n")

        log.info(f"TXT report saved: {filename}")
        return filename
    except Exception as e:
        log.error(f"TXT report failed: {e}")
        return None


def save_json_report(results, filename):
    try:
        payload = {
            "tool":      "ExifXtract",
            "version":   VERSION,
            "author":    AUTHOR,
            "generated": datetime.now().isoformat(),
            "results":   [],
        }
        for r in results:
            lat, lon = r.get("lat"), r.get("lon")
            payload["results"].append({
                "file":          r["name"],
                "size_kb":       r["size"],
                "hashes":        r["hashes"],
                "stego_flagged": r.get("stego_flagged", False),
                "stego_ratio":   r.get("stego_ratio"),
                "gps": {
                    "lat":     lat,
                    "lon":     lon,
                    "address": r.get("address"),
                    "maps":    f"https://maps.google.com/?q={lat:.6f},{lon:.6f}" if lat else None,
                },
                "metadata": {str(k): str(v) for k, v in r["meta"].items()},
            })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        log.info(f"JSON report saved: {filename}")
        return filename
    except Exception as e:
        log.error(f"JSON report failed: {e}")
        return None


#  CLI display  (color-coded by tag category)


_DEVICE_TAGS = {"Make", "Model", "Software", "LensMake", "LensModel", "HostComputer"}
_TIME_TAGS   = {"DateTime", "DateTimeOriginal", "DateTimeDigitized", "GPSDateStamp"}
_GEO_TAGS    = {"GeoLatitude", "GeoLongitude", "GPSAltitude", "GPSSpeed"}
_DIM_TAGS    = {"Width", "Height", "ExifImageWidth", "ExifImageHeight", "XResolution", "YResolution"}


def _tag_color(tag):
    if tag in _DEVICE_TAGS: return "bold yellow"
    if tag in _TIME_TAGS:   return "bold green"
    if tag in _GEO_TAGS:    return "bold red"
    if tag in _DIM_TAGS:    return "bold blue"
    return "white"


def display_results_cli(r):
    console.print(Rule(f"[bold cyan]{r['name']}[/bold cyan]"))

    # Hash + file info
    ht = Table(box=box.MINIMAL_DOUBLE_HEAD, border_style="yellow", show_header=False)
    ht.add_column("k", style="bold yellow", width=10)
    ht.add_column("v", style="dim white")
    ht.add_row("MD5",    r["hashes"].get("MD5",    "N/A"))
    ht.add_row("SHA1",   r["hashes"].get("SHA1",   "N/A"))
    ht.add_row("SHA256", r["hashes"].get("SHA256", "N/A"))
    ht.add_row("Size",   f"{r['size']} KB")
    if r.get("stego_flagged"):
        ht.add_row(
            "⚠ STEGO",
            f"[bold red]File is {r['stego_ratio']}x larger than expected — possible hidden data[/bold red]"
        )
    console.print(ht)

    # GPS panel
    lat, lon = r.get("lat"), r.get("lon")
    if lat is not None and lon is not None:
        maps_url   = f"https://maps.google.com/?q={lat:.6f},{lon:.6f}"
        addr_line  = (
            f"\n[bold white]Address  :[/bold white]  [yellow]{r['address']}[/yellow]"
            if r.get("address") else ""
        )
        console.print(Align.center(Panel(
            f"[bold white]Latitude :[/bold white]  [green]{lat:.6f}[/green]\n"
            f"[bold white]Longitude:[/bold white]  [green]{lon:.6f}[/green]"
            f"{addr_line}\n"
            f"[bold white]Maps Link:[/bold white]  [cyan underline]{maps_url}[/cyan underline]",
            title="[bold red]📍 GPS Location Detected[/bold red]",
            border_style="red",
            expand=False,
        )))
    else:
        console.print("[dim]  📍 No GPS data found in this image.[/dim]")

    # Metadata table
    if r["meta"]:
        mt = Table(
            title="Extracted Metadata",
            box=box.SIMPLE,
            header_style="bold magenta",
            show_lines=False,
        )
        mt.add_column("Tag",   style="cyan", width=32)
        mt.add_column("Value")
        for k, v in r["meta"].items():
            c = _tag_color(str(k))
            mt.add_row(f"[{c}]{k}[/{c}]", str(v))
        console.print(mt)
    else:
        console.print("[red]  No metadata found.[/red]")


# ══════════════════════════════════════════════
#  Run analysis
# ══════════════════════════════════════════════

def run_analysis(files, preview=False):
    if not files:
        console.print("[red]No files to analyze.[/red]")
        return

    results = []

    for f_path in track(files, description="[cyan]Scanning...[/cyan]"):
        hashes, raw_size = get_hashes(f_path)
        meta, gps, lat, lon = extract_data(f_path)

        w = meta.get("Width", 0) or 0
        h = meta.get("Height", 0) or 0
        stego_flagged, stego_ratio = stego_check(f_path, w, h, raw_size)
        if stego_flagged:
            SESSION["flagged"] += 1

        address = None
        if lat is not None:
            with console.status("[dim]Reverse geocoding...[/dim]", spinner="dots"):
                address = reverse_geocode(lat, lon)
            SESSION["with_gps"] += 1

        SESSION["scanned"] += 1

        if preview:
            show_thumbnail(f_path)

        res = {
            "name":          os.path.basename(f_path),
            "size":          round(raw_size / 1024, 2) if raw_size else 0,
            "hashes":        hashes,
            "meta":          meta,
            "lat":           lat,
            "lon":           lon,
            "address":       address,
            "stego_flagged": stego_flagged,
            "stego_ratio":   stego_ratio,
        }
        results.append(res)
        display_results_cli(res)

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = (
        f"Report_{results[0]['name']}_{ts}"
        if len(results) == 1
        else f"Bulk_Report_{ts}"
    )

    txt  = save_txt_report(results, f"{base}.txt")
    jsn  = save_json_report(results, f"{base}.json")

    if txt:  console.print(f"\n[bold green]  TXT  → {txt}[/bold green]")
    if jsn:  console.print(f"[bold green]  JSON → {jsn}[/bold green]")

    print_summary()



#  Interactive menu

def interactive_menu():
    clear_screen()
    print_banner(force=True)

    while True:
        console.print()
        menu = Table(show_header=False, box=box.SIMPLE, border_style="cyan", show_edge=False)
        menu.add_column("opt",  style="bold cyan",  width=8)
        menu.add_column("name", style="bold white",  width=24)
        menu.add_column("desc", style="dim")
        menu.add_row("[ 1 ]", "Deep Analysis",     "Single file — full forensic scan")
        menu.add_row("[ 2 ]", "Bulk Folder Scan",  "Entire directory — batch results")
        menu.add_row("[ 3 ]", "Metadata Remover",  "Privacy shield — strip all EXIF")
        menu.add_row("[ 4 ]", "Thumbnail Preview", "Preview image then run analysis")
        menu.add_row("[ 0 ]", "Exit",               "Close session")
        console.print(Align.center(menu))

        choice = Prompt.ask(
            "\n[bold yellow]Module[/bold yellow]",
            choices=["0", "1", "2", "3", "4"],
            default="0",
        )

        if choice == "0":
            print_summary()
            console.print(
                f"\n[bold green]Session closed. Stay sharp, {AUTHOR.split()[0]}. 🕵️‍♂️[/bold green]\n"
            )
            break

        elif choice == "1":
            target = open_file_browser("file")
            if target:
                run_analysis([target])
            else:
                console.print("[red]No file selected.[/red]")

        elif choice == "2":
            d = open_file_browser("dir")
            if d:
                targets = [
                    os.path.join(d, x)
                    for x in os.listdir(d)
                    if x.lower().endswith(SUPPORTED_EXT)
                ]
                if targets:
                    run_analysis(targets)
                else:
                    console.print("[red]No supported images found in that directory.[/red]")
            else:
                console.print("[red]No directory selected.[/red]")

        elif choice == "3":
            target = open_file_browser("file")
            if target:
                with console.status("[bold red]Scrubbing metadata...[/bold red]"):
                    out = remove_metadata(target)
                if out:
                    console.print(f"\n[bold green]Done → {out}[/bold green]")
                else:
                    console.print("[red]Failed to strip metadata.[/red]")
            else:
                console.print("[red]No file selected.[/red]")

        elif choice == "4":
            target = open_file_browser("file")
            if target:
                show_thumbnail(target)
                run_analysis([target])
            else:
                console.print("[red]No file selected.[/red]")

        input("\nPress Enter to return to menu...")
        clear_screen()
        print_banner(force=True)



#  CLI argument mode  (headless)


def build_parser():
    p = argparse.ArgumentParser(
        prog="exifxtract",
        description=f"ExifXtract v{VERSION} — Image Forensics & Metadata Extractor by {AUTHOR}",
    )
    p.add_argument("--version", action="store_true", help="Show version and exit")
    p.add_argument("--path",    metavar="FILE",       help="Analyze a single image (headless)")
    p.add_argument("--dir",     metavar="DIR",        help="Bulk scan a directory (headless)")
    p.add_argument("--strip",   metavar="FILE",       help="Strip EXIF from an image and save")
    p.add_argument("--preview", action="store_true",  help="Open thumbnail preview during scan")
    return p



#  Entry point


def main():
    parser = build_parser()
    args   = parser.parse_args()

    if args.version:
        print_version()
        return

    if args.strip:
        if not os.path.exists(args.strip):
            console.print(f"[red]File not found: {args.strip}[/red]")
            sys.exit(1)
        with console.status("[bold red]Scrubbing...[/bold red]"):
            out = remove_metadata(args.strip)
        console.print(f"[bold green]Done → {out}[/bold green]" if out else "[red]Failed.[/red]")
        return

    if args.path:
        if not os.path.exists(args.path):
            console.print(f"[red]File not found: {args.path}[/red]")
            sys.exit(1)
        clear_screen()
        print_banner()
        run_analysis([args.path], preview=args.preview)
        return

    if args.dir:
        if not os.path.isdir(args.dir):
            console.print(f"[red]Directory not found: {args.dir}[/red]")
            sys.exit(1)
        targets = [
            os.path.join(args.dir, x)
            for x in os.listdir(args.dir)
            if x.lower().endswith(SUPPORTED_EXT)
        ]
        if not targets:
            console.print("[red]No supported images in that directory.[/red]")
            sys.exit(1)
        clear_screen()
        print_banner()
        run_analysis(targets, preview=args.preview)
        return

    # Default: interactive
    interactive_menu()


if __name__ == "__main__":
    main()
    if os.name == "nt":
        input("\nPress Enter to exit...")
