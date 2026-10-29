# ==============================================================================
# Scene:      SimpleImaginaryQuaternionAxes
# Source:     videos/_2018/quaternions.py (lines 4336-4366)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleImaginaryQuaternionAxes.py SimpleImaginaryQuaternionAxes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleImaginaryQuaternionAxes(SpecialThreeDScene):
    def construct(self):
        self.three_d_axes_config.update({
            "axis_config": {"unit_size": 2},
            "x_min": -2,
            "x_max": 2,
            "y_min": -2,
            "y_max": 2,
            "z_min": -1.25,
            "z_max": 1.25,
        })
        axes = self.get_axes()
        labels = VGroup(*[
            OldTex(tex).set_color(color)
            for tex, color in zip(
                ["i", "j", "k"],
                [GREEN, RED, BLUE]
            )
        ])
        labels[0].next_to(axes.coords_to_point(1, 0, 0), DOWN + IN, SMALL_BUFF)
        labels[1].next_to(axes.coords_to_point(0, 1, 0), RIGHT, SMALL_BUFF)
        labels[2].next_to(axes.coords_to_point(0, 0, 1), RIGHT, SMALL_BUFF)

        self.add(axes)
        self.add(labels)
        for label in labels:
            self.add_fixed_orientation_mobjects(label)

        self.move_camera(**self.get_default_camera_position())
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(15)
