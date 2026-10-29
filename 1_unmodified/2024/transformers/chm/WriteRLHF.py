# ==============================================================================
# Scene:      WriteRLHF
# Source:     videos/_2024/transformers/chm.py (lines 1414-1430)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteRLHF.py WriteRLHF -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WriteRLHF(InteractiveScene):
    def construct(self):
        text = Text("Step 2: RLHF")
        full_text = Text("Reinforcement Learning\nwith Human Feedback")
        full_text.next_to(text, UP, LARGE_BUFF)
        full_text.align_to(text, RIGHT).shift(RIGHT)
        initials = VGroup(full_text[letter[0]][0][0] for letter in "RLHF")
        full_text.remove(*initials)

        self.add(text)
        self.wait()
        self.play(
            TransformFromCopy(text["RLHF"][0], initials, lag_ratio=0.25),
            Write(full_text, time_span=(1.5, 3)),
            run_time=3
        )
        self.wait()
