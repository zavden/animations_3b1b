# ==============================================================================
# Scene:      LinearityDefinition
# Source:     videos/_2025/laplace/supplements.py (lines 1046-1116)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LinearityDefinition.py LinearityDefinition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LinearityDefinition(InteractiveScene):
    def construct(self):
        # Base differential equation string
        eq_str = R"m x''(t) + k x(t) = 0"
        t2c = {"x_1": TEAL, "x_2": RED, "0.0": YELLOW, "2.0": YELLOW}

        base_eq = Tex(eq_str)
        base_eq.to_edge(UP)

        eq1, eq2, eq3, eq4 = equations = VGroup(
            Tex(eq_str.replace("x", "x_1"), t2c=t2c),
            Tex(eq_str.replace("x", "x_2"), t2c=t2c),
            Tex(R"m\Big(x_1''(t) + x_2''(t) \Big) + k \Big(x_1(t) + x_2(t)\Big) = 0", t2c=t2c),
            Tex(R"m\Big(0.0 x_1''(t) + 2.0 x_2''(t) \Big) + k \Big(0.0 x_1(t) + 2.0 x_2(t)\Big) = 0", t2c=t2c),
        )
        for eq in equations:
            eq.set_max_width(7)
        equations.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        equations.to_edge(RIGHT)
        equations.shift(DOWN)

        phrase1, phrase2, phrase3, phrase4 = phrases = VGroup(
            TexText("If $x_1$ solves it:", t2c=t2c),
            TexText("and $x_2$ solves it:", t2c=t2c),
            TexText("Then $(x_1 + x_2)$ solves it:", t2c=t2c),
            TexText("Then $(0.0 x_1 + 2.0 x_2)$ solves it:", t2c=t2c),
        )

        for phrase, eq in zip(phrases, equations):
            phrase.set_max_width(5)
            phrase.next_to(eq, LEFT, LARGE_BUFF)

        eq4.move_to(eq3)
        phrase4.move_to(phrase3)

        kw = dict(edge_to_fix=RIGHT)
        c1_terms = VGroup(phrase4.make_number_changeable("0.0", **kw), *eq4.make_number_changeable("0.0", replace_all=True, **kw))
        c2_terms = VGroup(phrase4.make_number_changeable("2.0", **kw), *eq4.make_number_changeable("2.0", replace_all=True, **kw))

        # Show base equation
        self.play(Write(phrase1), FadeIn(eq1))
        self.wait()
        self.play(
            TransformMatchingTex(eq1.copy(), eq2, key_map={"x_1": "x_2"}, run_time=1, lag_ratio=0.01),
            FadeTransform(phrase1.copy(), phrase2)
        )
        self.wait()
        self.play(
            FadeIn(phrase3, DOWN),
            FadeIn(eq3, DOWN),
        )
        self.wait()
        self.play(
            FadeOut(eq3, 0.5 * DOWN),
            FadeOut(phrase3, 0.5 * DOWN),
            FadeIn(eq4, 0.5 * DOWN),
            FadeIn(phrase4, 0.5 * DOWN),
        )
        for _ in range(8):
            new_c1 = random.random() * 10
            new_c2 = random.random() * 10
            self.play(*(
                ChangeDecimalToValue(c1, new_c1, run_time=1)
                for c1 in c1_terms
            ))
            self.wait(0.5)
            self.play(*(
                ChangeDecimalToValue(c2, new_c2, run_time=1)
                for c2 in c2_terms
            ))
            self.wait(0.5)
