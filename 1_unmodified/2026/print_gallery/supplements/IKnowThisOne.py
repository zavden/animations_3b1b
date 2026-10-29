# ==============================================================================
# Scene:      IKnowThisOne
# Source:     videos/_2026/print_gallery/supplements.py (lines 496-513)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IKnowThisOne.py IKnowThisOne -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IKnowThisOne(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            stds[2].says("I know\nthis one!", look_at=morty.eyes, mode="hooray", bubble_direction=LEFT),
            stds[0].change("confused", self.screen),
            stds[1].change("happy", self.screen),
            morty.change("tease"),
        )
        self.wait(3)
        self.play(
            morty.change("raise_right_hand"),
            stds[2].debubble('pondering', self.screen),
        )
        self.wait(2)
