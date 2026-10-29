# ==============================================================================
# Scene:      RuleOfThumb
# Source:     videos/_2020/med_test.py (lines 3253-3441)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RuleOfThumb.py RuleOfThumb -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RuleOfThumb(Scene):
    def construct(self):
        # Add Bayes factor
        t2c = {
            "+": GREEN,
            "\\text{Cancer}": YELLOW,
            "\\text{No cancer}": GREY_B,
            "=": WHITE,
            "\\over": WHITE,
            "{90\\%": GREEN,
            "9\\%}": GREEN,
            "1\\%}": TEAL,
            "{10}": GREEN,
        }
        frac_part = OldTex(
            """
            {P(+ \\, | \\, \\text{Cancer}) \\over
            P(+ \\, | \\, \\text{No cancer})}
            """,
            tex_to_color_map=t2c
        )
        frac_part.add(SurroundingRectangle(
            frac_part, buff=0.1, stroke_width=1, stroke_color=GREY_B
        ))
        ex_part = OldTex(
            "\\text{e.g. } {90\\% \\over 9\\%} = {10}",
            tex_to_color_map=t2c
        )
        ex_part.next_to(frac_part, RIGHT, LARGE_BUFF)

        brace = Brace(frac_part, UP, buff=SMALL_BUFF)
        bf_label = brace.get_text("Bayes factor")
        bf_label.set_color(GREEN)

        bf_group = VGroup(frac_part, ex_part, brace, bf_label)
        bf_group.to_corner(DL)

        self.add(bf_group)

        # Lightbulb
        bulb = Lightbulb()
        condition = OldTexText("If Prior $\\ll$ 1 \\dots", tex_to_color_map={"Prior": YELLOW})
        condition.next_to(bulb, RIGHT, buff=MED_LARGE_BUFF, aligned_edge=DOWN)
        bulb_group = VGroup(bulb, condition)
        bulb_group.center().to_edge(UP)

        self.play(DrawBorderThenFill(bulb, run_time=1))
        self.play(FadeIn(condition, lag_ratio=0.1))
        self.wait()

        # Equation
        equation = OldTexText(
            "Posterior", " $\\approx$ ",
            "(", "Prior", ")", "(", "Bayes factor", ")",
            tex_to_color_map={
                "Prior": YELLOW,
                "Bayes factor": GREEN,
            }
        )
        equation.next_to(bulb_group, DOWN, LARGE_BUFF)

        self.play(Write(equation[:2]), run_time=1)
        self.wait()
        self.play(
            FadeIn(equation.get_parts_by_tex("(")),
            FadeIn(equation.get_parts_by_tex(")")),
            TransformFromCopy(
                condition.get_part_by_tex("Prior"),
                equation.get_part_by_tex("Prior")
            ),
            TransformFromCopy(
                bf_label[0],
                equation.get_part_by_tex("Bayes factor"),
            ),
        )
        self.wait()

        # 1% example
        ex_rhs = OldTex(
            "\\left({1 \\over 100}\\right)({10}) = {1 \\over 10}",
            tex_to_color_map={
                "1 \\over 100": YELLOW,
                "{10}": GREEN,
            }
        )
        ex_rhs.next_to(equation, DOWN, MED_LARGE_BUFF)
        ex_rhs.shift(RIGHT)

        ex_lhs = OldTex("{1 \\over 11} \\approx")
        ex_lhs.next_to(ex_rhs, LEFT)

        self.play(FadeIn(ex_rhs, DOWN))
        self.wait()
        self.play(Write(ex_lhs))
        self.wait()

        # 10% example
        randy = Randolph(height=2)
        randy.next_to(bf_label, UP, SMALL_BUFF)

        self.play(
            FadeOut(ex_lhs), FadeOut(ex_rhs),
            VFadeIn(randy),
            randy.change, "hesitant",
        )
        self.play(Blink(randy))
        self.wait()

        ex2_rhs = OldTex(
            "(10\\%)({10}) = 100\\%",
            tex_to_color_map={
                "10\\%": YELLOW,
                "{10}": GREEN,
                "=": WHITE,
            }
        )
        ex2_rhs.move_to(ex_rhs, LEFT)
        ex2_rhs.shift(0.15 * RIGHT)

        eq_index = ex2_rhs.index_of_part_by_tex("=")
        self.play(
            Write(ex2_rhs[:eq_index]),
            randy.change, "confused",
        )
        self.play(Blink(randy))
        self.play(Write(ex2_rhs[eq_index:]))
        self.wait()
        self.play(Blink(randy))

        ex2_lhs = OldTex("53\\%", "\\approx")
        ex2_lhs.next_to(ex2_rhs, LEFT)
        ex2_lhs.align_to(equation.get_part_by_tex("\\approx"), RIGHT)
        approx_part = ex2_lhs.get_part_by_tex("\\approx")
        approx_part.scale(1.2, about_edge=DL)
        strike = Line(DL, UR).replace(approx_part, stretch=True)
        strike.set_stroke(RED, 6)
        strike.stretch(0.7, 0)
        strike.stretch(1.5, 1)

        self.play(
            Write(ex2_lhs, run_time=1),
            randy.look_at, ex2_lhs,
        )
        self.play(
            randy.change, "sad", ex2_lhs,
            ShowCreation(strike, run_time=0.3)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change, "tired", ex2_lhs,
        )
        self.play(Blink(randy))
        self.wait()

        ex2 = VGroup(ex2_lhs, strike, ex2_rhs)

        # This statement is actually true
        morty = Mortimer()
        morty.replace(randy, dim_to_match=1)
        morty.to_edge(RIGHT, buff=1.5)

        self.play(
            VFadeIn(morty),
            morty.change, "tease", equation,
            FadeOut(ex2, UP),
            FadeOut(VGroup(bulb, condition), UP),
            equation.match_y, randy,
            randy.change, "erm",
        )
        self.play(Blink(morty))

        eq = OldTex("=")
        approx = equation.get_part_by_tex("\\approx")
        eq.replace(approx)

        self.play(
            PiCreatureSays(
                morty, "This equation\\\\is precisely true!",
                bubble_config={"height": 2, "width": 3},
                look_at=randy.eyes,
            ),
            GrowFromPoint(eq, morty.get_corner(UL)),
            FadeOut(approx, 0.25 * DL),
            randy.change, "confused", morty.eyes,
        )
        self.play(Blink(randy))
        self.play(Blink(morty))
        self.wait(3)
