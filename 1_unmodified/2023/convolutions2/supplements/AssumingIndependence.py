# ==============================================================================
# Scene:      AssumingIndependence
# Source:     videos/_2023/convolutions2/supplements.py (lines 193-210)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AssumingIndependence.py AssumingIndependence -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AssumingIndependence(TeacherStudentsScene):
    def construct(self):
        # Assuming...
        morty = self.teacher
        stds = self.students
        self.remove(self.background)

        self.play(
            morty.says("Assuming\nindependence!", mode="surprised", run_time=1),
            self.change_students("hesitant", "guilty", "plain")
        )
        self.wait(3)
        self.play(
            morty.debubble("tease"),
            stds[1].says(TexText(R"Isn't that a \\ little pedantic?"), mode="sassy"),
            stds[2].change("angry")
        )
        self.wait(3)
