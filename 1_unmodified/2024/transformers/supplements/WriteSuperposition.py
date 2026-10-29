# ==============================================================================
# Scene:      WriteSuperposition
# Source:     videos/_2024/transformers/supplements.py (lines 2023-2041)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteSuperposition.py WriteSuperposition -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WriteSuperposition(InteractiveScene):
    def construct(self):
        # Test
        word = Text("Superposition", font_size=120)
        outline = word.copy()
        outline.set_stroke(TEAL, 3)
        outline.set_fill(opacity=0)

        self.play(
            FadeIn(word, lag_ratio=0.1),
            LaggedStartMap(
                VShowPassingFlash,
                outline,
                time_width=2,
                run_time=5,
                lag_ratio=0.01
            )
        )
        self.wait()
