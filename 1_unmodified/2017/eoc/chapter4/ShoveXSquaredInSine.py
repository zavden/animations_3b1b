# ==============================================================================
# Scene:      ShoveXSquaredInSine
# Source:     videos/_2017/eoc/chapter4.py (lines 1459-1505)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShoveXSquaredInSine.py ShoveXSquaredInSine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


class ShoveXSquaredInSine(Scene):
    def construct(self):
        title = OldTexText("Function composition")
        title.to_edge(UP)

        sine = OldTex("g(", "x", ")", "=", "\\sin(", "x", ")")
        sine.set_color(SINE_COLOR)
        x_squared = OldTex("h(x)", "=", "x^2")
        x_squared.set_color(X_SQUARED_COLOR)
        group = VGroup(sine, x_squared)
        group.arrange(buff = LARGE_BUFF)
        group.shift(UP)
        composition = OldTex(
            "g(", "h(x)", ")", "=", "\\sin(", "x^2", ")"
        )
        for i in 0, 2, 4, 6:
            composition[i].set_color(SINE_COLOR)
        for i in 1, 5:
            composition[i].set_color(X_SQUARED_COLOR)
        composition.next_to(group, DOWN, buff = LARGE_BUFF)

        brace = Brace(VGroup(*composition[-3:]), DOWN)
        deriv_q = brace.get_text("Derivative?")

        self.add(group)
        self.play(Write(title))
        self.wait()
        triplets = [
            [sine, (0, 2), (0, 2)],
            [x_squared, (0,), (1,)],
            [sine, (3, 4, 6), (3, 4, 6)],
            [x_squared, (2,), (5,)]
        ]
        for premob, pre_indices, comp_indicies in triplets:
            self.play(*[
                ReplacementTransform(
                    premob[i].copy(), composition[j]
                )
                for i, j in zip(pre_indices, comp_indicies)
            ])
            self.wait()
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(deriv_q)
        )
        self.wait()
