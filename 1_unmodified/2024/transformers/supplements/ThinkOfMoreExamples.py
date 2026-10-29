# ==============================================================================
# Scene:      ThinkOfMoreExamples
# Source:     videos/_2024/transformers/supplements.py (lines 929-962)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThinkOfMoreExamples.py ThinkOfMoreExamples -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThinkOfMoreExamples(TeacherStudentsScene):
    def construct(self):
        # Show general confusion
        morty = self.teacher
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        self.play(
            morty.change("raise_right_hand"),
            self.change_students("confused", "maybe", "confused", look_at=3 *UP, run_time=2, lag_ratio=0.25),
        )
        self.wait(2)
        self.play(morty.change("guilty"))
        self.play(
            
            self.change_students("confused", "pleading", "concentrating", look_at=3 * UP, run_time=2, lag_ratio=0.25)
        )
        self.wait(3)
        self.play(
            self.change_students("maybe", "confused", "dejected", look_at=morty.eyes, lag_ratio=0),
            morty.change("well")
        )
        self.wait(2)

        # Ask about the goal
        self.wait()
        self.play(LaggedStart(
            self.students[2].says("What is attention\nsupposed to do?"),
            self.students[0].change("maybe"),
            self.students[1].change("pondering"),
            morty.change("tease"),
            lag_ratio=0.1
        ))
        self.wait(5)
