# ==============================================================================
# Scene:      IntegrateByParts
# Source:     videos/_2025/laplace/derivatives.py (lines 1732-1824)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegrateByParts.py IntegrateByParts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegrateByParts(InteractiveScene):
    def construct(self):
        # Show formulas
        t2c = {"{t}": BLUE, "{s}": YELLOW}
        ibp_rule = VGroup(
            Text("Integration by parts: "),
            Tex(R"\int u dv = uv - \int v du", t2c={"u": PINK, "v": RED})
        )
        ibp_rule.arrange(RIGHT, buff=MED_LARGE_BUFF)
        ibp_rule.to_edge(UP, buff=MED_LARGE_BUFF)

        lt_deriv_lines = VGroup(
            Tex(R"\mathcal{L}\big\{f'({t})\big\} =\int_0^\infty f'({t}) e^{\minus {s}{t}} d{t}", t2c=t2c),
            Tex(R"=\Big[f({t}) e^{\minus {s}{t}} \Big]_0^\infty - \int_0^\infty f({t}) (-{s}) e^{\minus {s}{t}} d{t}", t2c=t2c),
            Tex(R"=-f(0) + {s} \int_0^\infty f({t}) e^{\minus {s}{t}} d{t}", t2c=t2c),
            Tex(R"={s} \mathcal{L}\big\{f({t})\big\} -f(0)", t2c=t2c),
        )
        lt_deriv_lines.arrange(DOWN, aligned_edge=LEFT)
        lt_deriv_lines[1:].align_to(lt_deriv_lines[0]["="], LEFT)
        lt_deriv_lines.next_to(ibp_rule, DOWN, LARGE_BUFF, aligned_edge=LEFT)

        # Show Definition
        definition = lt_deriv_lines[0]
        definition.save_state()
        definition.set_height(1.6).center()
        eq_index = definition.submobjects.index(definition["="][0][0])

        def_brace = Brace(definition[eq_index:], UP)
        def_words = Text("Definition", font_size=60)
        def_words.next_to(def_brace, UP)

        self.add(definition[:eq_index])
        self.wait()
        self.play(LaggedStart(
            Transform(*definition["f'({t})"].copy(), path_arc=60 * DEG, remover=True),
            GrowFromCenter(def_brace),
            FadeIn(def_words, 0.5 * UP),
            Write(definition[eq_index:], lag_ratio=0.1),
            lag_ratio=0.2
        ))
        self.wait()
        self.play(LaggedStart(
            Transform(
                definition[R"\int"][0].copy(),
                ibp_rule[1][R"\int"][0].copy(),
                remover=True,
                path_arc=-45 * DEG,
            ),
            FadeOut(def_brace),
            FadeOut(def_words),
            FadeIn(ibp_rule, lag_ratio=0.1),
            lag_ratio=0.2
        ))
        self.wait()

        # Show remaining lines
        self.play(Restore(definition))
        self.play(
            FadeTransform(ibp_rule[1][4:].copy(), lt_deriv_lines[1])
        )
        self.wait()
        for line in lt_deriv_lines[2:]:
            self.play(FadeIn(line, 0.5 * DOWN))
            self.wait()

        # Ask about times s and minus f(0)
        final_line = lt_deriv_lines[-1]
        s_rect = SurroundingRectangle(final_line["{s}"][0], buff=0.05)
        s_rect.set_stroke(YELLOW, 2)
        minus_f0_rect = SurroundingRectangle(final_line["-f(0)"][0], buff=0.05)
        minus_f0_rect.set_stroke(BLUE, 2)

        why = Text("Why?")
        why.next_to(s_rect, LEFT, buff=1.5).shift(0.5 * UP)
        why_arrow = Arrow(why.get_right() + SMALL_BUFF * RIGHT, s_rect.get_top(), path_arc=-90 * DEG, buff=0.05)
        VGroup(why, why_arrow).set_color(YELLOW)

        why2 = Text("Why?")
        why2.next_to(minus_f0_rect, RIGHT)
        why2.set_color(BLUE)

        self.play(
            Write(why),
            Write(why_arrow),
            ShowCreation(s_rect),
            lt_deriv_lines[1:3].animate.set_fill(opacity=0.3),
        )
        self.wait()
        self.play(
            ShowCreation(minus_f0_rect),
            Write(why2),
        )
        self.wait()
