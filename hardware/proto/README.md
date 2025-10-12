# KappashaOS Protofolder

Early prototype. Not for real skin. Yet.

## Overview
The `proto/` folder contains experimental components for KappashaOS, pushing the boundaries of gaze-reactive interfaces and fractal surface integration. These cyberpunk experiments—`ink.rs`, `postcard.frag`, `grokflat.frag`, and `ink_sim.py`—extend the iPhone-shaped fish tank (`arch_id.py`, `fishtank.ksp`) with gaze-tracking pixel arrays and tetra-based etching (Sierpiński triangles/tetrahedrons). Pixels crawl to match gaze, screens pulse green on eye contact, and kappa spirals ensure perspective honesty. These components are part of the broader tetra/kappasha workflow, linking to construction site curvature monitoring (`site_kappa.py`) and CAD integration (SolidWorks, Rhino, Keyshot).

This repository is private, with a planned public release. Access and licensing require a GitHub issue at github.com/tetrasurfaces/issues.

## Components
- **`ink.rs`**: Rust-based simulation of a photolithographic tattoo with 0.2-micron grooves. Features retro-reflective gaze detection and bone conduction audio triggered by green key (matched gaze).  
- **`postcard.frag`**: WebGL shader for multi-user pixel splitting. Renders green for keyed gaze (recognized user), red for unread (unrecognized), supporting up to 5 simultaneous viewers.  
- **`grokflat.frag`**: WebGL shader for flat perspective rendering. Displays a green kappa spiral to maintain visual honesty across viewpoints, eliminating parallax distortion.  
- **`ink_sim.py`**: NumPy-based simulation for multi-user gaze tracking, supporting 5 users with theta spiral patterns, tied to tetra hash generation.  

## Usage
Run demos in a controlled environment:
```bash
# Simulate gaze tracking (requires NumPy, VTK)
python3 proto/ink_sim.py

# Render shaders in browser (requires WebGL-compatible browser)
# Load postcard.frag or grokflat.frag via WebGL framework (e.g., Three.js)
open index.html  # Example WebGL harness
```

Before running, set your intent in `config/config.json`:
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
Every action plants a `nav3d.py` tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces must respect tendon/gaze limits (<20%/30s). Misuse (e.g., harmful applications) triggers license revocation. Operators must declare intent in `config/config.json` and request licenses via github.com/tetrasurfaces/issues.

## Related Repositories
- **Open Repo**: `tetrasurfaces/tetra` contains `arch_utils.py`, `site_kappa.py`, and `tetra_surface.py` for fractal surfaces and construction monitoring (Beau Ayres copyright).  
- **Private Repo**: `tetrasurfaces/kappashaos` includes `arch_id.py` and `fishtank.ksp` for the iPhone-shaped fish tank, with public release pending.
