# ==============================================================================
# Scene:      DivisionOfUnity
# Source:     videos/_2018/borsuk_addition.py (lines 1110-1139)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/uncertainty.py
#
# Run from this folder:
#     manimgl DivisionOfUnity.py DivisionOfUnity -w -m --fps 15
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

class DivisionOfUnity(Scene):
    def construct(self):
        factor = 2
        line = Line(factor * LEFT, factor * RIGHT)
        lower_brace = Brace(line, DOWN)
        lower_brace.add(lower_brace.get_text("1"))
        v_lines = VGroup(*[
            DashedLine(0.2 * UP, 0.2 * DOWN).shift(factor * v)
            for v in [LEFT, 0.3 * LEFT, 0.1 * RIGHT, RIGHT]
        ])
        upper_braces = VGroup(*[
            Brace(VGroup(vl1, vl2), UP)
            for vl1, vl2 in zip(v_lines[:-1], v_lines[1:])
        ])
        colors = color_gradient([GREEN, BLUE], 3)
        for i, color, brace in zip(it.count(1), colors, upper_braces):
            label = brace.get_tex("x_%d^2" % i)
            label.set_color(color)
            brace.add(label)

        self.add(line, lower_brace)
        self.play(LaggedStartMap(
            ShowCreation, v_lines[1:3],
            lag_ratio=0.8,
            run_time=1
        ))
        self.play(LaggedStartMap(
            GrowFromCenter, upper_braces
        ))
        self.wait()
