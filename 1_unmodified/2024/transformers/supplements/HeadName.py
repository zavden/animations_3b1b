# ==============================================================================
# Scene:      HeadName
# Source:     videos/_2024/transformers/supplements.py (lines 1191-1204)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HeadName.py HeadName -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HeadName(InteractiveScene):
    def construct(self):
        # Test
        title = Text("One head of attention", font_size=72)
        title.to_edge(UP)
        head = title["head"][0]
        self.play(
            Write(title, run_time=1)
        )
        self.play(
            FlashAround(head, time_width=2, run_time=2),
            head.animate.set_color(YELLOW),
        )
        self.wait()
