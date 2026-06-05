"""ORCA Hand MuJoCo animation script.

Defines poses, interpolation, and rendering for the right ORCA Hand.
"""

import pathlib
import time

import mujoco
import numpy as np

# ── 17 actuator names (right hand) ──
ACTUATORS = [
    "right_wrist",
    "right_p-abd", "right_p-mcp", "right_p-pip",
    "right_r-abd", "right_r-mcp", "right_r-pip",
    "right_m-abd", "right_m-mcp", "right_m-pip",
    "right_i-abd", "right_i-mcp", "right_i-pip",
    "right_t-cmc", "right_t-abd", "right_t-mcp", "right_t-pip",
]

# MJCF path relative to repo root
_HERE = pathlib.Path(__file__).resolve().parent
MJCF_PATH = str(_HERE.parent / "orcahand_description" / "v2" / "scene_combined.xml")


# ── Poses (radians) ──
# Each value within MJCF ctrlrange. Positive = flexion / abduction.
# NOTE: keys must include the `_actuator` suffix to match MJCF naming.

_act = lambda n: n + "_actuator"

home = {_act(a): 0.0 for a in ACTUATORS}



open_ = {
    _act("right_wrist"):    0.0,
    _act("right_p-abd"):    0.0,   _act("right_p-mcp"): -0.3,   _act("right_p-pip"): -0.2,
    _act("right_r-abd"):    0.0,   _act("right_r-mcp"): -0.3,   _act("right_r-pip"): -0.2,
    _act("right_m-abd"):    0.0,   _act("right_m-mcp"): -0.3,   _act("right_m-pip"): -0.2,
    _act("right_i-abd"):    0.0,   _act("right_i-mcp"): -0.3,   _act("right_i-pip"): -0.2,
    _act("right_t-cmc"):    0.0,   _act("right_t-abd"):  0.0,   _act("right_t-mcp"): -0.3,   _act("right_t-pip"): -0.2,
}

fist = {
    _act("right_wrist"):    0.0,
    _act("right_p-abd"):    0.0,   _act("right_p-mcp"):  1.7,   _act("right_p-pip"):  1.8,
    _act("right_r-abd"):    0.0,   _act("right_r-mcp"):  1.7,   _act("right_r-pip"):  1.8,
    _act("right_m-abd"):    0.0,   _act("right_m-mcp"):  1.7,   _act("right_m-pip"):  1.8,
    _act("right_i-abd"):    0.0,   _act("right_i-mcp"):  1.7,   _act("right_i-pip"):  1.8,
    _act("right_t-cmc"):    0.3,   _act("right_t-abd"):  0.3,   _act("right_t-mcp"):  1.5,   _act("right_t-pip"):  1.5,
}

point = {
    _act("right_wrist"):    0.0,
    _act("right_p-abd"):    0.0,   _act("right_p-mcp"):  1.7,   _act("right_p-pip"):  1.8,
    _act("right_r-abd"):    0.0,   _act("right_r-mcp"):  1.7,   _act("right_r-pip"):  1.8,
    _act("right_m-abd"):    0.0,   _act("right_m-mcp"):  1.7,   _act("right_m-pip"):  1.8,
    _act("right_i-abd"):    0.0,   _act("right_i-mcp"): -0.3,   _act("right_i-pip"): -0.2,
    _act("right_t-cmc"):    0.3,   _act("right_t-abd"):  0.3,   _act("right_t-mcp"):  1.5,   _act("right_t-pip"):  1.5,
}

pinch = {
    _act("right_wrist"):    0.0,
    _act("right_p-abd"):    0.0,   _act("right_p-mcp"):  1.7,   _act("right_p-pip"):  1.8,
    _act("right_r-abd"):    0.0,   _act("right_r-mcp"):  1.7,   _act("right_r-pip"):  1.8,
    _act("right_m-abd"):    0.0,   _act("right_m-mcp"):  1.7,   _act("right_m-pip"):  1.8,
    _act("right_i-abd"):    0.0,   _act("right_i-mcp"):  0.8,   _act("right_i-pip"):  1.0,
    _act("right_t-cmc"):    0.3,   _act("right_t-abd"):  0.5,   _act("right_t-mcp"):  0.8,   _act("right_t-pip"):  1.0,
}

