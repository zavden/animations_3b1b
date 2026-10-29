# ==============================================================================
# Scene:      FrustratedAtGroups
# Source:     videos/_2020/monster.py (lines 2360-2374)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FrustratedAtGroups.py FrustratedAtGroups -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FrustratedAtGroups(TeacherStudentsScene):
    def construct(self):
        formula = OldTex(r"|G|=|Z(G)|+\sum i\left[G: C_{G}\left(x_{i}\right)\right]")
        formula.move_to(self.hold_up_spot, DOWN)
        formula.shift(0.5 * UL)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeIn(formula, DOWN),
        )
        self.play_student_changes("confused", "horrified", "pleading")
        self.look_at(formula.get_left())
        self.wait(2)
        self.look_at(formula.get_right())
        self.wait(2)
