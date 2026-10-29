# ==============================================================================
# Scene:      IntroductionOfExp
# Source:     videos/_2019/diffyq/part5/staging.py (lines 18-143)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroductionOfExp.py IntroductionOfExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

T_COLOR = GREY_B


CONST_COLOR = YELLOW


tex_config = {
    "tex_to_color_map": {
        "{t}": T_COLOR,
        "{0}": T_COLOR,
        "e^": WHITE,
        "=": WHITE,
    }
}


class IntroductionOfExp(Scene):
    def construct(self):
        questions = VGroup(
            OldTexText("What", "is", "$e^{t}$", "?"),
            OldTexText("What", "properties", "does", "$e^{t}$", "have?"),
            OldTexText(
                "What", "property", "defines", "$e^{t}$", "?",
                tex_to_color_map={"defines": BLUE}
            ),
        )
        questions.scale(2)
        questions[0].next_to(questions[1], UP, LARGE_BUFF)
        questions[2][-1].next_to(questions[2][-2], RIGHT, SMALL_BUFF)
        questions.to_edge(UP)
        for question in questions:
            part = question.get_part_by_tex("e^{t}")
            part[1].set_color(T_COLOR)

        top_cross = Cross(questions[0])

        deriv_ic = self.get_deriv_and_ic()
        deriv_ic.save_state()
        deriv_ic.scale(2 / 1.5)
        deriv_ic.to_edge(DOWN, buff=LARGE_BUFF)
        derivative, ic = deriv_ic
        derivative.save_state()
        derivative.set_x(0)

        self.play(FadeInFromDown(questions[0]))
        self.wait()
        self.play(
            ShowCreation(top_cross),
            LaggedStart(
                *[
                    TransformFromCopy(
                        questions[0].get_part_by_tex(tex),
                        questions[1].get_part_by_tex(tex),
                    )
                    for tex in ("What", "e^{t}")
                ],
                *[
                    FadeIn(questions[1][i])
                    for i in [1, 2, 4]
                ]
            )
        )
        self.wait()
        self.play(
            TransformFromCopy(
                questions[1].get_part_by_tex("$e^{t}$"),
                derivative[3:7],
            ),
            FadeIn(derivative[:2]),
            FadeIn(derivative.get_part_by_tex("=")),
        )
        self.play(
            ReplacementTransform(
                questions[1][0],
                questions[2][0],
            ),
            FadeOut(questions[1][1]),
            FadeIn(questions[2][1]),
            FadeOut(questions[1][2]),
            FadeIn(questions[2][2]),
            ReplacementTransform(
                questions[1][3],
                questions[2][3],
            ),
            FadeOut(questions[1][4]),
            FadeIn(questions[2][4]),
        )
        self.wait()
        self.play(
            TransformFromCopy(
                derivative[3:7:3],
                derivative[-5:],
                path_arc=-60 * DEGREES,
            ),
        )
        self.wait()
        self.play(
            Restore(derivative),
            FadeIn(ic, LEFT)
        )
        self.wait()
        self.play(
            FadeOut(questions[0]),
            FadeOut(top_cross),
            FadeOut(questions[2]),
            Restore(deriv_ic),
        )
        self.wait()

    def get_deriv_and_ic(self, const=None):
        if const:
            const_str = "{" + str(const) + "}"
            mult_str = "\\cdot"
        else:
            const_str = "{}"
            mult_str = "{}"
        args = [
            "{d \\over d{t}}",
            "e^{",
            const_str,
            "{t}}",
            "=",
            const_str,
            mult_str,
            "e^{",
            const_str,
            "{t}}"
        ]
        derivative = OldTex(
            *args,
            **tex_config
        )
        if const:
            derivative.set_color_by_tex(const_str, CONST_COLOR)

        ic = OldTex("e^{0} = 1", **tex_config)
        group = VGroup(derivative, ic)
        group.arrange(RIGHT, buff=LARGE_BUFF)
        ic.align_to(derivative.get_part_by_tex("e^"), DOWN)
        group.scale(1.5)
        group.to_edge(UP)
        return group
