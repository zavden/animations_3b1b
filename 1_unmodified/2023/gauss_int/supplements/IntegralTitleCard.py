# ==============================================================================
# Scene:      IntegralTitleCard
# Source:     videos/_2023/gauss_int/supplements.py (lines 407-468)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegralTitleCard.py IntegralTitleCard -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class IntegralTitleCard(InteractiveScene):
    def construct(self):
        # Test
        curve = FunctionGraph(lambda x: np.exp(-x**2), x_range=(-2.5, 2.5, 0.1))
        curve.set_width(8)
        curve.set_height(3, stretch=True)
        curve.move_to(DOWN)
        curve.set_stroke(BLUE, 3)
        curve.set_fill(BLUE, 0.5)

        # Make it into an equation
        curve.set_height(2)
        parens = Tex("()")
        parens.match_height(curve)
        parens[0].next_to(curve, LEFT, buff=0.2)
        parens[1].next_to(curve, RIGHT, buff=0.2)
        lhs = VGroup(curve, parens)
        two = Integer(2).move_to(lhs.get_corner(UR))
        lhs.add(two)

        equals = Tex("=", font_size=90)
        equals.next_to(lhs, RIGHT, MED_LARGE_BUFF)

        circle = Circle()
        circle.match_style(curve)
        circle.set_height(3)
        circle.next_to(equals, RIGHT, MED_LARGE_BUFF)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_stroke(WHITE, 2)
        r_label = Integer(1).next_to(radius, UP, SMALL_BUFF)
        rhs = VGroup(circle, radius, r_label)

        equation = VGroup(lhs, equals, rhs)
        equation.move_to(DOWN)

        # Animate
        self.add(curve)
        circle.set_fill(opacity=0)
        self.play(LaggedStart(
            Write(VGroup(parens, two, equals), run_time=1),
            TransformFromCopy(curve.copy().set_fill(opacity=0), circle),
            FadeIn(VGroup(radius, r_label)),
            FadeIn(circle.copy().set_fill(opacity=0.5)),
            lag_ratio=0.5,
            run_time=3
        ))
        # circle.set_fill(opacity=0.5)
        self.add(rhs)
        # self.play(circle.animate.set_fill(opacity=0.5))
        self.wait(2)

        return

        # Alternatively...
        func_label = Tex("e^{-x^2}", font_size=60)
        func_label.next_to(curve.pfp(0.6), UR)
        area_label = Tex(R"\sqrt{\pi}", font_size=120)
        area_label.move_to(curve, DOWN).shift(0.5 * UP)

        self.play(ShowCreation(curve), FadeIn(func_label, lag_ratio=0.1))
        self.play(curve.animate.set_fill(BLUE, 0.5), Write(area_label))
        self.wait()
