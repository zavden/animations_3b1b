# ==============================================================================
# Scene:      HoldUp
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 57-70)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUp.py HoldUp -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class HoldUp(TeacherStudentsScene):
    def construct(self):
        arrow = Vector(LEFT, stroke_color=YELLOW)
        arrow.to_edge(UP, buff=1.0)
        # self.add(arrow)
        self.play(
            self.teacher.change("raise_right_hand", look_at=3 * UR),
            self.change_students("pondering", "erm", "sassy", look_at=self.screen)
        )
        self.wait(3)
        self.play(
            self.change_students("maybe", "pondering", "hesitant", look_at=3 * UR)
        )
        self.wait(3)
