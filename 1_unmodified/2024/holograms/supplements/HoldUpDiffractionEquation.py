# ==============================================================================
# Scene:      HoldUpDiffractionEquation
# Source:     videos/_2024/holograms/supplements.py (lines 711-741)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HoldUpDiffractionEquation.py HoldUpDiffractionEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HoldUpDiffractionEquation(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher

        equation = Tex(R"d \cdot \sin(\theta) = \lambda", t2c={R"\lambda": TEAL}, font_size=60)
        equation.move_to(self.hold_up_spot, DOWN)

        words = Text("Remember this")
        words.next_to(equation, UP, 1.5)
        equation.to_edge(RIGHT)
        arrow = Arrow(words, equation)

        self.play(
            morty.change("raise_left_hand", look_at=equation),
            FadeIn(equation, UP),
            self.change_students("pondering", "pondering", "pondering", equation)
        )
        self.play(
            FadeIn(words, lag_ratio=0.1),
            GrowArrow(arrow),
        )
        self.play(morty.change("tease"))
        self.wait(3)

        morty.body.insert_n_curves(100)
        self.play(
            self.change_students("thinking", "erm", "pondering", look_at=self.screen),
            morty.change("raise_right_hand", look_at=self.screen),
        )
        self.wait(4)
