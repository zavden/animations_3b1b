# ==============================================================================
# Scene:      UmWhy
# Source:     videos/_2026/print_gallery/supplements.py (lines 625-642)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UmWhy.py UmWhy -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UmWhy(TeacherStudentsScene):
    def construct(self):
        stds = self.students
        morty = self.teacher
        self.play(
            stds[1].says("Um, why?", mode="maybe", look_at=self.screen),
            stds[2].change("erm", look_at=self.screen),
            stds[0].change("pondering", look_at=self.screen),
        )
        self.play(morty.change("guilty"))
        self.wait(3)
        self.play(
            morty.says("Watch what\nhappens"),
            stds[1].debubble(),
            stds[0].change("hesitant", morty.eyes),
            stds[2].change("sassy", morty.eyes),
        )
        self.wait(3)
