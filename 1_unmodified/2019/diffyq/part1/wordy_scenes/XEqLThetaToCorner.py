# ==============================================================================
# Scene:      XEqLThetaToCorner
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 111-123)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl XEqLThetaToCorner.py XEqLThetaToCorner -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class XEqLThetaToCorner(Scene):
    def construct(self):
        equation = OldTex(
            "x = L\\theta",
            tex_to_color_map={
                "x": GREEN,
                "\\theta": BLUE,
            }
        )
        equation.move_to(DOWN + 3 * RIGHT)
        self.add(equation)
        self.play(equation.to_corner, DL, {"buff": LARGE_BUFF})
        self.wait()
