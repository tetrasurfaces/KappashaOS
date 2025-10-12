# KappashaOS

Experimental platform for gaze-reactive interfaces and fractal surface integration, powering the iPhone-shaped fish tank and related prototypes. This repository is private, with a planned public release. It extends the tetra/kappasha workflow (Sierpiński triangles/tetrahedrons, kappasha256 hashing) from the open `tetrasurfaces/tetra` repo, focusing on industrial design (Keyshot rendering, gaze-tracking pixels) and cyberpunk experiments.

## Overview
KappashaOS drives the iPhone-shaped fish tank—a 0.7mm convex glass device with tetra-etched surfaces (15-micron depth at crown, 5-micron at edge), gaze-tracking pixel arrays, and a 60ml water volume with micro-bubble system. The `proto/` folder contains experimental components for gaze-reactive shaders and simulations, pushing the boundaries of human-device interaction. All components integrate with `tetrasurfaces/tetra`’s core utilities for fractal surfaces and construction monitoring.

## Components
- **`arch_id.py`**: Python script for live Keyshot rendering of the fish tank, applying tetra hashes and dynamic bump maps for gaze-reactive etching.  
- **`fishtank.ksp`**: Keyshot scene file (placeholder) for the fish tank, with convex glass, water volume, and gaze-tracking animations.  
- **`proto/`**: Experimental folder with:  
  - `ink.rs`: Rust-based photolithographic tattoo sim (0.2-micron grooves, gaze detection).  
  - `postcard.frag`: WebGL shader for multi-user pixel splitting (green/red based on gaze).  
  - `grokflat.frag`: WebGL shader for flat perspective with green kappa spiral.  
  - `ink_sim.py`: NumPy-based gaze tracking sim for 5 users with theta spiral patterns.  

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
   python3 proto/ink_sim.py  # Gaze tracking simulation
   # Load postcard.frag, grokflat.frag in WebGL browser (e.g., via Three.js)
   open proto/index.html
   ```
4. **License**: Open a GitHub issue at github.com/tetrasurfaces/issues for access or licensing (royalty-free for educational use).

## Licensing
Licensed under a dual AGPL-3.0 (software) and Apache 2.0 with xAI amendments (hardware). See `LICENSE.txt`.  
- **Educational Use**: Royalty-free for teaching/research, requires GitHub issue.  
- **Commercial Use**: Requires negotiated approval via github.com/tetrasurfaces/issues.  
- **IP**: xAI owns fish tank IP (gaze-tracking, convex etching).  
- **Ethics**: Tendon/gaze limits (<20%/30s), revocable for misuse (e.g., surveillance).  
- **Export Controls**: Complies with US EAR Category 5 Part 2.

## Ethics
Every action plants a `nav3d.py` tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces respect tendon/gaze limits. Misuse triggers license revocation. Declare intent in `config/config.json` and request licenses via github.com/tetrasurfaces/issues.

## Related Repositories
- **Open Repo**: `tetrasurfaces/tetra` contains `arch_utils.py`, `site_kappa.py`, `tetra_surface.py` for fractal surfaces and construction (Tetrasurfaces copyright).  
- **Private Repo**: `tetrasurfaces/kappashaos` (this repo) will transition to public soon. Contact github.com/tetrasurfaces/issues for access.
