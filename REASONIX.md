# robot-hands-eval — Monorepo

Unmanaged monorepo of independent open-source robotic hand and arm
projects.  No root manifest, build, or test harness — each sub-project
is self-contained.

## Stack

- **Python 3.10+** — primary language for `orca_core`, `LEAP_Hand_Sim`,
  `AHSimulation`, `HandTracking`
- **Rust** — `AmazingHand/Demo/AHControl` binary (Cargo workspace)
- **ROS2 (Humble/Jazzy)** — `openarm_ros2`, `SO-100-arm`,
  `orcahand_description` use `CMakeLists.txt` + `package.xml`
- **Arduino** — `AmazingHand/ArduinoExample/*.ino`
- **CAD** — STEP / STL files under `SO-ARM100/`, `SO-ARM100/Optional/`,
  `AmazingHand/cad/`

## Layout

| Dir | Contents |
| --- | -------- |
| `AmazingHand/` | Full open-source hand: Arduino, Python demos, Rust sim, CAD/STEP, docs |
| `LEAP_Hand_Sim/` | Isaac Gym simulation env + sim2real deployment for LEAP Hand |
| `openarm_description/` | URDF + assets for OpenArm (ROS2 package) |
| `openarm_isaac_lab/` | Isaac Lab RL scripts + source for OpenArm |
| `openarm_ros2/` | ROS2 packages: bringup, hardware interface, MoveIt config |
| `orca_core/` | Python controller for ORCA Hand (Dynamixel, FastAPI, calibration) |
| `orcahand_description/` | URDF/MJCF models for ORCA Hand (v1, v2) |
| `SO-100-arm/` | ROS2 packages for SO-100 arm (URDF, Gazebo, MoveIt2) |
| `SO-ARM100/` | 3D printing files, STEP/STL, URDF for SO-100/101 arms |

## Commands

**`orca_core` (uv-managed):**
```bash
uv sync --group dev          # install + dev deps
uv run pytest tests/         # run tests
uv run python scripts/...    # calibration / demo scripts
```

**`orcahand_description`:**
```bash
pip install pytest mujoco urdf-parser-py
python -m pytest
```

**`AmazingHand/Demo` (Rust):**
```bash
cargo build --release        # builds AHControl binary
```

**`openarm_ros2` (lint):**
```bash
pip install pre-commit && pre-commit run --all-files
```

## Conventions

- **`orca_core`** uses `uv` for dependency management (never bare pip).
- **`orca_core`** tests stub Dynamixel SDK via a fake module in
  `conftest.py` — no real hardware needed.
- **`orca_core`** joint naming: `{finger}_{joint_type}` — e.g.
  `index_mcp`, `thumb_pip`. Fingers: thumb/index/middle/ring/pinky/wrist.
  Joints: mcp/pip/dip/abd.
- **`orca_core`** control modes: `current_based_position` (recommended),
  `position`, `current`, `velocity`.
- **ROS2 packages** follow standard ROS2 layout (`launch/`, `config/`,
  `urdf/`, `src/`, `CMakeLists.txt` + `package.xml`).
- **PRs** target `main`; branch naming `feature/...` or `fix/...`
  (visible in orca_core CLAUDE.md).

## Watch out for

- **Root-level README / manifest don't exist** — there is no top-level
  build, test, or lint command. Always `cd` into the relevant sub-project
  first (e.g. `(cd orca_core && uv run pytest)`).
- **`orca_core` models dir** (`orca_core/models/`) — YAML config files
  define motor-to-joint mapping, ROMs, calibration; hand-editing them
  incorrectly can damage hardware.
- **`LEAP_Hand_Sim`** requires Isaac Gym Preview 4 (NVIDIA, proprietary)
  + Python 3.8 — not installable with standard modern toolchains.
