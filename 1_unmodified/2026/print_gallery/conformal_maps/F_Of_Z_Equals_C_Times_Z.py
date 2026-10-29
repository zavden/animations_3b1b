# ==============================================================================
# Scene:      F_Of_Z_Equals_C_Times_Z
# Source:     videos/_2026/print_gallery/conformal_maps.py (lines 458-465)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl F_Of_Z_Equals_C_Times_Z.py F_Of_Z_Equals_C_Times_Z -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class F_Of_Z_Equals_C_Times_Z(InteractiveScene):
    def construct(self):
        f_of_z = Tex(
            r"f(z) = c \cdot z",
            tex_to_color_map={"f": PINK, "z": YELLOW, "c": GREEN},
            font_size=150
        )
        self.play(Write(f_of_z), run_time=2)
