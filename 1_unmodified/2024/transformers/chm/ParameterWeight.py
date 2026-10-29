# ==============================================================================
# Scene:      ParameterWeight
# Source:     videos/_2024/transformers/chm.py (lines 1220-1236)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ParameterWeight.py ParameterWeight -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ParameterWeight(InteractiveScene):
    def construct(self):
        # Test
        text = Text("Parameter / Weight", font_size=72)
        text.to_edge(UP)
        text.set_color(YELLOW)
        param = text["Parameter"][0]
        param.save_state()
        param.set_x(0)

        self.play(Write(param))
        self.wait()
        self.play(LaggedStart(
            Restore(param),
            FadeIn(text["/ Weight"]),
        ))
        self.wait()
