# ==============================================================================
# Scene:      AmbientChangingDots
# Source:     videos/_2024/transformers/supplements.py (lines 1574-1590)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AmbientChangingDots.py AmbientChangingDots -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AmbientChangingDots(InteractiveScene):
    def construct(self):
        # Test
        dots = Dot().get_grid(20, 30)
        dots.set_height(8)
        dots.set_fill(opacity=0.5)
        dots.phases = np.random.uniform(0, TAU, len(dots))
        dots.freqs = np.random.uniform(0.3, 0.8, len(dots))

        def update_dots(dots):
            for dot, phase, freq in zip(dots, dots.phases, dots.freqs):
                dot.set_fill(opacity=np.cos(phase + freq * self.time)**2)
            return dots

        dots.add_updater(update_dots)
        self.add(dots)
        self.wait(30)
