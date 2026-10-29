# ==============================================================================
# Scene:      PassingFlashes
# Source:     videos/_2026/2025_P6/p6.py (lines 3722-3727)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PassingFlashes.py PassingFlashes -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

class PassingFlashes(InteractiveScene):
    def construct(self):
        # Do some passing flashes
        self.play(VShowPassingFlash(Rectangle(width=4, height=1, stroke_width=4, stroke_color=YELLOW).insert_n_curves(100), time_width=3), run_time=4)
        self.wait(1)
        self.play(VShowPassingFlash(Rectangle(width=4.5, height=1, stroke_width=4, stroke_color=YELLOW).insert_n_curves(100), time_width=3), run_time=4)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
