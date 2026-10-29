# ==============================================================================
# Scene:      WhoCares
# Source:     videos/_2022/some2/winners.py (lines 1051-1078)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhoCares.py WhoCares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhoCares(TeacherStudentsScene):
    def construct(self):
        # Start
        morty = self.teacher
        stds = self.students

        equation = OldTex("\\sum_{n=1}^N n^2 = \\frac{N(N + 1)(2N + 1)}{6}")
        equation.set_stroke(WHITE, 1)
        equation.move_to(self.hold_up_spot, DOWN).shift(UL)

        self.play(
            morty.change("raise_right_hand", look_at=equation),
            Write(equation),
            self.change_students("pondering", "pondering", "pondering", look_at=equation),
        )
        self.wait()
        self.play(self.change_students("sassy", "confused", "erm"))
        self.wait()
        self.play(
            stds[0].says("Why should\nI care?", mode="angry"),
            morty.change("guilty"),
        )
        self.wait()
        self.play(
            morty.says("Well...hmmm...", mode="sassy", look_at=equation),
            stds[1].change("maybe"),
        )
        self.wait(5)
