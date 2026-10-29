# ==============================================================================
# Scene:      UnexpectedConnection
# Source:     videos/_2018/borsuk_addition.py (lines 68-139)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl UnexpectedConnection.py UnexpectedConnection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - removed arrow.tip[1].shift(SMALL_BUFF*UP): GL arrows have no separate tip (0.1 cosmetic shift)
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/borsuk_addition.py -----

class UnexpectedConnection(Scene):
    def construct(self):
        primes = OldTex(
            "2,", "3,", "5,", "7,", "11,", "13,", "17,", "\\dots"
        )
        primes.move_to(2.5 * UP)

        circle = Circle(
            color=YELLOW,
            stroke_width=1,
            radius=1.5,
        )
        circle.shift(1.5 * DOWN)
        center = circle.get_center()
        center_dot = Dot(center)
        radius = Line(center, circle.get_right())
        radius.set_stroke(WHITE, 3)

        arrow = DoubleArrow(primes, circle)
        # CHANGE: GL arrows are a single shape (no arrow.tip); dropped the tiny 0.1 shift of the end tip
        pass
        arrow.save_state()
        arrow.rotate(90 * DEGREES)
        arrow.scale(1.5)
        arrow.fade(1)

        formula = OldTex(
            "\\frac{\\pi^2}{6} = \\prod_{p \\text{ prime}}"
            "\\frac{1}{1 - p^{-2}}"
        )
        formula.next_to(arrow.get_center(), RIGHT)

        def get_arc():
            angle = radius.get_angle()
            return Arc(
                start_angle=0,
                angle=angle,
                radius=circle.radius,
                stroke_color=YELLOW,
                stroke_width=5
            ).shift(center)

        arc = always_redraw(get_arc)

        decimal = DecimalNumber(0)
        decimal.add_updater(
            lambda d: d.move_to(interpolate(
                radius.get_start(),
                radius.get_end(),
                1.5,
            )),
        )
        decimal.add_updater(
            lambda d: d.set_value(radius.get_angle())
        )
        pi = OldTex("\\pi")
        pi.scale(2)
        pi.next_to(circle, LEFT)

        self.add(circle, radius, center_dot, decimal, arc)
        self.play(
            Rotate(radius, PI - 1e-7, about_point=center),
            LaggedStartMap(FadeInFromDown, primes),
            run_time=4
        )
        self.remove(decimal)
        self.add(pi)
        self.wait()
        self.play(
            Restore(arrow),
            FadeIn(formula, LEFT)
        )
        self.wait()
