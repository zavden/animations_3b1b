# ==============================================================================
# Scene:      GoalOfRediscovery
# Source:     videos/_2024/holograms/supplements.py (lines 348-364)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoalOfRediscovery.py GoalOfRediscovery -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GoalOfRediscovery(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        self.play(
            self.change_students("pondering", "confused", "maybe", look_at=self.screen),
            morty.change("guilty"),
        )
        self.wait(2)
        self.play(
            morty.says("I want this to\nfeel rediscovered"),
            self.change_students("tease", "erm", "pondering", look_at=morty.eyes)
        )
        self.wait(2)
        self.look_at(self.screen)
        self.play(self.change_students("thinking", "pondering", "thinking"))
        self.wait(4)
