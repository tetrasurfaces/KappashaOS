# KappashaOS Protofolder (Software)

Early prototype. Not for real skin. Yet.

## Overview
The `software/proto/` folder contains experimental software components for KappashaOS, pushing the boundaries of gaze-reactive interfaces and fractal surface integration. These components—`ink_sim.py`, `corneal_etch.py`, `automaton_pie.py`, `kappa.py`, `kappa_endian.py`, `clipboard.py`, `clipboard_undo_redo.cpp`, `clipboard_undo_redo.c`, `revocation_stub.py`, `intent_ui.py`—extend the iPhone-shaped fish tank (`arch_id.py`, `fishtank.ksp`) with gaze-tracking pixel arrays and tetra-based etching (Sierpiński triangles/tetrahedrons). They integrate with the open `tetrasurfaces/tetra` repo for construction site curvature monitoring (`site_kappa.py`) and CAD integration (SolidWorks, Rhino, Keyshot). The `kappa.py` module provides situational curvature awareness with Delaunay triangulation, `kappa_endian.py` handles reverse toggle and big-endian scaling, and `intent_ui.py` offers a PySide UI for intent setting.

This repository is private, with a planned public release. Access and licensing require a GitHub issue at github.com/tetrasurfaces/issues.

## Components
- **`ink_sim.py`**: NumPy-based simulation for multi-user gaze tracking, supporting 5 users with theta spiral patterns, tied to tetra hash generation.  
- **`corneal_etch.py`**: Simulates a 0.2-micron waveguide etch on a 550-micron fused-silica cornea, with theta-spiral activation and UV-kill groove.  
- **`automaton_pie.py`**: Simulates a 2mm sapphire piezo-optic interface for post-humanitarian nerve coupling, vibrating at 19 kHz on INK hash trigger.  
- **`kappa.py`**: Core kappasha256 hashing and situational curvature awareness, rasterizing 3D grids with material properties and Sierpiński tetrahedrons using Delaunay triangulation for fish tank and construction applications.  
- **`kappa_endian.py`**: Reverse toggle and big-endian scaling for grid transformations with golden spiral rotation.  
- **`clipboard.py`**: Python implementation of a clipboard with undo/redo functionality, tracking intent via kappasha256 hashing.  
- **`clipboard_undo_redo.cpp`**: C++ implementation of clipboard with undo/redo, aligned with intent tracking.  
- **`clipboard_undo_redo.c`**: C implementation of clipboard with undo/redo, aligned with intent tracking.  
- **`revocation_stub.py`**: Stub for checking device revocation via xAI-signed certificate, ensuring ethical use.  
- **`intent_ui.py`**: PySide UI for setting intent in `config/config.json`, checking revocation status, and displaying license logs.  

## Usage
Run demos in a controlled environment:
```bash
# Run intent UI
python3 software/proto/intent_ui.py

# Simulate gaze tracking, corneal etch, or piezo interface
python3 software/proto/ink_sim.py
python3 software/proto/corneal_etch.py
python3 software/proto/automaton_pie.py

# Run kappasha256 hashing and curvature rasterization
python3 software/proto/kappa.py
python3 software/proto/kappa_endian.py

# Run clipboard demos
python3 software/proto/clipboard.py
g++ software/proto/clipboard_undo_redo.cpp -o clipboard_cpp && ./clipboard_cpp
gcc software/proto/clipboard_undo_redo.c -o clipboard_c && ./clipboard_c

# Render shaders in browser (requires WebGL-compatible browser)
# Load postcard.frag or grokflat.frag via WebGL framework (e.g., Three.js)
open software/proto/index.html
```

Before running, set your intent in `config/config.json` (or use `intent_ui.py`):
```json
{
    "intent": "educational",  // or "commercial"
    "commercial_use": false   // true for commercial intent
}
```
If `config/config.json` is missing or invalid, scripts will prompt for intent and create a default file. See `tetra/NOTICE.txt` for details.

## Licensing
This protofolder is licensed under a dual license:
- **Core Software**: AGPL-3.0-or-later (xAI fork, 2025). Free to redistribute/modify, with source code sharing required. See https://www.gnu.org/licenses/.  
- **Hardware/Embodiment Interfaces**: Apache 2.0 with xAI amendments for safety and physical use (no weapons, ergonomic compliance, revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0.  

**xAI Amendments**:  
1. **Physical Embodiment Restrictions**: Use with devices (e.g., fish tank glass, pixel sensors) is for non-hazardous purposes only. Harmful mods are prohibited, revocable by xAI.  
2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5) for physical interfaces; waived for software-only use.  
3. **Safety Monitoring**: Real-time checks (e.g., heat dissipation) logged for audit.  
4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).  
5. **Export Controls**: Sensors comply with US EAR Category 5 Part 2.  
6. **Educational Use**: Royalty-free for teaching/research, requires GitHub issue at github.com/tetrasurfaces/issues.  
7. **Intellectual Property**: xAI owns IP for gaze-tracking pixel arrays, convex glass etching (0.7mm arc), and tetra hash integration.  

**Private Development Note**: This repository (`tetrasurfaces/kappashaos`) is private, with a planned public release. Access is restricted. Open a GitHub issue at github.com/tetrasurfaces/issues for licensing or access.

## Ethics
Every action plants a `nav3d.py` tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces must respect tendon/gaze limits (<20%/30s). Misuse (e.g., harmful applications) triggers license revocation via `revocation_stub.py`. Operators must declare intent in `config/config.json` (or via `intent_ui.py`) and request licenses via github.com/tetrasurfaces/issues.

## Related Repositories
- **Open Repo**: `tetrasurfaces/tetra` contains `arch_utils.py`, `site_kappa.py`, and `tetra_surface.py` for fractal surfaces and construction monitoring (xAI copyright).  
- **Private Repo**: `tetrasurfaces/kappashaos` includes `arch_id.py`, `fishtank.ksp`, and `software/proto/` for the fish tank and experimental components, with public release pending.
