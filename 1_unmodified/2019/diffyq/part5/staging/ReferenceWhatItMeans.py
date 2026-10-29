# ==============================================================================
# Scene:      ReferenceWhatItMeans
# Source:     videos/_2019/diffyq/part5/staging.py (lines 1388-1483)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferenceWhatItMeans.py ReferenceWhatItMeans -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

T_COLOR = GREY_B


POSITION_COLOR = BLUE


CONST_COLOR = YELLOW


class ReferenceWhatItMeans(PiCreatureScene):
    def construct(self):
        randy = self.pi_creature

        tex_config = {
            "tex_to_color_map": {
                "{i}": CONST_COLOR,
                "\\pi": T_COLOR,
                "-1": POSITION_COLOR,
            },
        }
        epii = OldTex(
            "e^{{i} \\pi} = -1",
            **tex_config
        )
        epii.scale(2)

        many_es = OldTex("e \\cdot e \\cdots e", "= -1", **tex_config)
        many_es.scale(2)
        brace = Brace(many_es[0], DOWN)
        pi_i = OldTex("{i} \\pi \\text{ times}", **tex_config)
        pi_i.next_to(brace, DOWN, SMALL_BUFF)
        repeated_mult = VGroup(many_es, brace, pi_i)

        # arrow = Vector(2 * RIGHT)
        arrow = OldTex("\\Rightarrow")
        arrow.scale(2)

        group = VGroup(epii, arrow, repeated_mult)
        group.arrange(
            RIGHT, buff=LARGE_BUFF,
        )
        for mob in group[1:]:
            mob.shift(
                (epii[0].get_bottom() - mob[0].get_bottom())[1] * UP
            )
        group.to_edge(UP)

        does_not_mean = OldTexText("Does \\emph{not}\\\\mean")
        does_not_mean.set_color(RED)
        does_not_mean.move_to(arrow)
        # cross = Cross(repeated_mult)

        nonsense = OldTexText(
            "\\dots because that's "
            "literal nonsense!"
        )
        nonsense.next_to(repeated_mult, DOWN)
        nonsense.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        nonsense.set_color(RED)

        down_arrow = OldTex("\\Downarrow")
        down_arrow.scale(2)
        down_arrow.stretch(1.5, 1)
        down_arrow.set_color(GREEN)
        down_arrow.next_to(epii, DOWN, LARGE_BUFF)
        actually_means = OldTexText("It actually\\\\means")
        actually_means.next_to(down_arrow, RIGHT)
        actually_means.set_color(GREEN)

        series = OldTex(
            "{({i} \\pi )^0 \\over 0!} + ",
            "{({i} \\pi )^1 \\over 1!} + ",
            "{({i} \\pi )^2 \\over 2!} + ",
            "{({i} \\pi )^3 \\over 3!} + ",
            "{({i} \\pi )^4 \\over 4!} + ",
            "\\cdots = -1",
            **tex_config
        )
        series.set_width(FRAME_WIDTH - 1)
        series.next_to(down_arrow, DOWN, LARGE_BUFF)
        series.set_x(0)

        self.add(epii)
        self.play(
            FadeIn(arrow, LEFT),
            FadeIn(repeated_mult, 2 * LEFT),
            randy.change, "maybe",
        )
        self.wait()
        self.play(randy.change, "confused")
        self.play(
            FadeOut(arrow, DOWN),
            FadeIn(does_not_mean, UP),
        )
        self.play(Write(nonsense))
        self.play(randy.change, "angry")
        # self.play(ShowCreation(cross))
        self.wait()
        self.play(
            FadeOut(randy, DOWN),
            FadeIn(down_arrow, UP),
            FadeIn(actually_means, LEFT),
            FadeIn(series, lag_ratio=0.1, run_time=2)
        )
        self.wait()
