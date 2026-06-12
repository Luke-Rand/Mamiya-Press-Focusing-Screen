# Mamiya Press Parametric Focusing Screen Adapter

A parametric 3D-printable focusing screen mounting system for the classic **Mamiya Press** line of medium format cameras. 

Built using **CadQuery**, this repository generates high-fidelity STL and STEP models for an adapter body that slots into the camera's rear mount interface, along with matching pressure plates and clamps to secure your focusing medium.

---

## Features

- **Double-Pocket Adapter Design**:
  - The glass focusing adapter uses a concentric double-pocket layout on the front face: an outer pocket ($70\text{ mm} \times 70\text{ mm}$ at $2.5\text{ mm}$ depth) to seat the pressure plate, and an inner pocket ($60.5\text{ mm} \times 60.5\text{ mm}$ at $6.5\text{ mm}$ depth) to hold the focusing glass.
- **M2 Hex Nut Channels**:
  - Pockets on the camera-facing back face (`<Z`) house captured M2 nuts (width $4.3\text{ mm}$, depth $1.8\text{ mm}$), creating a durable metal-threaded connection that prevents plastic stripping.
  - The hex pockets are rotated such that their flat edges face the light trap groove, maximizing wall thickness ($0.8\text{ mm}$ clearance) and ensuring print integrity.
- **Universal M2 Screw Compatibility**:
  - The countersink depth on the pressure plate is set to $1.6\text{ mm}$, supporting both standard **M2 x 4 mm** (engages $3.5$ threads of the nut) and **M2 x 6 mm** (engages the full nut, ending flush inside the pocket) countersunk screws.
- **Snug Fit & Focus Calibration**:
  - The adapter body is **$7.0\text{ mm}$** thick to slide securely into the camera adapter mount.
  - The registration plane sits at a distance of **$0.5\text{ mm}$** from the camera-facing back face, ensuring the ground glass/paper surface aligns perfectly for infinity focus.
- **Multi-Format Generation**:
  - Both scripts automatically output files for four distinct image formats:
    - **`60x45_vertical`** (Portrait 6x4.5 format)
    - **`60x60`** (Square 6x6 format)
    - **`60x70`** (6x7 landscape format)
    - **`60x90`** (Full 6x9 format)

---

## Repository Structure

```text
Mamiya-Press-Focusing-Screen/
├── .gitignore                    # Excludes build outputs & environments
├── README.md                     # This documentation
├── requirements.txt              # Project dependencies
├── build.py                      # One-click CAD export script
├── glass-focusing-screen.py      # CAD instructions for glass screen assembly
├── paper-focusing-screen.py      # CAD instructions for paper screen assembly
└── exports/                      # Generated CAD outputs (created by build.py)
    ├── glass/                    # Glass screen components for each format size
    │   ├── mamiya_screen_body_60x45_vertical.stl/step
    │   ├── glass_retention_ring_60x45_vertical.stl/step
    │   ├── mamiya_screen_body_60x60.stl/step
    │   ├── glass_retention_ring_60x60.stl/step
    │   ├── mamiya_screen_body_60x70.stl/step
    │   ├── glass_retention_ring_60x70.stl/step
    │   ├── mamiya_screen_body_60x90.stl/step
    │   └── glass_retention_ring_60x90.stl/step
    └── paper/                    # Paper screen components for each format size
        ├── mamiya_screen_body_60x45_vertical.stl/step
        ├── paper_retention_ring_60x45_vertical.stl/step
        ├── mamiya_screen_body_60x60.stl/step
        ├── paper_retention_ring_60x60.stl/step
        ├── mamiya_screen_body_60x70.stl/step
        ├── paper_retention_ring_60x70.stl/step
        ├── mamiya_screen_body_60x90.stl/step
        └── paper_retention_ring_60x90.stl/step
```

---

## 3D Printing Recommendations

For the best results, adhere to the following slicing parameters:

| Parameter | Recommended Value | Rationale |
| :--- | :--- | :--- |
| **Material** | **PETG**, **ABS**, or **ASA** | High durability and temperature resistance (prevents warping in hot cars). |
| **Color** | **Matte Black** | Minimizes internal light scattering and reflection inside the camera body. |
| **Layer Height** | `0.15 mm` or `0.20 mm` | Higher resolution ensures smooth registration steps and precise hex nut slots. |
| **Perimeters (Walls)** | `3` or `4` | Enhances structural stiffness for sliding mounts. |
| **Infill** | `20% - 30%` (Gyroid or Grid) | Balances weight and torsional stability. |
| **Supports** | **None** | Designed to print flat on the build plate without support material. |

---

## Assembly & Focusing Medium Sizing

### 1. The Glass Focusing Screen
- **Medium Dimensions**: Select the glass plate size to match your format width (45, 60, 70, or 90 mm) by 60.0 mm height (thickness $2.0\text{ mm}$).
- **Hardware Needed**: 
  - 4x **M2 Hex Nuts** (standard $1.6\text{ mm}$ thickness, $4.0\text{ mm}$ flat-to-flat).
  - 4x **M2 x 4 mm** or **M2 x 6 mm** countersunk head screws.
- **Grinding (DIY)**: Use 600-grit silicon carbide powder or aluminum oxide slurry on raw glass to grind a uniform frosted surface.
- **Orientation**: Drop the glass into the main body pocket with the **frosted/matte side facing the lens** (i.e. resting directly against the pocket's bottom registration ledge).
- **Assembly**:
  1. Insert the M2 nuts into the pockets on the back of the adapter body.
  2. Drop the glass sheet in from the front.
  3. Fit the pressure plate on top.
  4. Screw down securely through the front of the plate.

### 2. The Paper Focusing Screen
- **Medium Dimensions**: Match your selected format width (45, 60, 70, or 90 mm) by 60.0 mm height (using high-quality translucent drafting film, drafting paper, or vellum paper).
- **Orientation**: Place the paper flat against the bottom ledge of the pocket.
- **Retention**: Press-fit the friction retention ring down into the pocket. This clamps the paper flat and prevents sagging, maintaining focal plane alignment.

---

## Local Development Setup

To compile the CAD models yourself and modify the designs, set up your Python environment as follows.

### Prerequisites
- Python 3.10 through 3.13 (macOS, Windows, and Linux are supported).

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

All compiled output files (`.stl` and `.step` formats) will be generated in the `exports/` folder.
