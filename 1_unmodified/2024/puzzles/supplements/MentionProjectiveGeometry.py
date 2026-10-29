# ==============================================================================
# Scene:      MentionProjectiveGeometry
# Source:     videos/_2024/puzzles/supplements.py (lines 287-297)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MentionProjectiveGeometry.py MentionProjectiveGeometry -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MentionProjectiveGeometry(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.play(
            stds[1].says("You could use\n projective geometry!", mode="hooray", look_at=morty.eyes),
            morty.change("happy"),
            stds[2].change("confused", stds[1].eyes),
            stds[0].change("erm", stds[1].eyes),
        )
        self.wait(4)
