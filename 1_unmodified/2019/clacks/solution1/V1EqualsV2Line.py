# ==============================================================================
# Scene:      V1EqualsV2Line
# Source:     videos/_2019/clacks/solution1.py (lines 155-165)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl V1EqualsV2Line.py V1EqualsV2Line -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class V1EqualsV2Line(Scene):
    def construct(self):
        line = Line(LEFT, 7 * RIGHT)
        eq = OldTex("v_1", "=", "v_2")
        eq.set_color_by_tex("v_", RED)
        eq.next_to(RIGHT, UR, SMALL_BUFF)
        self.play(
            Write(eq, run_time=1),
            ShowCreation(line),
        )
        self.wait()
