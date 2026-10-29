# ==============================================================================
# Scene:      ILearnedSomething
# Source:     videos/_2022/convolutions/supplements.py (lines 31-47)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ILearnedSomething.py ILearnedSomething -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ILearnedSomething(TeacherStudentsScene):
    def construct(self):
        # Test
        implication = VGroup(
            Text("Making\nvisuals"),
            OldTex(R"\Rightarrow", font_size=60),
            Text("Deeper\nunderstanding")
        )
        implication.arrange(RIGHT, buff=0.4)
        implication.move_to(self.hold_up_spot, DOWN)
        implication.shift_onto_screen()
        self.play(
            self.teacher.change("raise_right_hand", implication),
            FadeIn(implication, UP),
            self.change_students("confused", "hesitant", "tease", look_at=implication)
        )
        self.wait(5)
