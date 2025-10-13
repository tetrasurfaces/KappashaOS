# KappashaOS Hardware Protofolder

Early prototype designs. Not for production yet.

## Overview
The `hardware/proto/` folder contains experimental hardware specifications and drivers for KappashaOS, focusing on gaze-reactive interfaces and fractal surface integration. These components—`fish_eye.py`, `fish_eye_keys.ksp`, `repo_audit.py`—support the iPhone-shaped fish tank (`arch_id.py`, `fishtank.ksp`) and the Fish Eye prototype (50mm fused-silica sphere with SMP iris blades). They integrate with the `software/proto/` modules and the open `tetrasurfaces/tetra` repo for construction site curvature monitoring (`site_kappa.py`) and CAD integration (SolidWorks, Rhino, Keyshot).

This repository is private, with a planned public release. Access and licensing require a GitHub issue at github.com/tetrasurfaces/issues.

## Components
- **`fish_eye.py`**: Python driver for rendering the Fish Eye keysheet (50mm sphere, tetra etch, SMP iris), with intent and revocation checks.  
- **`fish_eye_keys.ksp`**: Keyshot scene pack for Fish Eye, 36 frames with 10° sweep, 4096x4096 resolution, for rendering and export.  
- **`repo_audit.py`**: Python utility to audit the KappashaOS GitHub repo, fetching commits and file contents with intent and revocation checks.  

## Usage
Run demos or utilities in a controlled environment:
```bash
# Render Fish Eye keysheet
python3 hardware/proto/fish_eye.py

# Audit repo contents
python3 hardware/proto/repo_audit.py

# Requires Keyshot for fish_eye_keys.ksp rendering
```

Before running, set your intent in `config/config.json` (or use `software/proto/intent_ui.py`):
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
1. **Physical Embodiment Restrictions**: Use with devices (e.g., fish tank glass, Fish Eye sphere) is for non-hazardous purposes only. Harmful mods are prohibited, revocable by xAI.  
2. **Ergonomic Compliance**: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5) for physical interfaces; waived for software-only use.  
3. **Safety Monitoring**: Real-time checks (e.g., heat dissipation) logged for audit.  
4. **Revocability**: xAI may revoke for unethical use (e.g., surveillance).  
5. **Export Controls**: Sensor devices comply with US EAR Category 5 Part 2.  
6. **Educational Use**: Royalty-free for teaching/research, requires GitHub issue at github.com/tetrasurfaces/issues.  
7. **Intellectual Property**: xAI owns IP for gaze-tracking pixel arrays, convex glass etching (0.7mm arc), and tetra hash integration.  

**Private Development Note**: This repository (`tetrasurfaces/kappashaos`) is private, with a planned public release. Access is restricted. Open a GitHub issue at github.com/tetrasurfaces/issues for licensing or access.

## Ethics
Every action plants a `nav3d.py` tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces must respect tendon/gaze limits (<20%/30s). Misuse (e.g., harmful applications) triggers license revocation via `revocation_stub.py`. Operators must declare intent in `config/config.json` (or via `software/proto/intent_ui.py`) and request licenses via github.com/tetrasurfaces/issues.

## Related Repositories
- **Open Repo**: `tetrasurfaces/tetra` contains `arch_utils.py`, `site_kappa.py`, and `tetra_surface.py` for fractal surfaces and construction monitoring (xAI copyright).  
- **Private Repo**: `tetrasurfaces/kappashaos` includes `arch_id.py`, `fishtank.ksp`, `hardware/proto/`, and `software/proto/` for the fish tank, Fish Eye, and experimental components, with public release pending.
