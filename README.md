# KappashaOS

Experimental platform for gaze-reactive interfaces and fractal surface integration, powering the iPhone-shaped fish tank, Fish Eye prototype, and related components. This repository is private, with a planned public release. It extends the tetra/kappasha workflow (Sierpiński triangles/tetrahedrons, kappasha256 hashing) from the open `tetrasurfaces/tetra` repo, focusing on industrial design (Keyshot rendering, gaze-tracking pixels) and cyberpunk experiments.

## Overview
KappashaOS drives the iPhone-shaped fish tank—a 0.7mm convex glass device with tetra-etched surfaces (15-micron depth at crown, 5-micron at edge), gaze-tracking pixel arrays, and a 60ml water volume with micro-bubble system. The Fish Eye prototype (`hardware/proto/fish_eye.py`, `fish_eye_keys.ksp`) is a 50mm fused-silica sphere with SMP iris blades, designed as an autonomous pupil. The `hardware/proto/` folder also includes `repo_audit.py` for repo auditing and `copyright_snapshot.txt` as a generated repo state snapshot. The `software/proto/` folder contains experimental software components (e.g., gaze tracking, corneal etching, clipboard functionality, curvature awareness, intent UI), while `hardware/proto/` includes hardware specifications (e.g., fish tank glass, Fish Eye). All components integrate with `tetrasurfaces/tetra`’s core utilities for fractal surfaces and construction monitoring.

## Components
- **`arch_id.py`**: Python script for live Keyshot rendering of the fish tank, applying tetra hashes and dynamic bump maps for gaze-reactive etching.  
- **`fishtank.ksp`**: Keyshot scene file (placeholder) for the fish tank, with convex glass, water volume, and gaze-tracking animations.  
- **`hardware/proto/`**: Hardware specifications and drivers:  
  - `fish_eye.py`: Python driver for rendering Fish Eye keysheet (50mm sphere, tetra etch, SMP iris).  
  - `fish_eye_keys.ksp`: Keyshot scene pack for Fish Eye, 36 frames with 10° sweep, 4096x4096 resolution.  
  - `repo_audit.py`: Python utility to audit the KappashaOS GitHub repo, fetching commits and file contents with intent and revocation checks.  
  - `copyright_snapshot.txt`: Generated snapshot of repo commit history and file contents, created by `repo_audit.py`, kept private for legal audit purposes.  
- **`software/proto/`**: Experimental software components:  
  - `ink_sim.py`: NumPy-based gaze tracking simulation for 5 users with theta spiral patterns.  
  - `corneal_etch.py`: Simulates 0.2-micron waveguide etch on fused-silica cornea.  
  - `automaton_pie.py`: Simulates 2mm sapphire piezo-optic interface for nerve coupling.  
  - `kappa.py`: Core kappasha256 hashing and situational curvature awareness using Delaunay triangulation.  
  - `kappa_endian.py`: Reverse toggle and big-endian scaling for grid transformations with golden spiral rotation.  
  - `clipboard.py`: Python clipboard with undo/redo, intent tracking via kappasha256.  
  - `clipboard_undo_redo.cpp`: C++ clipboard with undo/redo, intent tracking.  
  - `clipboard_undo_redo.c`: C clipboard with undo/redo, intent tracking.  
  - `revocation_stub.py`: Stub for device revocation via xAI-signed certificate.  
  - `intent_ui.py`: PySide UI for setting intent in `config/config.json`, checking revocation status, and displaying license logs.  

## Usage
1. **Set Intent**: Use `intent_ui.py` or edit `config/config.json`:
   ```json
   {
       "intent": "educational",  // or "commercial"
       "commercial_use": false   // true for commercial intent
   }
   ```
   If missing or invalid, scripts or UI prompt for intent and create a default file. See `tetra/NOTICE.txt`.  
2. **Run Fish Tank Rendering**:
   ```bash
   python3 arch_id.py
   ```
   Requires Keyshot and `fishtank.ksp`. Outputs live renders at 1080x1920, 20 FPS.  
3. **Run Fish Eye Rendering**:
   ```bash
   python3 hardware/proto/fish_eye.py
   ```
   Requires Keyshot and `fish_eye_keys.ksp`. Outputs 36-frame keysheet at 4096x4096.  
4. **Audit Repo and Generate Snapshot**:
   ```bash
   python3 hardware/proto/repo_audit.py
   ```
   Outputs `copyright_snapshot.txt` with commit history and file contents. Requires a GitHub token set as `GITHUB_TOKEN` environment variable.  
5. **Run Proto Demos**:
   ```bash
   python3 software/proto/intent_ui.py  # Intent UI
   python3 software/proto/ink_sim.py  # Gaze tracking simulation
   python3 software/proto/corneal_etch.py  # Corneal etching simulation
   python3 software/proto/automaton_pie.py  # Piezo interface simulation
   python3 software/proto/kappa.py  # Kappasha256 hashing and curvature
   python3 software/proto/kappa_endian.py  # Grid transformations
   python3 software/proto/clipboard.py  # Clipboard demo
   g++ software/proto/clipboard_undo_redo.cpp -o clipboard_cpp && ./clipboard_cpp
   gcc software/proto/clipboard_undo_redo.c -o clipboard_c && ./clipboard_c
   # Load postcard.frag, grokflat.frag in WebGL browser (e.g., via Three.js)
   open software/proto/index.html
   ```
6. **License**: Open a GitHub issue at github.com/tetrasurfaces/issues for access or licensing (royalty-free for educational use).

## Licensing
Licensed under a dual AGPL-3.0 (software) and Apache 2.0 with xAI amendments (hardware). See `LICENSE.txt`.  
- **Educational Use**: Royalty-free for teaching/research, requires GitHub issue.  
- **Commercial Use**: Requires negotiated approval via github.com/tetrasurfaces/issues.  
- **IP**: xAI owns fish tank and Fish Eye IP (gaze-tracking, convex etching, tetra hashing).  
- **Ethics**: Tendon/gaze limits (<20%/30s), revocable for misuse (e.g., surveillance).  
- **Export Controls**: Complies with US EAR Category 5 Part 2.

## Ethics
Every action plants a `nav3d.py` tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces respect tendon/gaze limits. Misuse triggers license revocation via `revocation_stub.py`. Declare intent in `config/config.json` (or via `intent_ui.py`) and request licenses via github.com/tetrasurfaces/issues.

## Related Repositories
- **Open Repo**: `tetrasurfaces/tetra` contains `arch_utils.py`, `site_kappa.py`, `tetra_surface.py` for fractal surfaces and construction monitoring (xAI copyright).  
- **Private Repo**: `tetrasurfaces/kappashaos` (this repo) includes `arch_id.py`, `fishtank.ksp`, `hardware/proto/`, and `software/proto/` for the fish tank, Fish Eye, and experimental components, with public release pending.
