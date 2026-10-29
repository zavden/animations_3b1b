# ==============================================================================
# Scene:      GrowthEquation
# Source:     videos/_2020/covid.py (lines 501-815)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GrowthEquation.py GrowthEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GrowthEquation(Scene):
    def construct(self):
        # Add labels
        N_label = OldTexText("$N_d$", " = Number of cases on a given day", )
        E_label = OldTexText("$E$", " = Average number of people someone infected is exposed to each day")
        p_label = OldTexText("$p$", " = Probability of each exposure becoming an infection")

        N_label[0].set_color(YELLOW)
        E_label[0].set_color(BLUE)
        p_label[0].set_color(TEAL)

        labels = VGroup(
            N_label,
            E_label,
            p_label
        )
        labels.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        labels.set_width(FRAME_WIDTH - 1)
        labels.to_edge(UP)

        for label in labels:
            self.play(FadeInFromDown(label))
            self.wait()

        delta_N = OldTex("\\Delta", "N_d")
        delta_N.set_color(YELLOW)
        eq = OldTex("=")
        eq.center()
        delta_N.next_to(eq, LEFT)

        delta_N_brace = Brace(delta_N, DOWN)
        delta_N_text = delta_N_brace.get_text("Change over a day")

        nep = OldTex("E", "\\cdot", "p", "\\cdot", "N_d")
        nep[4].match_color(N_label[0])
        nep[0].match_color(E_label[0])
        nep[2].match_color(p_label[0])
        nep.next_to(eq, RIGHT)

        self.play(FadeIn(delta_N), FadeIn(eq))
        self.play(
            GrowFromCenter(delta_N_brace),
            FadeIn(delta_N_text, 0.5 * UP),
        )
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(N_label[0], nep[4]),
            TransformFromCopy(E_label[0], nep[0]),
            TransformFromCopy(p_label[0], nep[2]),
            FadeIn(nep[1]),
            FadeIn(nep[3]),
            lag_ratio=0.2,
            run_time=2,
        ))
        self.wait()
        self.play(ShowCreationThenFadeAround(
            nep[-1],
            surrounding_rectangle_config={"color": RED},
        ))

        # Recursive equation
        lhs = OldTex("N_{d + 1}", "=")
        lhs[0].set_color(YELLOW)
        lhs.move_to(eq, RIGHT)
        lhs.shift(DOWN)

        rhs = VGroup(
            nep[-1].copy(),
            OldTex("+"),
            nep.copy(),
        )
        rhs.arrange(RIGHT)
        rhs.next_to(lhs, RIGHT)

        self.play(
            FadeOut(delta_N_brace),
            FadeOut(delta_N_text),
            FadeIn(lhs, UP),
        )
        self.play(FadeIn(rhs[:2]))
        self.play(TransformFromCopy(nep, rhs[2]))
        self.wait()

        alt_rhs = OldTex(
            "(", "1", "+", "E", "\\cdot", "p", ")", "N_d",
            tex_to_color_map={
                "E": BLUE,
                "p": TEAL,
                "N_d": YELLOW,
            }
        )
        new_lhs = lhs.copy()
        new_lhs.shift(DOWN)
        alt_rhs.next_to(new_lhs, RIGHT)
        self.play(TransformFromCopy(lhs, new_lhs))

        self.play(
            TransformFromCopy(rhs[0], alt_rhs[7].copy()),
            TransformFromCopy(rhs[2][4], alt_rhs[7]),
        )
        self.play(
            TransformFromCopy(rhs[1][0], alt_rhs[2]),
            TransformFromCopy(rhs[2][0], alt_rhs[3]),
            TransformFromCopy(rhs[2][1], alt_rhs[4]),
            TransformFromCopy(rhs[2][2], alt_rhs[5]),
            TransformFromCopy(rhs[2][3], alt_rhs[6]),
            FadeIn(alt_rhs[0]),
            FadeIn(alt_rhs[1]),
        )
        self.wait()

        # Comment on factor
        brace = Brace(alt_rhs[:7], DOWN)
        text = OldTexText("For example, ", "1.15")
        text.next_to(brace, DOWN)
        self.play(
            GrowFromCenter(brace),
            FadeIn(text, 0.5 * UP)
        )
        self.wait()

        # Show exponential
        eq_group = VGroup(
            delta_N, eq, nep,
            lhs, rhs,
            new_lhs, alt_rhs,
            brace,
            text,
        )
        self.clear()
        self.add(labels, eq_group)

        self.play(ShowCreationThenFadeAround(
            VGroup(delta_N, eq, nep),
            surrounding_rectangle_config={"color": RED},
        ))
        self.play(ShowCreationThenFadeAround(
            VGroup(new_lhs, alt_rhs, brace, text),
            surrounding_rectangle_config={"color": RED},
        ))
        self.wait()
        self.play(eq_group.to_edge, LEFT, LARGE_BUFF)

        exp_eq = OldTex(
            "N_d = (1 + E \\cdot p)^{d} \\cdot N_0",
            tex_to_color_map={
                "N_d": YELLOW,
                "E": BLUE,
                "p": TEAL,
                "{d}": YELLOW,
                "N_0": YELLOW,
            }
        )
        exp_eq.next_to(alt_rhs, RIGHT, buff=3)
        arrow = Arrow(alt_rhs.get_right(), exp_eq.get_left())

        self.play(
            GrowArrow(arrow),
            FadeIn(exp_eq, 2 * LEFT)
        )
        self.wait()

        # Discuss factor in front of N
        ep = nep[:3]
        ep_rect = SurroundingRectangle(ep)
        ep_rect.set_stroke(RED, 2)

        ep_label = OldTexText("This factor will decrease")
        ep_label.next_to(ep_rect, UP, aligned_edge=LEFT)
        ep_label.set_color(RED)

        self.play(
            ShowCreation(ep_rect),
            FadeIn(ep_label, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            FadeOut(ep_rect),
            FadeOut(ep_label),
        )

        # Add carrying capacity factor to p
        p_factors = OldTex(
            "\\left(1 - {N_d \\over \\text{pop. size}} \\right)",
            tex_to_color_map={"N_d": YELLOW},
        )
        p_factors.next_to(nep, RIGHT, buff=3)
        p_factors_rect = SurroundingRectangle(p_factors)
        p_factors_rect.set_stroke(TEAL, 2)
        p_arrow = Arrow(
            p_factors_rect.get_corner(UL),
            nep[2].get_top(),
            path_arc=75 * DEGREES,
            color=TEAL,
        )

        self.play(
            ShowCreation(p_factors_rect),
            ShowCreation(p_arrow)
        )
        self.wait()
        self.play(Write(p_factors))
        self.wait()
        self.play(
            FadeOut(p_factors),
            FadeOut(p_arrow),
            FadeOut(p_factors_rect),
        )

        # Ask about ep shrinking
        ep_question = OldTexText("What makes this shrink?")
        ep_question.set_color(RED)
        ep_question.next_to(ep_rect, UP, aligned_edge=LEFT)

        E_line = Underline(E_label)
        E_line.set_color(BLUE)
        p_line = Underline(p_label)
        p_line.set_color(TEAL)

        self.play(
            ShowCreation(ep_rect),
            FadeIn(ep_question, LEFT)
        )
        self.wait()
        for line in E_line, p_line:
            self.play(ShowCreation(line))
            self.wait()
            self.play(FadeOut(line))
        self.wait()

        # Show alternate projections
        ep_value = DecimalNumber(0.15)
        ep_value.next_to(ep_rect, UP)

        self.play(
            FadeOut(ep_question),
            FadeIn(ep_value),
            FadeOut(text[0]),
            text[1].next_to, brace, DOWN,
        )

        eq1 = OldTex("(", "1.15", ")", "^{61}", "\\cdot", "21{,}000", "=")
        eq2 = OldTex("(", "1.05", ")", "^{61}", "\\cdot", "21{,}000", "=")
        eq1_rhs = Integer((1.15**61) * (21000))
        eq2_rhs = Integer((1.05**61) * (21000))

        for eq, rhs in (eq1, eq1_rhs), (eq2, eq2_rhs):
            eq[1].set_color(RED)
            eq.move_to(nep)
            eq.to_edge(RIGHT, buff=3)
            rhs.next_to(eq, RIGHT)
            rhs.align_to(eq[-2], UP)

        self.play(FadeIn(eq1))
        for tex in ["21{,}000", "61"]:
            self.play(ShowCreationThenFadeOut(
                Underline(
                    eq1.get_part_by_tex(tex),
                    stroke_color=YELLOW,
                    stroke_width=2,
                    buff=SMALL_BUFF,
                ),
                run_time=2,
            ))
        value = eq1_rhs.get_value()
        eq1_rhs.set_value(0)
        self.play(ChangeDecimalToValue(eq1_rhs, value))
        self.wait()
        eq1.add(eq1_rhs)
        self.play(
            eq1.shift, DOWN,
            FadeIn(eq2),
        )

        new_text = OldTexText("1.05")
        new_text.move_to(text[1])
        self.play(
            ChangeDecimalToValue(ep_value, 0.05),
            FadeOut(text[1]),
            FadeIn(new_text),
        )

        self.wait()

        eq2_rhs.align_to(eq1_rhs, RIGHT)
        value = eq2_rhs.get_value()
        eq2_rhs.set_value(0)
        self.play(ChangeDecimalToValue(eq2_rhs, value))
        self.wait()

        # Pi creature quote
        morty = Mortimer()
        morty.set_height(1)
        morty.next_to(eq2_rhs, UP)
        bubble = SpeechBubble(
            direction=RIGHT,
            height=2.5,
            width=5,
        )
        bubble.next_to(morty, UL, buff=0)
        bubble.write("The only thing to fear\\\\is the lack of fear itself.")

        self.add(morty)
        self.add(bubble)
        self.add(bubble.content)

        self.play(
            labels.set_opacity, 0.5,
            VFadeIn(morty),
            morty.change, "speaking",
            FadeIn(bubble),
            Write(bubble.content),
        )
        self.play(Blink(morty))
        self.wait()
