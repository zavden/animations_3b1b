# ==============================================================================
# Scene:      LISEqualsK
# Source:     videos/_2026/2025_P6/p6.py (lines 3678-3693)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LISEqualsK.py LISEqualsK -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

class LISEqualsK(InteractiveScene):
    def construct(self):
        # Write the equation
        increasing_sequence_color = GREEN_D
        k_color = TEAL
        equation = Tex(
            R"\text{LIS} = 3 = k", font_size=70, tex_to_color_map={"LIS": increasing_sequence_color, "k": k_color}
        ).to_edge(RIGHT, buff=1)
        self.play(Write(equation), run_time=2)
        self.wait(2)

        # Generalize
        generalized_equation = Tex(
            R"\text{LIS} = k", font_size=70, tex_to_color_map={"LIS": increasing_sequence_color, "k": k_color}
        ).move_to(equation)
        self.play(TransformMatchingShapes(equation, generalized_equation))


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
