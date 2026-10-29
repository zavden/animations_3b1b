# ==============================================================================
# Scene:      AnnotateLogP
# Source:     videos/_2026/cross_entropy/supplements.py (lines 794-863)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AnnotateLogP.py AnnotateLogP -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AnnotateLogP(InteractiveScene):
    def construct(self):
        # Add equation
        equation = Tex(R"-\log_2(p) = n")
        info = equation[R"-\log_2(p)"][0]
        info_rect = SurroundingRectangle(info, buff=SMALL_BUFF)
        info_rect.set_stroke(BLUE, 2)
        eq = equation["="][0]
        info_word = Text("Information")
        info_word.set_color(BLUE)
        info_word.match_width(info_rect)
        info_word.next_to(info_rect, DOWN, SMALL_BUFF)

        n_rect = SurroundingRectangle(equation["n"], buff=SMALL_BUFF)
        n_rect.match_height(info_rect, stretch=True).match_y(info_rect)
        n_rect.set_stroke(YELLOW, 2)
        n_bits = Text("# bits")
        n_bits.next_to(n_rect, UP, SMALL_BUFF, LEFT)
        n_bits.match_color(n_rect)

        self.add(equation)
        self.wait()
        self.play(
            ShowCreation(info_rect),
            FadeIn(info_word, lag_ratio=0.1),
        )
        self.wait()

        # Replace eq with ineq
        bang = Tex(R"!!")
        bang.set_color(RED)
        bang.next_to(eq, UP)
        ineq = Tex(R"\le")
        ineq.move_to(eq)

        self.play(
            eq.animate.set_color(RED),
            FadeIn(bang, 0.2 * UP)
        )
        self.wait()
        self.play(
            Transform(eq, ineq),
            FadeOut(bang)
        )
        self.play(
            FadeIn(n_rect),
            FadeIn(n_bits, lag_ratio=0.1),
        )
        self.wait()

        # Show averages
        n_bits.target = n_bits.generate_target()
        n_bits.target.next_to(ineq, RIGHT)
        overbars = VGroup(
            Line(mob.get_left(), mob.get_right()).next_to(mob, UP, SMALL_BUFF)
            for mob in [info, n_bits.target]
        )
        overbars.set_stroke(WHITE, 4)

        self.play(
            FadeOut(info_rect),
            FadeOut(info_word),
            MoveToTarget(n_bits),
            FadeOut(n_rect),
            FadeOut(equation["n"]),
        )
        self.play(
            ShowCreation(overbars, lag_ratio=0)
        )
        self.wait()
