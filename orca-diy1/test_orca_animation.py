"""Tests for ORCA Hand MuJoCo animation script.

POSE = dict of {actuator_name: target_radians}
Right hand has 17 actuators (16 fingers + 1 wrist).
"""

import json
import importlib.util
import pathlib

import numpy as np
import pytest

# Path to the implementation we're about to write
SCRIPT_PATH = pathlib.Path(__file__).parent / "orca_animate.py"

# Poses that the script should define
EXPECTED_POSES = [
    "home",       # all joints at 0
    "open",       # full extension
    "fist",       # full curl
    "point",      # index extended, others curled
    "pinch",      # thumb + index tip close
    "spread",     # all fingers abducted
]

# Right hand actuator names from MJCF
RIGHT_ACTUATORS = [
    "right_wrist",
    "right_p-abd", "right_p-mcp", "right_p-pip",
    "right_r-abd", "right_r-mcp", "right_r-pip",
    "right_m-abd", "right_m-mcp", "right_m-pip",
    "right_i-abd", "right_i-mcp", "right_i-pip",
    "right_t-cmc", "right_t-abd", "right_t-mcp", "right_t-pip",
]

# (name, min_rad, max_rad) from MJCF ctrlrange — with _actuator suffix
JOINT_LIMITS: dict[str, tuple[float, float]] = {
    "right_wrist_actuator":   (-1.1345, 0.6109),
    "right_p-abd_actuator":   (-0.5236, 0.5236),
    "right_p-mcp_actuator":   (-0.4363, 1.7453),
    "right_p-pip_actuator":   (-0.2618, 1.8675),
    "right_r-abd_actuator":   (-0.4712, 0.4712),
    "right_r-mcp_actuator":   (-0.4363, 1.7453),
    "right_r-pip_actuator":   (-0.2618, 1.8675),
    "right_m-abd_actuator":   (-0.4712, 0.4712),
    "right_m-mcp_actuator":   (-0.4363, 1.7453),
    "right_m-pip_actuator":   (-0.2618, 1.8675),
    "right_i-abd_actuator":   (-0.4363, 0.5236),
    "right_i-mcp_actuator":   (-0.4363, 1.7453),
    "right_i-pip_actuator":   (-0.2618, 1.8675),
    "right_t-cmc_actuator":   (-0.7854, 0.5760),
    "right_t-abd_actuator":   (-0.3142, 0.9599),
    "right_t-mcp_actuator":   (-0.4363, 1.7453),
    "right_t-pip_actuator":   (-0.2618, 1.8675),
}


# ── Helpers ──

