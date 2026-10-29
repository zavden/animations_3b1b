# ==============================================================================
# Scene:      RoleOfCalculus
# Source:     videos/_2018/sphere_area.py (lines 2415-2450)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RoleOfCalculus.py RoleOfCalculus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RoleOfCalculus(SpecialThreeDScene):
    CONFIG = {
        "camera_config": {
            "light_source_start_point": [-4, 5, 7],
        }
    }

    def construct(self):
        calc = OldTex("\\int", "\\int")
        calc.space_out_submobjects(0.4)
        calc.scale(2)
        arrow = Vector(2 * RIGHT, color=WHITE)
        sphere = self.get_sphere()
        sphere.rotate(70 * DEGREES, axis=LEFT)

        group = VGroup(calc, arrow, sphere)
        group.arrange(RIGHT)
        group.shift(0.5 * RIGHT)
        cross = Cross(group[:2], stroke_width=10)

        # arrow2 = arrow.copy()

        self.add(calc, arrow)
        self.play(Write(sphere))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            sphere.next_to, ORIGIN, LEFT, 1.0,
            arrow.move_to, ORIGIN, LEFT,
            calc.next_to, ORIGIN, RIGHT, 2.25,
            FadeOut(cross),
            path_arc=PI,
            run_time=2,
        )
        self.wait()
