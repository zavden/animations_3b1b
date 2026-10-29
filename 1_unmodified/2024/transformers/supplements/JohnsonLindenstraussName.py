# ==============================================================================
# Scene:      JohnsonLindenstraussName
# Source:     videos/_2024/transformers/supplements.py (lines 2044-2056)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JohnsonLindenstraussName.py JohnsonLindenstraussName -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class JohnsonLindenstraussName(InteractiveScene):
    def construct(self):
        # Test
        text = VGroup(
            Text("Johnson–Lindenstrauss\nLemma"),
            Tex(R"\Rightarrow", font_size=120),
        )
        text[0].set_color(RED_B)
        text.arrange(RIGHT, buff=MED_LARGE_BUFF)
        self.play(
            FadeIn(text[0], lag_ratio=0.1),
            Write(text[1], run_time=1)
        )