spread = {
    _act("right_wrist"):    0.0,
    _act("right_p-abd"):    0.5,   _act("right_p-mcp"):  0.0,   _act("right_p-pip"):  0.0,
    _act("right_r-abd"):    0.3,   _act("right_r-mcp"):  0.0,   _act("right_r-pip"):  0.0,
    _act("right_m-abd"):    0.0,   _act("right_m-mcp"):  0.0,   _act("right_m-pip"):  0.0,
    _act("right_i-abd"):   -0.3,   _act("right_i-mcp"):  0.0,   _act("right_i-pip"):  0.0,
    _act("right_t-cmc"):    0.0,   _act("right_t-abd"):  0.0,   _act("right_t-mcp"):  0.0,   _act("right_t-pip"):  0.0,
}

# Alias: the test imports `mod.open` but `open` is a Python keyword
open = open_

# ── Interpolation ──

def lerp_poses(pose_a: dict, pose_b: dict, n_frames: int) -> list[dict]:
    """Linearly interpolate between two poses over *n_frames* frames."""
    if n_frames < 1:
        return []
    if n_frames == 1:
        return [dict(pose_b)]

    keys = list(pose_a.keys())
    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        frame = {}
        for k in keys:
            frame[k] = pose_a[k] + t * (pose_b[k] - pose_a[k])
        frames.append(frame)
    return frames


# ── Sequence builder ──

def build_sequence(frames_per_transition: int = 10) -> list[dict]:
    """Build a full animation sequence: open → fist → point → pinch → spread → home."""
    seq = []
    transitions = [
        (home, open_),
        (open_, fist),
        (fist, point),
        (point, pinch),
        (pinch, spread),
        (spread, home),
    ]
    for a, b in transitions:
        seq.extend(lerp_poses(a, b, frames_per_transition))
    return seq


# ── Model loading ──

_model_cache: tuple = (None, None)  # (model, data)


def load_model(mjcf_path: str | None = None):
    """Load MuJoCo model. Returns just the model (for test compatibility)."""
    path = mjcf_path or MJCF_PATH
    model = mujoco.MjModel.from_xml_path(path)
    return model


# ── Rendering ──

_renderer_cache = None


def _get_renderer(model, width=640, height=480):
    global _renderer_cache
    if _renderer_cache is None:
        _renderer_cache = mujoco.Renderer(model, width=width, height=height)
    return _renderer_cache


def render_frame(pose: dict, width=640, height=480) -> np.ndarray:
    """Set the hand to *pose*, take one render, return RGB array (H, W, 3)."""
    model = load_model()
    data = mujoco.MjData(model)
    for act_name, value in pose.items():
        actuator_id = model.actuator(act_name).id
        joint_qpos_adr = model.jnt_qposadr[model.actuator(act_name).trnid[0]]
        data.qpos[joint_qpos_adr] = value

    mujoco.mj_forward(model, data)

    renderer = _get_renderer(model, width, height)
    renderer.update_scene(data)
    return renderer.render()


def render_sequence(seq: list[dict], out_dir: str = "frames") -> str:
    """Render each frame in *seq* to PNG in *out_dir*. Returns out_dir path."""
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i, pose in enumerate(seq):
        img = render_frame(pose)
        # Save as PNG via PIL or imageio
        import imageio.v3 as iio

        iio.imwrite(str(out / f"frame_{i:04d}.png"), img)
    return str(out)


# ── CLI entry point ──

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Animate ORCA Hand in MuJoCo")
    parser.add_argument("--frames", type=int, default=10, help="Frames per transition")
    parser.add_argument("--out", type=str, default="frames", help="Output directory")
    parser.add_argument("--viewer", action="store_true", help="Open interactive viewer instead")
    args = parser.parse_args()

    if args.viewer:
        model = load_model()
        data = mujoco.MjData(model)
        mujoco.viewer.launch(model, data)
        return

    seq = build_sequence(args.frames)
    print(f"Rendering {len(seq)} frames to {args.out}/ ...")
    t0 = time.perf_counter()
    out_dir = render_sequence(seq, args.out)
    elapsed = time.perf_counter() - t0
    print(f"Done in {elapsed:.1f}s → {out_dir}/")

    # Optionally compose video with ffmpeg
    fps = 30
    video_path = f"{out_dir}/animation.mp4"
    import subprocess
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(fps),
        "-i", f"{out_dir}/frame_%04d.png",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        video_path,
    ], capture_output=True)
    print(f"Video → {video_path}")


if __name__ == "__main__":
    main()
