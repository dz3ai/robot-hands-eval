# robot lab — evaluation of open source robot hands

Unmanaged monorepo of independent open-source robotic hand and arm projects. Each sub-project is self-contained (no root build/test harness).

## Projects

| Directory | What it is | Tech |
|-----------|-----------|------|
| `AmazingHand/` | Full open-source dexterous hand — Arduino firmware, Python demos, Rust simulation, CAD/STEP files | Arduino, Python, Rust, CAD |
| `LEAP_Hand_Sim/` | Isaac Gym simulation env + sim2real for LEAP Hand (arXiv 2309.06440) | Python (Isaac Gym, PyTorch) |
| `openarm_description/` | URDF + assets for OpenArm (ROS2 description package) | ROS2, URDF |
| `openarm_isaac_lab/` | Isaac Lab RL training scripts for OpenArm | Python (Isaac Lab) |
| `openarm_ros2/` | Full ROS2 stack — bringup, hardware interface, MoveIt2 config | ROS2, C++ |
| `orca_core/` | ORCA Hand Python controller — Dynamixel SDK, FastAPI API, calibration tools | Python 3.10+, uv |
| `orcahand_description/` | URDF + MuJoCo MJCF models for ORCA Hand (v1, v2) | MuJoCo, ROS2 |
| `SO-100-arm/` | ROS2 support for SO-100 5-DOF arm (URDF, Gazebo, MoveIt2) | ROS2, Gazebo |
| `SO-ARM100/` | 3D printing files, STEP/STL, and URDF for SO-100/101 arms | CAD, 3D printing |

## The web app (planned)
- Project showcase
- Feature comparison
- Simulators

## The physical lab
- 3D printing parts (see [docs/printed-parts-checklist.md](docs/printed-parts-checklist.md))
- Full assembly — sensors, servos, structure
- Controller programming (Python / ROS2 / Arduino)

## AI-driven benchmarks (planned)
- Policy deployment on physical hardware
- Sim-to-real transfer
- Dexterous manipulation evaluation

---

## Quick start

### ORCA Hand (Python, simulator first)

```bash
cd orcahand_description
uv pip install mujoco
uv run python -m mujoco.viewer --mjcf=v2/scene_combined.xml
```

### ORCA Hand (calibration on real hardware)

```bash
cd orca_core
uv sync --group dev
uv run python scripts/tension.py orca_core/models/v2/orcahand_right
uv run python scripts/calibrate.py orca_core/models/v2/orcahand_right
uv run python scripts/neutral.py orca_core/models/v2/orcahand_right
```

### SO-100 arm simulation

```bash
cd SO-100-arm/so_arm_100_description
# requires ROS2 Humble/Jazzy + Gazebo
colcon build
ros2 launch so_arm_100_description view_robot.launch.py
```

### AmazingHand Rust simulation

```bash
cd AmazingHand/Demo
cargo build --release
```

## Conventions

- **`orca_core`** uses `uv` for Python dependency management (never bare pip).
- Joint naming in `orca_core`: `{finger}_{joint}` — e.g. `index_mcp`, `thumb_pip`. Fingers: thumb/index/middle/ring/pinky/wrist. Joints: mcp/pip/dip/abd.
- ROS2 packages follow standard ROS2 layout (`launch/`, `config/`, `urdf/`, `src/`, `CMakeLists.txt` + `package.xml`).
- PRs target `main`; branches named `feature/...` or `fix/...`.

## Notes

- **No root-level commands** — always `cd` into the relevant sub-project first.
- **`orca_core` models** (`orca_core/models/v1/`, `v2/`) — YAML defines motor-to-joint mapping, ROMs, calibration. Incorrect edits can damage hardware.
- **`LEAP_Hand_Sim`** requires Isaac Gym Preview 4 (NVIDIA, proprietary) + Python 3.8 — not installable with standard modern toolchains.
 