def load_script_module():
    """Lazy-import the animation script so tests can inspect its constants."""
    if not SCRIPT_PATH.exists():
        pytest.skip(f"{SCRIPT_PATH} not yet written")
    spec = importlib.util.spec_from_file_location("orca_animate", SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Tests ──

class TestPoseDefinitions:
    """Every expected pose must exist, have the right joint count, and respect limits."""

    def test_all_expected_poses_defined(self):
        mod = load_script_module()
        for name in EXPECTED_POSES:
            assert hasattr(mod, name), f"Pose '{name}' not defined in orca_animate.py"

    def test_each_pose_has_17_joints(self):
        mod = load_script_module()
        for name in EXPECTED_POSES:
            pose: dict = getattr(mod, name)
            assert isinstance(pose, dict), f"Pose '{name}' should be a dict"
            assert len(pose) == 17, (
                f"Pose '{name}' has {len(pose)} joints, expected 17"
            )

    def test_each_pose_uses_valid_actuator_names(self):
        mod = load_script_module()
        valid = {a + "_actuator" for a in RIGHT_ACTUATORS}
        for name in EXPECTED_POSES:
            pose: dict = getattr(mod, name)
            for key in pose:
                assert key in valid, (
                    f"Pose '{name}' has unknown actuator '{key}'"
                )

    def test_each_pose_value_within_limits(self):
        mod = load_script_module()
        for name in EXPECTED_POSES:
            pose: dict = getattr(mod, name)
            for act, val in pose.items():
                lo, hi = JOINT_LIMITS[act]
                assert lo <= val <= hi, (
                    f"Pose '{name}', joint '{act}': {val:.4f} rad "
                    f"outside [{lo:.4f}, {hi:.4f}]"
                )


class TestInterpolation:
    """Linear interpolation between two poses produces valid intermediate frames."""

    def test_lerp_home_to_fist(self):
        mod = load_script_module()
        n_frames = 10
        frames = mod.lerp_poses(mod.home, mod.fist, n_frames)
        assert len(frames) == n_frames, f"Expected {n_frames} frames, got {len(frames)}"
        # First frame = home
        for act_key in mod.home:
            assert frames[0][act_key] == pytest.approx(mod.home[act_key])
        # Last frame = fist
        for act_key in mod.fist:
            assert frames[-1][act_key] == pytest.approx(mod.fist[act_key])
        # Middle frames are interpolated (not equal to either end)
        mid = frames[n_frames // 2]
        assert mid != frames[0]
        assert mid != frames[-1]

    def test_lerp_respects_limits(self):
        mod = load_script_module()
        frames = mod.lerp_poses(mod.open, mod.fist, 20)
        for frame in frames:
            for act, val in frame.items():
                lo, hi = JOINT_LIMITS[act]
                assert lo <= val <= hi + 1e-6, (
                    f"Interpolated value {act}={val:.4f} "
                    f"outside [{lo:.4f}, {hi:.4f}]"
                )

    def test_lerp_single_frame(self):
        mod = load_script_module()
        frames = mod.lerp_poses(mod.home, mod.fist, 1)
        assert len(frames) == 1
        assert frames[0] == mod.fist

    def test_lerp_same_pose(self):
        mod = load_script_module()
        frames = mod.lerp_poses(mod.home, mod.home, 5)
        for frame in frames:
            assert frame == mod.home


class TestAnimationSequence:
    """Full animation sequence produces expected number of frames."""

    def test_build_sequence_returns_list_of_frames(self):
        mod = load_script_module()
        seq = mod.build_sequence()
        assert isinstance(seq, list)
        assert len(seq) > 0
        for frame in seq:
            assert isinstance(frame, dict)
            assert len(frame) == 17

    def test_every_frame_in_sequence_valid(self):
        mod = load_script_module()
        seq = mod.build_sequence()
        for i, frame in enumerate(seq):
            for act, val in frame.items():
                assert act in JOINT_LIMITS, f"Frame {i}: unknown joint '{act}'"
                lo, hi = JOINT_LIMITS[act]
                assert lo <= val <= hi + 1e-6, (
                    f"Frame {i}: {act}={val:.4f} outside [{lo:.4f}, {hi:.4f}]"
                )


class TestModelLoading:
    """MuJoCo model can be loaded from the MJCF path."""

    def test_model_loads(self):
        mod = load_script_module()
        model = mod.load_model()
        assert model is not None
        # scene_combined has both hands: 34 actuators, 34 joint qpos
        assert model.nu == 34
        assert model.nq > 0


class TestRender:
    """Render function produces frames correctly."""

    def test_render_frame_returns_array(self):
        mod = load_script_module()
        frame = mod.render_frame(mod.home)
        assert isinstance(frame, np.ndarray)
        # Typical MuJoCo RGB render: (height, width, 3)
        assert frame.ndim == 3
        assert frame.shape[2] == 3

    def test_render_sequence_saves_frames(self, tmp_path):
        mod = load_script_module()
        seq = mod.build_sequence()[:5]  # just 5 frames for speed
        out_dir = mod.render_sequence(seq, out_dir=str(tmp_path))
        rendered = sorted(pathlib.Path(out_dir).glob("frame_*.png"))
        assert len(rendered) == len(seq), (
            f"Expected {len(seq)} frames, got {len(rendered)}"
        )
