# ==============================================================================
# Scene:      CommentOnForce
# Source:     videos/_2026/hairy_ball/supplements.py (lines 77-96)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CommentOnForce.py CommentOnForce -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CommentOnForce(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        morty.body.insert_n_curves(1000)
        equation = Tex(R"m x''(t) = \text{Lift} + \text{Gravity}", t2c={R"x''(t)": RED, R"\text{Lift}": PINK, R"\text{Gravity}": BLUE})
        equation.move_to(self.hold_up_spot, DOWN)
        equation.shift_onto_screen()

        self.play(
            morty.change("tease"),
            self.change_students("thinking", "erm", "concentrating", look_at=self.screen),
        )
        self.wait(2)
        self.play(
            morty.change("raise_right_hand", equation),
            self.change_students("pondering", "confused", "hesitant", look_at=equation),
            Write(equation),
        )
        self.wait(3)
