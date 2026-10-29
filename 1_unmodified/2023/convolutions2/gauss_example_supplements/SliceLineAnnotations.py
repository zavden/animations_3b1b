# ==============================================================================
# Scene:      SliceLineAnnotations
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 490-545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SliceLineAnnotations.py SliceLineAnnotations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SliceLineAnnotations(InteractiveScene):
    def construct(self):
        # Line equation
        kw = dict(t2c={"s": RED})
        line_eq = Tex("x + y = s", **kw)
        line_eq.to_edge(UP)
        s_term = line_eq["s"][0]
        decimal_rhs = DecimalNumber(-6, edge_to_fix=LEFT)
        decimal_rhs.move_to(s_term, LEFT)
        decimal_rhs.shift(0.025 * UP)
        s_eq = Tex("=").rotate(90 * DEGREES)
        s_eq.next_to(s_term, DOWN, SMALL_BUFF)

        self.add(line_eq, decimal_rhs)
        self.remove(s_term)
        self.play(ChangeDecimalToValue(decimal_rhs, 1), run_time=5 / 1.5)
        self.wait()
        self.play(
            decimal_rhs.animate.next_to(s_eq, DOWN, SMALL_BUFF),
            Write(s_eq),
            FadeIn(s_term, 0.5 * DOWN),
        )
        self.wait()

        # What we want
        words = Text("What we want:")
        words.to_corner(UR)
        conv = Tex("[f * g](s)", **kw)
        conv.next_to(words, DOWN, MED_LARGE_BUFF)
        conv_eq = Tex("=").rotate(90 * DEGREES)
        conv_eq.next_to(conv, DOWN)
        area = Tex(R"(\text{This area}) / \sqrt{2}")
        area[R"\text{This area}"].set_color(TEAL)
        area.next_to(conv_eq, DOWN)

        self.play(
            FadeIn(words, 0.5 * UP),
            FadeIn(conv, 0.5 * DOWN),
        )
        self.play(FlashAround(conv, run_time=2, time_width=1.5))
        self.wait()
        self.play(
            Write(conv_eq),
            FadeIn(area, 0.5 * DOWN),
        )
        for s in [1.5, 0.5, 1.0]:
            self.play(ChangeDecimalToValue(decimal_rhs, s))
            self.wait()

        self.play(
            LaggedStartMap(FadeOut, VGroup(
                words, conv, conv_eq, area, s_eq, decimal_rhs
            )),
            line_eq.animate.to_corner(UR),
        )
        self.wait()
