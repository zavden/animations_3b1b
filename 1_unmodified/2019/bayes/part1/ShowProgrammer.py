# ==============================================================================
# Scene:      ShowProgrammer
# Source:     videos/_2019/bayes/part1.py (lines 4576-4592)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowProgrammer.py ShowProgrammer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowProgrammer(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E,
        }
    }

    def construct(self):
        programmer = SVGMobject(file_name="programmer")
        programmer.set_stroke(width=0)
        programmer.set_fill(GREY, 1)
        programmer.set_sheen(1, UL)
        programmer.set_height(3)

        programmer.to_corner(DL)
        self.play(FadeIn(programmer, DOWN))
        self.wait()
