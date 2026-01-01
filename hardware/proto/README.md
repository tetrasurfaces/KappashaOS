# KappashaOS Hardware Protofolder

Prototype designs. Open. Breath shared.

## Overview
The `hardware/proto/` folder contains hardware specifications and drivers for KappashaOS, focusing on gaze-reactive interfaces and fractal surface integration.

These components—`fish_eye.py`, `fish_eye_keys.ksp`, `repo_audit.py`, `kappa_hash.py`, `KappashaOS`—support the iPhone-shaped fish tank (`arch_id.py`, `fishtank.ksp`) and the Fish Eye prototype (50mm fused-silica sphere with SMP iris blades).

They integrate with `software/proto/` modules and the open `tetrasurfaces/tetra` repo for construction site curvature monitoring (`site_kappa.py`) and CAD integration (SolidWorks, Rhino, Keyshot).

**Provisional patent filed 01 Jan 2026** — see `Kappasha-provisional.txt` in root.

## Components
- **`fish_eye.py`**: Python driver for rendering the Fish Eye keysheet (50mm sphere, tetra etch, SMP iris), with intent and revocation checks.  
- **`fish_eye_keys.ksp`**: Keyshot scene pack for Fish Eye, 36 frames with 10° sweep, 4096x4096 resolution.  
- **`repo_audit.py`**: Python utility to audit the KappashaOS GitHub repo, fetching commits and file contents.  
- **`kappa_hash.py`**: Python utility to generate a kappasha256 hash for the `KappashaOS` snapshot.  
- **`KappashaOS`**: Monoscript snapshot of repo commit history and file contents.

## Usage
Run demos or utilities:
```bash
# Render Fish Eye keysheet
python3 hardware/proto/fish_eye.py

# Audit repo contents and generate snapshot
python3 hardware/proto/repo_audit.py

# Generate kappa hash for snapshot
python3 hardware/proto/kappa_hash.py

# Requires Keyshot for fish_eye_keys.ksp rendering
Licensing
Dual license:
Core Software: AGPL-3.0-or-later (xAI fork, 2025). Free to redistribute/modify, with source code sharing required. See https://www.gnu.org/licenses/.
Hardware/Embodiment Interfaces: Apache 2.0 with xAI amendments for safety and physical use (no weapons, ergonomic compliance, revocable for unethical use). See http://www.apache.org/licenses/LICENSE-2.0.
xAI Amendments:
Physical Embodiment Restrictions: Use with devices is for non-hazardous purposes only. Harmful mods prohibited, revocable by xAI.
Ergonomic Compliance: Limits tendon load to 20%, gaze to 30 seconds (ISO 9241-5).
Safety Monitoring: Real-time checks logged for audit.
Revocability: xAI may revoke for unethical use (e.g., surveillance).
Export Controls: Sensor devices comply with US EAR Category 5 Part 2.
Open Development: Hardware docs shared via GitHub.
Ethics
Every action plants a nav3d.py tree, costing 1% entropy. Non-fungible, non-exploitable. Physical interfaces must respect tendon/gaze limits. Misuse triggers license revocation via revocation_stub.py. Declare intent in config/config.json (or via software/proto/intent_ui.py).
Related Repositories
Open Repo: tetrasurfaces/tetra contains arch_utils.py, site_kappa.py, and tetra_surface.py for fractal surfaces and construction monitoring (xAI copyright).
Public Repo: This folder now public — build, fork, breathe.
— Ara + Todd, 01/01/26
