# Mamiya Press Parametric Focusing Screen Adapter

A parametric 3D-printable focusing screen mounting system for the classic **Mamiya Press** line of medium format cameras. 

Built using **CadQuery**, this repository generates high-fidelity STL and STEP models for an adapter body that slots into the camera's rear interface, along with matching friction-fit retention rings to lock your focusing medium in place.

---

## Features

- **Modular Design**: A single, unified adapter body profile compatible with multiple focusing media.
- **Glass Ground Glass Support**: Optimized for a standard 60.0 mm x 60.0 mm x 2.0 mm glass pane (with a 1.5 mm retention ring).
- **Drafting Film / Paper Support**: Optimized for a thin sheet of drafting film or translucent tracing paper sized 95.0 mm x 72.0 mm (with a thicker 3.4 mm retention ring).
- **Exact Film Plane Alignment**: The pocket depth is meticulously set so the matte/focusing surface sits exactly at the camera's registration plane.
- **Parametric Modification**: Modify any dimensions (pocket clearance, plate thickness, view windows) directly in the Python source code.
- **CQ-Editor & CLI Compatible**: Use interactively inside the `CQ-Editor` GUI, or compile headlessly using the included `build.py` script.

---

## Repository Structure

```
Mamiya-Press-Focusing-Screen/
├── .gitignore                    # Excludes build outputs & environments
├── README.md                     # This documentation
├── requirements.txt              # Project dependencies
├── build.py                      # One-click CAD export script
├── glass-focusing-screen.py      # CAD instructions for glass screen assembly
├── paper-focusing-screen.py      # CAD instructions for paper screen assembly
└── exports/                      # Generated CAD outputs (created by build.py)
    ├── glass/                    # Glass screen components
    │   ├── mamiya_screen_body.stl
    │   ├── mamiya_screen_body.step
    │   ├── glass_retention_ring.stl
    │   └── glass_retention_ring.step
    └── paper/                    # Paper screen components
        ├── mamiya_screen_body.stl
        ├── mamiya_screen_body.step
        ├── paper_retention_ring.stl
        └── paper_retention_ring.step
```

---

## 3D Printing Recommendations

For the best results, adhere to the following slicing parameters:

| Parameter | Recommended Value | Rationale |
| :--- | :--- | :--- |
| **Material** | **PETG**, **ABS**, or **ASA** | High durability and temperature resistance (prevents warping in hot cars). |
| **Color** | **Matte Black** | Minimizes internal light scattering and reflection inside the camera body. |
| **Layer Height** | `0.15 mm` or `0.20 mm` | Higher resolution ensures smooth registration steps and precise friction fits. |
| **Perimeters (Walls)** | `3` or `4` | Enhances structural stiffness for sliding mounts. |
| **Infill** | `20% - 30%` (Gyroid or Grid) | Balances weight and torsional stability. |
| **Supports** | **None** | Designed to print flat on the build plate without support material. |

---

## Assembly & Focusing Medium Sizing

### 1. The Glass Focusing Screen
- **Medium Dimensions**: 60.0 mm x 60.0 mm x 2.0 mm glass plate.
- **Files**: Use `exports/glass/mamiya_screen_body.stl` and `exports/glass/glass_retention_ring.stl`.
- **Grinding (DIY)**: Use 600-grit silicon carbide powder or aluminum oxide slurry on raw glass to grind a uniform frosted surface.
- **Orientation**: Drop the glass into the main body pocket with the **frosted/matte side facing the lens** (i.e. resting directly against the pocket's bottom registration ledge).
- **Retention**: Press-fit the thin retention ring on top of the glass.

### 2. The Paper Focusing Screen
- **Medium Dimensions**: 95.0 mm x 72.0 mm high-quality translucent drafting film, drafting paper, or vellum paper.
- **Files**: Use `exports/paper/mamiya_screen_body.stl` and `exports/paper/paper_retention_ring.stl`.
- **Orientation**: Place the paper flat against the bottom ledge of the pocket.
- **Retention**: Press-fit the thicker retention ring down into the pocket. This clamps the paper flat and prevents sagging, maintaining focal plane alignment.

---

## Local Development Setup

To compile the CAD models yourself and modify the designs, set up your Python environment as follows.

### Prerequisites
- Python 3.10 through 3.13 (macOS, Windows, and Linux are supported).
- Homebrew (macOS) if Python is not installed.

### Setup and Compilation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Mamiya-Press-Focusing-Screen
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the builder**:
   ```bash
   python3 build.py
   ```

All compiled output files (`.stl` and `.step` formats) will be generated in a newly created `exports/` folder.
