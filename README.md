# 🪒 Parametric Safety Razor & Shaving Brush Holder

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg)](LICENSE)
[![Format: STEP & STL](https://img.shields.io/badge/CAD_Format-STEP_%26_STL-blue.svg)](models/)
[![OpenSCAD Customizer](https://img.shields.io/badge/Parametric-OpenSCAD-brightgreen.svg)](customize_holder.scad)

A high-speed, custom-fit 3D printable holder for traditional safety razors, shaving brushes, soap bowls, and replacement blades. 

This repository features:
- **Fast-Print Flat-Side Orientation**: Cuts print time from **4h 15m down to 2h 28m (~40% faster)** by correcting the subtle 4.2° draft angle.
- **Parametric OpenSCAD Customizer**: Adjust brush knot diameters ($22\,\text{mm}$ to $34\,\text{mm}$), dual-line personalized debossed text, and vector emblems.
- **Solid Perimeter Generation**: Eliminates hand-filing and prevents ugly hollow infill cavities from being exposed.
- **Pre-Rendered Models**: Ready-to-slice STLs and CAD STEP files for standard $24\,\text{mm}$, $28.5\,\text{mm}$, and $30\,\text{mm}$ shaving brushes.
- **Studio Rendering Pipeline**: Built-in FreeCAD & VTK PBR rendering script to generate publication-grade showcase images with zero GPU dependencies.

---

## 🎨 Studio Product Showcase

| Studio Hero View (Upright) | Top Functional Overview |
| :---: | :---: |
| ![Studio Hero View](docs/images/render_hero_studio.png) | ![Top Functional Overview](docs/images/render_top_overview.png) |

| Personalized Bottom Branding (Debossed) | Fast-Print Flat-Side Bed Adhesion (PEI Plate) |
| :---: | :---: |
| ![Personalized Bottom Branding](docs/images/render_bottom_branding.png) | ![Fast-Print Bed Adhesion](docs/images/render_flatside_bed.png) |

---

## 📸 Technical Analyses & Diagrams

| Fast-Print Flat Orientation (2h 28m) | Draft-Angle Bed Alignment (17.3 cm² Contact) |
| :---: | :---: |
| ![Orientation Comparison](docs/images/orientation_comparison.png) | ![Bed Alignment Verification](docs/images/true_side_alignment_verification.png) |

| OpenSCAD Customizer UI | Parametric Knot Cross-Sections |
| :---: | :---: |
| ![Bottom Customizer Preview](docs/images/bottom_customizer_preview.png) | ![Brush Knot Cross Sections](docs/images/brush_sections.png) |

---

## ⚡ Why This Redesign?

### 1. The 4.2° Draft Angle Problem Solved
In the original model, the side wall has a subtle $4.2^\circ$ aesthetic taper (normal vector `[0.074, 0.997, 0.033]`). If you simply lay the holder on its side using a standard 90° rotation in your slicer, **only a single sharp corner touches the build plate**, leaving the rest of the model hovering in mid-air.

This project incorporates the exact compensatory affine transformation matrix:
```
R = [
  [ 0.994385, -0.075946,  0.073695,  0.000000 ],
  [-0.075946, -0.027196,  0.996741,  0.000000 ],
  [-0.073695, -0.996741, -0.032811, 34.229908 ],
  [ 0.000000,  0.000000,  0.000000,  1.000000 ]
]
```
This forces the entire side flank into a **100% planar contact ($17.32\,\text{cm}^2$ bed adhesion at $Z = 0.00\,\text{mm}$)**, eliminating bed-lifting warping and reducing print time from **4.2 hours to 2.5 hours**.

### 2. Solid Walls vs. Hand-Filing Cavities
Commercial shaving brushes vary widely in knot diameter:
- Small / Travel knots: $20 - 22\,\text{mm}$
- Standard knots: $24 - 26\,\text{mm}$
- Oversized / Dense badger knots: $28 - 30\,\text{mm}$

If you attempt to file down an undersized print by hand, the outer wall perimeters are worn through, immediately exposing the hollow grid/gyroid infill. By setting the diameter parametrically in CAD, your slicer constructs **3 to 4 continuous solid concentric perimeters** around the opening, providing a smooth, watertight, and hygienic finish.

---

## 📦 Pre-Rendered Models Catalog

Production-ready models are available in both **STL** (3D printing) and **STEP** (CAD engineering) in the [`models/`](models/) directory:

| Knot Diameter | Brush Clearance | Recommended Brushes | Fast-Print (Flat-Side) | Upright Standard |
| :---: | :---: | :---: | :---: | :---: |
| **24.0 mm** | Up to $22.5\,\text{mm}$ | Omega 10065, Semogue 1438, Simpson Classic 1, 20-22mm knots | [`models/24mm/`](models/24mm/) | [`models/24mm/`](models/24mm/) |
| **28.0 mm** | Up to $26.5\,\text{mm}$ | Original geometry base models | [`models/28mm/`](models/28mm/) | [`models/28mm/`](models/28mm/) |
| **28.5 mm** | Up to $27.0\,\text{mm}$ | Simpson Duke 3, Muhle Silvertip 25mm, Yaqi 26mm synthetics | [`models/28.5mm/`](models/28.5mm/) | [`models/28.5mm/`](models/28.5mm/) |
| **30.0 mm** | Up to $28.5\,\text{mm}$ | Simpson Chubby 2/3, Stirling 28mm Kong, Zenith Pro badger knots | [`models/30mm/`](models/30mm/) | [`models/30mm/`](models/30mm/) |

---

## 🖨️ Recommended Slicer Settings

| Parameter | Bambu Studio / OrcaSlicer | PrusaSlicer / SuperSlicer |
| :--- | :--- | :--- |
| **Print Orientation** | **Flat-Side** (Fast 2.5h) | **Flat-Side** (Fast 2.5h) |
| **Support Type** | **Tree (auto)** / Tree Slim | **Organic** |
| **Support Placement** | Support on build plate only | For support enforcers only / Build plate |
| **Overhang Threshold** | 35° – 40° | 35° – 40° |
| **Wall Loops** | **3 to 4 walls** (1.2 - 1.6 mm) | **3 to 4 perimeters** |
| **Top / Bottom Shells** | 4 Top / 4 Bottom | 4 Top / 4 Bottom |
| **Infill Density** | 15% – 20% | 15% – 20% |
| **Infill Pattern** | Gyroid or Cross Hatch | Gyroid |
| **Layer Height** | 0.20 mm (0.16 mm for high-detail text) | 0.20 mm |
| **Recommended Material**| **PETG** (moisture and soap resistant) | **PETG** or **PLA+** |

> **Tree Support Tip**: When slicing in Flat-Side orientation, tree supports will sprout exclusively to support the razor prong overhangs and the curved interior rim. They pop off cleanly with minimal post-processing.

---

## 🛠️ OpenSCAD Customizer Guide

Create a fully custom holder tailored to your exact brush model and personalized branding:

1. Download and install [OpenSCAD](https://openscad.org/) (v2021.01 or newer).
2. Open [`customize_holder.scad`](customize_holder.scad).
3. If the customizer window is not visible, navigate to `Window` -> uncheck `Hide Customizer`.
4. Adjust the parameters:
   - **Knot Diameter**: Slider from $22.0\,\text{mm}$ to $34.0\,\text{mm}$.
   - **Primary Text**: e.g., `"Tumesh"` (Font size 4–14 mm).
   - **Secondary Text**: e.g., `"30mm Silvertip"` (Font size 3–10 mm).
   - **Emblem / Logo**: Choose from `"Brush"`, `"Razor"`, `"Crown"`, `"Star"`, `"Custom_SVG"`, or `"None"`.
   - **Custom SVG**: Place any monochrome `.svg` (like `my_logo.svg`) in the folder to engrave your personal maker mark.
   - **Print Orientation**: Select `"Flat-Side (Fast 2.5h)"` or `"Upright (Standard 4.2h)"`.
5. Press `F5` to preview and `F6` to render.
6. Press `F7` or click `File -> Export as STL`.

---

## 📸 Re-Generating Studio Renders (FreeCAD + VTK)

To re-render the studio images at 1080p with physically based PBR lighting:

```bash
& "C:\Program Files\FreeCAD 1.1\bin\python.exe" scripts/render_studio_freecad.py
```

This headless pipeline runs completely CPU/OpenGL offscreen, ensuring 100% reliable output on any workstation without GPU dependency.

---

## 💻 Automated Batch Generation (Python)

If you have multiple brushes or want to batch-export a catalog of models:

```bash
python batch_generate_holders.py
```

This script invokes OpenSCAD in headless CLI mode (`openscad.com -o output.stl -D ...`) and builds custom variations in parallel.

---

## 📄 Documentation

For full geometric analyses, contact area verification calculations, and overhang maps, see the Word document in [`docs/Safety_Razor_Holder_Documentation.docx`](docs/Safety_Razor_Holder_Documentation.docx).

---

## 📜 Attribution & License

- **Original Design**: Based on *"Safety razor holder + soap, brush and blades"* by **ConstruKt 3D** ([Thingiverse: thing:2860456](https://www.thingiverse.com/thing:2860456)).
- **Parametric OpenSCAD System, Draft Angle Alignment & Batch Tools**: Created by [tumesh007](https://github.com/tumesh007).
- **License**: Released under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](LICENSE) license.
