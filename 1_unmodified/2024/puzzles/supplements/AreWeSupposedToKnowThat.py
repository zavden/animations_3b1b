# ==============================================================================
# Scene:      AreWeSupposedToKnowThat
# Source:     videos/_2024/puzzles/supplements.py (lines 206-226)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AreWeSupposedToKnowThat.py AreWeSupposedToKnowThat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AreWeSupposedToKnowThat(TeacherStudentsScene):
    def construct(self):
        morty = self.teacher
        stds = self.students
        self.play(
            stds[0].change("confused", look_at=self.screen),
            stds[1].change("erm", look_at=self.screen),
            stds[2].says("Are we supposed\nto know that?", mode="pleading", look_at=self.screen, bubble_direction=LEFT),
            morty.change("guilty"),
        )
        self.wait(4)

        self.play(
            morty.change("raise_right_hand"),
            stds[2].debubble(mode="hesitant", look_at=morty.eyes),
            stds[0].change("maybe", morty.eyes),
            stds[1].change("pondering", morty.eyes),
        )
        self.wait(2)
        self.play(self.change_students("pondering", "pondering", "pondering", 2 * UR))
        self.wait(3)
