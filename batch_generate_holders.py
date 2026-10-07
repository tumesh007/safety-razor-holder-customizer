#!/usr/bin/env python3
"""
Batch Generator for Custom Safety Razor & Brush Holders using OpenSCAD.
Allows creating customized holders for all your shaving brushes in one go.
"""

import os
import subprocess
import sys

# Locate OpenSCAD executable
OPENSCAD_PATHS = [
    r"C:\Program Files\OpenSCAD\openscad.com",
    r"C:\Program Files\OpenSCAD\openscad.exe",
    r"C:\Program Files (x86)\OpenSCAD\openscad.com",
    r"C:\Program Files (x86)\OpenSCAD\openscad.exe",
    "openscad",
]

openscad_bin = None
for p in OPENSCAD_PATHS:
    if os.path.exists(p):
        openscad_bin = p
        break

if not openscad_bin:
    print("Error: OpenSCAD executable not found. Please verify OpenSCAD installation.")
    sys.exit(1)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCAD_FILE = os.path.join(SCRIPT_DIR, "customize_holder.scad")

# -------------------------------------------------------------------------
# DEFINE YOUR BRUSHES HERE
# Add as many brushes as you have!
# -------------------------------------------------------------------------
BRUSH_PRESETS = [
    {
        "output_filename": "Halter_Tumesh_30mm_Custom.stl",
        "knot_diameter": 30.0,
        "text_line_1": "TUMESH",
        "text_line_2": "30mm Silvertip",
        "logo_type": "Brush",
        "logo_position": "Left_Of_Text",
        "orientation": "Flat-Side (Fast 2.5h)",
    },
    {
        "output_filename": "Halter_Tumesh_24mm_Custom.stl",
        "knot_diameter": 24.0,
        "text_line_1": "TUMESH",
        "text_line_2": "22mm Knot + Play",
        "logo_type": "Brush",
        "logo_position": "Left_Of_Text",
        "orientation": "Flat-Side (Fast 2.5h)",
    },
    {
        "output_filename": "Halter_Simpson_Chubby_28.5mm.stl",
        "knot_diameter": 28.5,
        "text_line_1": "SIMPSON",
        "text_line_2": "Chubby 2 - 28.5mm",
        "logo_type": "Crown",
        "logo_position": "Left_Of_Text",
        "orientation": "Flat-Side (Fast 2.5h)",
    },
]

def generate_model(preset, output_dir=SCRIPT_DIR):
    out_stl = os.path.join(output_dir, preset["output_filename"])
    print(f"\n[+] Generating: {preset['output_filename']}")
    print(f"    Knot: {preset['knot_diameter']} mm | Line 1: '{preset['text_line_1']}' | Line 2: '{preset['text_line_2']}' | Logo: {preset['logo_type']}")

    cmd = [
        openscad_bin,
        "-o", out_stl,
        "-D", f"knot_diameter={preset['knot_diameter']}",
        "-D", f'text_line_1="{preset["text_line_1"]}"',
        "-D", f'text_line_2="{preset["text_line_2"]}"',
        "-D", f'logo_type="{preset["logo_type"]}"',
        "-D", f'logo_position="{preset.get("logo_position", "Left_Of_Text")}"',
        "-D", f'print_orientation="{preset.get("orientation", "Flat-Side (Fast 2.5h)")}"',
        SCAD_FILE,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"    -> Successfully created: {out_stl}")
    else:
        print(f"    [!] Error generating {preset['output_filename']}:")
        print(result.stderr)

def main():
    print("=" * 60)
    print(" Safety Razor & Shaving Brush Holder — Batch Generator")
    print(f" OpenSCAD: {openscad_bin}")
    print(f" SCAD Script: {SCAD_FILE}")
    print("=" * 60)

    for p in BRUSH_PRESETS:
        generate_model(p)

    print("\n[✔] All batch models generated successfully!")

if __name__ == "__main__":
    main()
