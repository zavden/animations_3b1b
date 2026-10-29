# ==============================================================================
# Scene:      CountHoles
# Source:     videos/_2019/windmill.py (lines 3548-3587)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CountHoles.py CountHoles -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CountHoles(Scene):
    def construct(self):
        labels = VGroup(
            OldTexText("Genus ", "0"),
            OldTexText("Genus ", "1"),
            OldTexText("Genus ", "2"),
        )

        labels.scale(2)
        labels.arrange(RIGHT, buff=1.5)
        labels.move_to(2 * DOWN)

        equation = OldTex("y^2 = x^3 + ax + b")
        equation.scale(1.5)
        equation.shift(UP)
        equation.to_edge(LEFT)
        # arrow = OldTex("\\approx").scale(2)
        arrow = Vector(2 * RIGHT)
        arrow.next_to(equation, RIGHT)

        equation_text = OldTexText("Some other problem")
        equation_text.next_to(equation, DOWN, MED_LARGE_BUFF)
        equation_text.match_width(equation)
        equation_text.set_color(YELLOW)

        self.play(LaggedStartMap(
            FadeInFromDown, labels,
            lag_ratio=0.5,
        ))
        self.wait()
        self.play(
            labels[1].shift, 4 * RIGHT,
            FadeOut(labels[0::2]),
        )
        self.play(
            FadeIn(equation, RIGHT),
            GrowArrow(arrow),
        )
        self.play(FadeIn(equation_text, UP))
        self.wait()
