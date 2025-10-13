# KappashaOS

Experimental platform for gaze-reactive interfaces and fractal surface integration, powering the iPhone-shaped fish tank and related prototypes. This repository is private, with a planned public release. It extends the tetra/kappasha workflow (Sierpiński triangles/tetrahedrons, kappasha256 hashing) from the open `tetrasurfaces/tetra` repo, focusing on industrial design (Keyshot rendering, gaze-tracking pixels) and cyberpunk experiments.

## Overview
KappashaOS drives the iPhone-shaped fish tank—a 0.7mm convex glass device with tetra-etched surfaces (15-micron depth at crown, 5-micron at edge), gaze-tracking pixel arrays, and a 60ml water volume with micro-bubble system. The `software/proto/` folder contains experimental software components (e.g., gaze tracking, corneal etching, clipboard functionality), while `hardware/proto/` will include hardware specifications (e.g., fish tank glass, piezo interfaces). All components integrate with `tetrasurfaces/tetra`’s core utilities for fractal surfaces and construction monitoring.

## Components
- **`arch_id.py`**: Python script for live Keyshot rendering of the fish tank, applying tetra hashes and dynamic bump maps for gaze-reactive etching.  
- **`fishtank.ksp`**: Keyshot scene file (placeholder) for the fish tank, with convex glass, water volume, and gaze-tracking animations.  
- **`software/proto/`**: Experimental software components:  
  - `ink_sim.py`: NumPy-based gaze tracking simulation for 5 users with theta spiral patterns.  
  - `corneal_etch.py`: Simulates 0.2-micron waveguide etch on fused-silica cornea.  
  - `automaton_pie.py`: Simulates 2mm sapphire piezo-optic interface for nerve coupling.  
  - `kappa.py`: Core kappasha256 hashing logic for tetra surfaces.  
  - `clipboard.py`: Python clipboard with undo/redo, intent tracking via kappasha256.  
  - `clipboard_undo_redo.cpp`: C++ clipboard with undo/redo, intent tracking.  
  - `clipboard_undo_redo.c`: C clipboard with undo/redo, intent tracking.  
  - `revocation_stub.py`: Stub for device revocation via xAI-signed certificate.  
- **`hardware/proto/`**: Placeholder for hardware specifications (e.g., fish tank glass, piezo interfaces), to be defined post-prototyping.  

## Usage
1. **Set Intent**: Edit `config/config.json` to declare intent:
   ```json
   {
       "intent": "educational",  // or "commercial"
       "commercial_use": false   // true for commercial intent
   }
   ```
   If missing or invalid, scripts prompt for intent and create a default file. See `tetra/NOTICE.txt`.  
2. **Run Fish Tank Rendering**:
   ```bash
   python3 arch_id.py
   ```
   Requires Keyshot and `fishtank.ksp`. Outputs live renders at 1080x1920, 20 FPS.  
3. **Run Proto Demos**:
   ```bash
   python3 software/proto/ink_sim.py  # Gaze tracking simulation
   python3 software/proto/corneal_etch.py  # Corneal etching simulation
   python3 software/proto/automaton_pie.py  # Piezo interface simulation
   python3 software/proto/kappa.py  # Kappasha256 hashing
   python3 software/proto/clipboard.py  # Clipboard demo
   g++ software/proto/clipboard_undo_redo.cpp -o clipboard_cpp && ./clipboard_cpp
   gcc software/proto/clipboard_undo_redo.c -o clipboard_c && ./clipboard_c
   # Load postcard.frag, grokflat.frag in WebGL browser (e.g., via Three.js)
   open software/proto/index.html
   ```
4. **License**: Open a GitHub issue at github.com/tetrasurfaces/issues for access or licensing (royalty-free for educational use).

## Licensing
Licensed under a dual AGPL-3.0 (software) and Apache 2.0 with xAI amendments (hardware). See `LICENSE.txt`.  
- **Educational Use**: Royalty-free for teaching/research, requires GitHub issue.  
- **Commercial Use**: Requires negotiated approval via github.com/tetrasurfaces/issues.  
- **IP**: xAI owns fish tank IP (gaze-tracking, convex etching, tetra hashing).  
- **Ethics**: Tendon/gaze limits (<20%/30s), revocable for misuse (e.g., surveillance).  
- **Export Controls**: Complies with US EAR Category 5 Part 2.

## Ethics
Every action plants a `nav3d.py` tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces respect tendon/gaze limits. Misuse triggers license revocation via `revocation_stub.py`. Declare intent in `config/config.json` and request licenses via github.com/tetrasurfaces/issues.

## Related Repositories
- **Open Repo**: `tetrasurfaces/tetra` contains `arch_utils.py`, `site_kappa.py`, `tetra_surface.py` for fractal surfaces and construction (xAI copyright).  
- **Private Repo**: `tetrasurfaces/kappashaos` (this repo) will transition to public soon. Contact github.com/tetrasurfaces/issues for access.
