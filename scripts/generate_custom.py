#!/usr/bin/env python3
"""
Serverless / CLI Generation Script for Safety Razor & Shaving Brush Holder.
Invoked by GitHub Actions workflow or locally via Python.
"""

import argparse
import os
import shutil
import subprocess
import sys

# Ensure UTF-8 output even on legacy Windows code pages
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def find_openscad():
    """Locate OpenSCAD binary across common platforms."""
    which_bin = shutil.which("openscad")
    if which_bin:
        return which_bin

    windows_paths = [
        r"C:\Program Files\OpenSCAD\openscad.com",
        r"C:\Program Files\OpenSCAD\openscad.exe",
        r"C:\Program Files (x86)\OpenSCAD\openscad.com",
        r"C:\Program Files (x86)\OpenSCAD\openscad.exe",
    ]
    for p in windows_paths:
        if os.path.exists(p):
            return p

    mac_paths = [
        "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD",
        os.path.expanduser("~/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"),
    ]
    for p in mac_paths:
        if os.path.exists(p):
            return p

    return None

def main():
    parser = argparse.ArgumentParser(description="Generate customized Safety Razor & Brush Holder STL.")
    parser.add_argument("--knot", type=float, default=28.5, help="Brush knot diameter in mm (22.0 to 34.0)")
    parser.add_argument("--line1", type=str, default="TUMESH", help="Primary name / branding line")
    parser.add_argument("--line2", type=str, default="30mm Silvertip", help="Secondary brush model / hair line")
    parser.add_argument("--logo", type=str, default="Brush", choices=["Brush", "Razor", "Crown", "Star", "None", "Custom_SVG"], help="Emblem type")
    parser.add_argument("--orientation", type=str, default="Flat-Side (Fast 2.5h)", choices=["Flat-Side (Fast 2.5h)", "Upright (Standard 4.2h)"], help="Print orientation")
    parser.add_argument("--deboss", type=float, default=0.8, help="Deboss depth in mm (0.4 to 1.5)")
    parser.add_argument("--output", type=str, default=None, help="Output STL filename")

    args = parser.parse_args()

    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scad_file = os.path.join(repo_dir, "customize_holder.scad")

    if not os.path.exists(scad_file):
        print(f"[!] Error: Could not find {scad_file}")
        sys.exit(1)

    openscad_bin = find_openscad()
    if not openscad_bin:
        print("[!] Error: OpenSCAD executable not found on system.")
        sys.exit(1)

    if not args.output:
        safe_line1 = "".join(c for c in args.line1 if c.isalnum() or c in ("_", "-")).strip() or "Custom"
        args.output = os.path.join(repo_dir, f"Safety_Razor_Holder_{args.knot}mm_{safe_line1}.stl")

    print("=" * 65)
    print(" [+] Safety Razor & Shaving Brush Holder Generator")
    print(f" Engine      : {openscad_bin}")
    print(f" Template    : {scad_file}")
    print(f" Output      : {args.output}")
    print(f" Knot Size   : {args.knot} mm")
    print(f" Line 1 Text : '{args.line1}'")
    print(f" Line 2 Text : '{args.line2}'")
    print(f" Emblem Logo : {args.logo}")
    print(f" Orientation : {args.orientation}")
    print(f" Deboss Depth: {args.deboss} mm")
    print("=" * 65)

    cmd = [
        openscad_bin,
        "-o", args.output,
        "-D", f"knot_diameter={args.knot}",
        "-D", f'text_line_1="{args.line1}"',
        "-D", f'text_line_2="{args.line2}"',
        "-D", f'logo_type="{args.logo}"',
        "-D", f'print_orientation="{args.orientation}"',
        "-D", f"deboss_depth={args.deboss}",
        scad_file
    ]

    print("[*] Running OpenSCAD compilation...")
    res = subprocess.run(cmd, capture_output=True, text=True)

    if res.returncode == 0 and os.path.exists(args.output):
        size_kb = os.path.getsize(args.output) / 1024
        print(f"[OK] Successfully generated STL: {args.output} ({size_kb:.1f} KB)")
    else:
        print(f"[!] Failed to generate STL. Return code: {res.returncode}")
        if res.stderr:
            print("--- OpenSCAD Error Output ---")
            print(res.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
