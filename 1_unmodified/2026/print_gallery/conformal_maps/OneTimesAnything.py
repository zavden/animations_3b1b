# ==============================================================================
# Scene:      OneTimesAnything
# Source:     videos/_2026/print_gallery/conformal_maps.py (lines 479-487)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneTimesAnything.py OneTimesAnything -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class OneTimesAnything(InteractiveScene):
    def construct(self):
        # Write 1*c = c
        oneTimesC = Tex(
            r"1 \cdot c = {c}",
            tex_to_color_map={"1": YELLOW, "c": GREEN, "{c}": PINK},
            font_size=150
        )
        self.play(Write(oneTimesC), run_time=2)
