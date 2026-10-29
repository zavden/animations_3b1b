# ==============================================================================
# Scene:      ZeroTimesAnything
# Source:     videos/_2026/print_gallery/conformal_maps.py (lines 468-476)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ZeroTimesAnything.py ZeroTimesAnything -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ZeroTimesAnything(InteractiveScene):
    def construct(self):
        # Write 0*c = 0
        zeroTimesC = Tex(
            r"0 \cdot c = {0}",
            tex_to_color_map={"0": YELLOW, "c": GREEN, "{0}": PINK},
            font_size=150
        )
        self.play(Write(zeroTimesC), run_time=2)
