# ==============================================================================
# Scene:      WhyDoWeCare
# Source:     videos/_2026/hairy_ball/supplements.py (lines 4-30)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyDoWeCare.py WhyDoWeCare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyDoWeCare(TeacherStudentsScene):
    def construct(self):
        # Test
        stds = self.students
        morty = self.teacher

        self.play(
            self.change_students("confused", "erm", "concentrating", look_at=self.screen),
        )
        self.wait(3)
        self.play(
            stds[2].change("erm", stds[1].eyes),
            stds[1].says("I’m sorry, why\ndo we care?", mode="sassy"),
            stds[0].change("thinking", self.screen),
            morty.change("well"),
        )
        self.wait(2)
        self.play(self.change_students("pondering", "maybe", "pondering", look_at=self.screen))

        # Answer
        self.play(
            morty.says("Topology has\nmore subtle utility", mode="tease"),
            stds[0].animate.look_at(morty.eyes),
            stds[1].debubble(),
            stds[2].change("hesitant", morty.eyes)
        )
        self.wait(3)
