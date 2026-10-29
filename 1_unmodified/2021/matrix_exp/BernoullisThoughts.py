# ==============================================================================
# Scene:      BernoullisThoughts
# Source:     videos/_2021/matrix_exp.py (lines 3109-3161)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BernoullisThoughts.py BernoullisThoughts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BernoullisThoughts(Scene):
    def construct(self):
        im = ImageMobject("Jacob_Bernoulli", height=4)
        name = Text("Jacob Bernoulli")
        name.match_width(im)
        name.next_to(im, DOWN, SMALL_BUFF)
        jacob = Group(im, name)
        jacob.to_corner(DR)

        bubble = ThoughtBubble(height=3.5, width=5)
        bubble.pin_to(jacob)
        bubble.shift(0.25 * RIGHT + 0.75 * DOWN)

        dollars = Text("$$$")
        dollars.set_height(1)
        dollars.set_color(GREEN)
        dollars.move_to(bubble.get_bubble_center())

        dollar = dollars[0].copy()
        continuous_money = VGroup(*(
            dollar.copy().shift(smooth(x) * RIGHT * 2.0 + np.exp(smooth(x) - 1) * UP)
            for x in np.linspace(0, 1, 300)
        ))
        continuous_money.set_fill(opacity=0.1)
        continuous_money.center()
        continuous_money.move_to(dollars)

        self.play(FadeIn(jacob, shift=RIGHT))
        self.play(
            ShowCreation(bubble),
            Write(dollars)
        )
        self.wait()
        self.add(continuous_money)
        self.play(
            FadeOut(dollars),
            Write(continuous_money, stroke_color=GREEN, stroke_width=1, run_time=3),
        )
        self.play(
            FadeOut(continuous_money, lag_ratio=0.01),
            FadeIn(dollars)
        )
        self.wait()

        limit = OldTex("\\left(1 + \\frac{r}{n}\\right)^{nt}")
        limit.move_to(bubble.get_bubble_center())
        limit.scale(1.5)

        self.play(
            FadeOut(dollars),
            FadeIn(limit),
        )
        self.wait()
