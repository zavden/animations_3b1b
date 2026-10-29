# ==============================================================================
# Scene:      LabelVector
# Source:     videos/_2024/transformers/chm.py (lines 258-269)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LabelVector.py LabelVector -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LabelVector(InteractiveScene):
    def construct(self):
        brace = Brace(Line(UP, DOWN).set_height(4), RIGHT)
        name = Text("Vector", font_size=72)
        name.next_to(brace, RIGHT)
        name.set_backstroke(BLACK, 5)

        self.play(
            GrowFromCenter(brace),
            Write(name),
        )
        self.wait()
