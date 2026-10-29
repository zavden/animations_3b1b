# ==============================================================================
# Scene:      CurrentAverageFees
# Source:     videos/_2017/crypto.py (lines 4907-4919)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CurrentAverageFees.py CurrentAverageFees -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CurrentAverageFees(Scene):
    def construct(self):
        fees = OldTexText(
            "Current average fees: ",
            "$\\sim 0.0013$ BTC", 
            "$\\approx$", "\\$3.39"
        )
        fees.set_color_by_tex("BTC", YELLOW)
        fees.set_color_by_tex("\\$", GREEN)
        fees.to_edge(UP)

        self.play(Write(fees))
        self.wait()
