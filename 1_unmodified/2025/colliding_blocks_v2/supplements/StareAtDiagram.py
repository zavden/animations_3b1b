# ==============================================================================
# Scene:      StareAtDiagram
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 604-632)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StareAtDiagram.py StareAtDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StareAtDiagram(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(
            self.change_students("well", "happy", look_at=self.screen),
            stds[2].says("I can see\nmyself there", mode="tease", look_at=self.screen, bubble_direction=LEFT),
            morty.change("tease")
        )
        self.wait(4)
        self.play(
            stds[2].debubble(mode="pondering", look_at=3 * UP),
            self.change_students("pondering", "pondering", look_at=3 * UP),
            morty.change("raise_right_hand"),
            FadeOut(self.background),
        )
        self.wait()
        self.play(stds[1].change("concentrating", look_at=3 * UP))
        self.wait()
        self.play(LaggedStart(
            stds[1].change("hooray"),
            stds[0].change("erm", look_at=stds[1].eyes),
            stds[2].change("erm", look_at=stds[1].eyes),
            morty.change("tease", look_at=stds[1].eyes),
            lag_ratio=0.25,
        ))
        self.wait()
