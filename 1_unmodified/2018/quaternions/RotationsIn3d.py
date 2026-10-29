# ==============================================================================
# Scene:      RotationsIn3d
# Source:     videos/_2018/quaternions.py (lines 501-533)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationsIn3d.py RotationsIn3d -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RotationsIn3d(SpecialThreeDScene):
    def construct(self):
        self.set_camera_orientation(**self.get_default_camera_position())
        self.begin_ambient_camera_rotation(rate=0.02)
        sphere = self.get_sphere()
        vectors = VGroup(*[
            Vector(u * v, color=color).next_to(sphere, u * v, buff=0)
            for v, color in zip(
                [RIGHT, UP, OUT],
                [GREEN, RED, BLUE],
            )
            for u in [-1, 1]
        ])
        vectors.set_shade_in_3d(True)
        sphere.add(vectors)

        self.add(self.get_axes())
        self.add(sphere)
        angle_axis_pairs = [
            (90 * DEGREES, RIGHT),
            (120 * DEGREES, UR),
            (-45 * DEGREES, OUT),
            (60 * DEGREES, IN + DOWN),
            (90 * DEGREES, UP),
            (30 * DEGREES, UP + OUT + RIGHT),
        ]
        for angle, axis in angle_axis_pairs:
            self.play(Rotate(
                sphere, angle,
                axis=axis,
                run_time=2,
            ))
            self.wait()
