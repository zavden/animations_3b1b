# ==============================================================================
# Scene:      SridharWatchingScene
# Source:     videos/_2018/wallis.py (lines 400-451)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SridharWatchingScene.py SridharWatchingScene -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


class SridharWatchingScene(PiCreatureScene):
    CONFIG = {
        "default_pi_creature_kwargs": {
            "color": YELLOW_E,
            "flip_at_start": False,
        },
    }

    def construct(self):
        laptop = Laptop()
        laptop.scale(1.8)
        laptop.to_corner(DR)
        sridhar = self.pi_creature
        sridhar.next_to(laptop, LEFT, SMALL_BUFF, DOWN)
        bubble = ThoughtBubble()
        bubble.flip()
        bubble.pin_to(sridhar)

        basel = OldTex(
            "{1", "\\over", "1^2}", "+"
            "{1", "\\over", "2^2}", "+"
            "{1", "\\over", "3^2}", "+", "\\cdots",
            "= \\frac{\\pi^2}{6}"
        )
        wallis = get_wallis_product(n_terms=4)
        VGroup(basel, wallis).scale(0.7)
        basel.move_to(bubble.get_bubble_center())
        basel.to_edge(UP, buff=MED_SMALL_BUFF)
        wallis.next_to(basel, DOWN, buff=0.75)
        arrow = OldTex("\\updownarrow")
        arrow.move_to(VGroup(basel, wallis))
        basel.set_color(YELLOW)
        wallis.set_color(BLUE)

        self.play(LaggedStartMap(DrawBorderThenFill, laptop))
        self.play(sridhar.change, "pondering", laptop.screen)
        self.wait()
        self.play(ShowCreation(bubble))
        self.play(LaggedStartMap(FadeIn, basel))
        self.play(
            ReplacementTransform(basel.copy(), wallis),
            GrowFromPoint(arrow, arrow.get_top())
        )
        self.wait(4)
        self.play(sridhar.change, "thinking", wallis)
        self.wait(4)
        self.play(LaggedStartMap(
            ApplyFunction,
            VGroup(*list(laptop) + [bubble, basel, arrow, wallis, sridhar]),
            lambda mob: (lambda m: m.set_color(BLACK).fade(1).scale(0.8), mob),
            run_time=3,
        ))
