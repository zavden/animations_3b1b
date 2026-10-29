# ==============================================================================
# Scene:      DoesThisMakeSense
# Source:     videos/_2023/clt/wordy_scenes.py (lines 1049-1063)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DoesThisMakeSense.py DoesThisMakeSense -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DoesThisMakeSense(InteractiveScene):
    def construct(self):
        rect = SurroundingRectangle(Tex(R"\sigma_a = \sigma / \sqrt{100} = 0.171"))
        words = Text("Does this make sense?")
        words.next_to(rect, DOWN)
        words.align_to(rect.get_center(), RIGHT)

        rect.set_stroke(RED, 2)
        words.set_color(RED)

        self.play(
            ShowCreation(rect),
            Write(words)
        )
        self.wait()
