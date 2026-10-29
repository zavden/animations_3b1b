# ==============================================================================
# Scene:      SwapIntegralAndSum
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1201-1732)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SwapIntegralAndSum.py SwapIntegralAndSum -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth

class SwapIntegralAndSum(Scene):
    def construct(self):
        self.perform_swap()
        self.show_average_of_individual_terms()
        self.ask_about_c2()
        self.multiply_f_by_exp_neg_2()
        self.show_modified_averages()
        self.add_general_expression()

    def perform_swap(self):
        light_pink = self.light_pink = interpolate_color(
            PINK, WHITE, 0.25
        )
        tex_config = self.tex_config = {
            "tex_to_color_map": {
                "=": WHITE,
                "\\int_0^1": WHITE,
                "+": WHITE,
                "\\cdots": WHITE,
                "{t}": PINK,
                "{dt}": light_pink,
                "{-2}": YELLOW,
                "{\\cdot 1}": YELLOW,
                "{0}": YELLOW,
                "{1}": YELLOW,
                "{2}": YELLOW,
                "{n}": YELLOW,
            },
        }
        int_ft = OldTex(
            "\\int_0^1 f({t}) {dt}",
            **tex_config
        )
        int_sum = OldTex(
            """
            =
            \\int_0^1 \\left(
            \\cdots +
            c_{\\cdot 1}e^{{\\cdot 1} \\cdot 2\\pi i {t}} +
            c_{0}e^{{0} \\cdot 2\\pi i {t}} +
            c_{1}e^{{1} \\cdot 2\\pi i {t}} +
            c_{2}e^{{2} \\cdot 2\\pi i {t}} +
            \\cdots
            \\right){dt}
            """,
            **tex_config
        )
        sum_int = OldTex(
            """
            = \\cdots +
            \\int_0^1
            c_{\\cdot 1}e^{{\\cdot 1} \\cdot 2\\pi i {t}}
            {dt} +
            \\int_0^1
            c_{0}e^{{0} \\cdot 2\\pi i {t}}
            {dt} +
            \\int_0^1
            c_{1}e^{{1} \\cdot 2\\pi i {t}}
            {dt} +
            \\int_0^1
            c_{2}e^{{2} \\cdot 2\\pi i {t}}
            {dt} +
            \\cdots
            """,
            **tex_config
        )

        self.fix_minuses(int_sum)
        self.fix_minuses(sum_int)

        group = VGroup(int_ft, int_sum, sum_int)
        group.arrange(
            DOWN, buff=MED_LARGE_BUFF,
            aligned_edge=LEFT
        )
        group.set_width(FRAME_WIDTH - 1)
        group.to_corner(UL)
        int_ft.align_to(int_sum[1], LEFT)
        int_ft.shift(0.2 * RIGHT)

        int_sum.exp_terms = self.get_exp_terms(int_sum)
        sum_int.exp_terms = self.get_exp_terms(sum_int)
        sum_int.int_terms = self.get_integral_terms(sum_int)

        breakdown_label = OldTexText(
            "Break this down"
        )
        arrow = Vector(LEFT)
        arrow.next_to(int_ft, RIGHT)
        breakdown_label.next_to(arrow, RIGHT)

        aos_label = OldTexText(
            "Average of a sum",
            tex_to_color_map={
                "Average": light_pink,
                "sum": YELLOW,
            }
        )
        soa_label = OldTexText(
            "Sum over averages",
            tex_to_color_map={
                "averages": light_pink,
                "Sum": YELLOW,
            }
        )
        aos_label.next_to(ORIGIN, RIGHT, buff=2)
        aos_label.to_edge(UP)
        soa_label.move_to(2.5 * DOWN)
        aos_arrow = Arrow(
            aos_label.get_corner(DL),
            int_sum.get_corner(TOP) + 2 * RIGHT,
            buff=0.3,
        )
        soa_arrow = Arrow(
            soa_label.get_top(),
            sum_int.get_bottom(),
            buff=0.3,
        )

        self.add(int_ft)
        self.play(
            FadeIn(breakdown_label, LEFT),
            GrowArrow(arrow),
        )
        self.wait()
        self.play(
            FadeOut(breakdown_label),
            FadeOut(arrow),
            FadeIn(int_sum.get_parts_by_tex("=")),
            FadeIn(int_sum.get_parts_by_tex("+")),
            FadeIn(int_sum.get_parts_by_tex("\\cdots")),
            FadeIn(int_sum.get_parts_by_tex("(")),
            FadeIn(int_sum.get_parts_by_tex(")")),
            *[
                TransformFromCopy(
                    int_ft.get_part_by_tex(tex),
                    int_sum.get_part_by_tex(tex),
                )
                for tex in ["\\int_0^1", "{dt}"]
            ]
        )
        self.play(LaggedStart(*[
            GrowFromPoint(
                term,
                int_ft.get_part_by_tex("{t}").get_center(),
            )
            for term in int_sum.exp_terms
        ]))
        self.wait()
        self.play(
            FadeIn(aos_label),
            GrowArrow(aos_arrow)
        )
        self.play(
            *[
                TransformFromCopy(
                    int_sum.get_parts_by_tex(tex),
                    sum_int.get_parts_by_tex(tex),
                    run_time=2,
                )
                for tex in ["\\cdots", "+"]
            ],
            TransformFromCopy(
                int_sum.exp_terms,
                sum_int.exp_terms,
                run_time=2,
            ),
            FadeIn(soa_label),
            GrowArrow(soa_arrow),
        )
        self.play(
            *[
                TransformFromCopy(
                    int_sum.get_part_by_tex("\\int_0^1"),
                    part,
                    run_time=2,
                )
                for part in sum_int.get_parts_by_tex(
                    "\\int_0^1"
                )
            ],
            FadeIn(sum_int.get_parts_by_tex("{dt}"))
        )
        self.wait()
        self.play(
            FadeOut(soa_arrow),
            soa_label.to_edge, DOWN,
        )

        self.int_sum = int_sum
        self.sum_int = sum_int
        self.int_ft = int_ft
        self.aos_label = aos_label
        self.aos_arrow = aos_arrow
        self.soa_label = soa_label
        self.soa_arrow = soa_arrow

    def show_average_of_individual_terms(self):
        sum_int = self.sum_int
        int_ft = self.int_ft

        braces = VGroup(*[
            Brace(term, DOWN, buff=SMALL_BUFF)
            for term in sum_int.int_terms
        ])
        self.play(LaggedStartMap(
            GrowFromCenter, braces
        ))

        self.show_individual_average(braces[0], -1)
        self.show_individual_average(braces[2], 1)
        self.show_individual_average(braces[3], 2)
        self.show_individual_average(braces[1], 0)

        eq = OldTex("=")
        eq.next_to(int_ft, RIGHT)
        c0 = self.c0.copy()
        c0.generate_target()
        c0.target.next_to(eq, RIGHT)
        c0.target.shift(0.05 * DOWN)
        self.play(
            FadeIn(eq),
            MoveToTarget(c0, run_time=2)
        )
        self.wait()

        self.braces = braces
        self.eq_c0 = VGroup(eq, c0)

    def ask_about_c2(self):
        int_sum = self.int_sum
        sum_int = self.sum_int

        c2 = int_sum.exp_terms[-1][:2]
        c2_rect = SurroundingRectangle(c2, buff=0.05)
        c2_rect.set_stroke(WHITE, 2)
        c2_rect.stretch(1.5, 1, about_edge=DOWN)

        q_marks = OldTex("???")
        q_marks.next_to(c2_rect, UP)

        last_diagram = self.all_average_diagrams[-2]
        last_int = sum_int.int_terms[-1]
        big_rect = SurroundingRectangle(
            VGroup(last_int, last_diagram)
        )
        big_rect.set_stroke(WHITE, 2)

        self.play(
            ShowCreation(c2_rect),
            FadeOut(self.aos_arrow),
            FadeInFromDown(q_marks),
        )
        self.play(ShowCreation(big_rect))
        self.wait(2)
        self.to_fade = VGroup(c2_rect, q_marks, big_rect)

    def multiply_f_by_exp_neg_2(self):
        int_ft = self.int_ft
        int_sum = self.int_sum
        sum_int = self.sum_int
        eq_c0 = self.eq_c0
        diagrams = self.all_average_diagrams
        diagrams.sort(lambda p: p[0])

        dt_part = int_ft.get_part_by_tex("{dt}")
        pre_dt_part = int_ft[:-1]
        new_exp = OldTex(
            "e^{{-2} \\cdot 2\\pi i {t}}",
            **self.tex_config,
        )
        new_exp.next_to(pre_dt_part, RIGHT, SMALL_BUFF)
        new_exp.shift(0.05 * UP)
        something = OldTexText("(something)")
        something.replace(new_exp, dim_to_match=0)
        something.align_to(new_exp, DOWN)

        self.play(
            FadeOut(eq_c0),
            Write(something, run_time=1),
            dt_part.next_to, new_exp, RIGHT, SMALL_BUFF,
            dt_part.align_to, dt_part, DOWN,
        )
        self.wait()
        self.play(*[
            Rotating(
                diagram[2],
                radians=n * TAU,
                about_point=diagram[0].n2p(0),
                run_time=3,
                rate_func=lambda t: smooth(t, 1)
            )
            for n, diagram in zip(it.count(-3), diagrams)
        ])
        self.wait()
        self.play(
            FadeOut(something, UP),
            FadeIn(new_exp, DOWN),
        )
        self.play(FadeOut(self.to_fade))

        # Go through each term
        moving_exp = new_exp.copy()
        rect = SurroundingRectangle(moving_exp)
        rect.set_stroke(GREY_B, width=1)
        times = OldTex("\\times")
        times.next_to(rect, LEFT, SMALL_BUFF)
        moving_exp.add(VGroup(rect, times))
        moving_exp[-1].set_opacity(0)
        moving_exp.save_state()
        moving_exp.generate_target()

        quads = zip(
            it.count(-3),
            int_sum.exp_terms,
            sum_int.exp_terms,
            diagrams,
        )
        for n, c_exp1, c_exp2, diagram in quads:
            exp1 = c_exp1[2:]
            exp2 = c_exp2[2:]
            moving_exp.target[-1][0].set_stroke(opacity=1)
            moving_exp.target[-1][1].set_fill(opacity=1)
            moving_exp.target.next_to(exp1, UP, SMALL_BUFF)
            if n < 0:
                n_str = "{\\cdot" + str(abs(n)) + "}"
            else:
                n_str = "{" + str(n) + "}"
            replacement1 = OldTex(
                "e^{", n_str, "\\cdot 2\\pi i", "{t}",
                tex_to_color_map={
                    "{t}": PINK,
                    n_str: YELLOW,
                }
            )
            self.fix_minuses(replacement1)
            replacement1[1][0].shift(0.025 * LEFT)
            replacement1.match_height(exp1)
            replacement1.move_to(exp1, DL)
            replacement2 = replacement1.copy()
            replacement2.move_to(exp2, DL)
            self.play(MoveToTarget(moving_exp))
            self.play(
                TransformFromCopy(
                    moving_exp[1],
                    replacement1[1],
                ),
                FadeOut(exp1[1], DOWN),
                Transform(exp1[0], replacement1[0]),
                Transform(exp1[2:], replacement1[2:]),
            )
            self.play(
                TransformFromCopy(replacement1, replacement2),
                FadeOut(exp2, DOWN),
                FadeOut(diagram),
            )
        self.play(Restore(moving_exp))

    def show_modified_averages(self):
        braces = self.braces

        for brace, n in zip(braces, it.count(-3)):
            self.show_individual_average(brace, n, "c_2")

        int_ft = self.int_ft
        c2 = self.c0.copy()
        c2.generate_target()
        eq = OldTex("=")
        eq.next_to(int_ft, RIGHT)
        c2.target.next_to(eq, RIGHT)
        c2.target.shift(0.05 * DOWN)
        self.play(
            FadeIn(eq),
            MoveToTarget(c2)
        )
        self.wait()

    def add_general_expression(self):
        expression = OldTex(
            """
            c_{n} =
            \\int_0^1 f({t})
            e^{-{n} \\cdot 2\\pi i {t}}{dt}
            """,
            **self.tex_config,
        )
        rect = SurroundingRectangle(expression, buff=MED_SMALL_BUFF)
        rect.set_fill(GREY_D, 1)
        rect.set_stroke(WHITE, 3)
        group = VGroup(rect, expression)
        group.to_edge(UP, buff=SMALL_BUFF)
        group.to_edge(RIGHT, buff=LARGE_BUFF)

        self.play(
            FadeOut(self.aos_label),
            FadeIn(rect),
            FadeIn(expression)
        )
        self.wait()

    #
    def show_individual_average(self, brace, n, cn_tex=None):
        if not hasattr(self, "all_average_diagrams"):
            self.all_average_diagrams = VGroup()

        seed = brace.get_center()[0] + 1
        int_seed = np.array([seed]).astype("uint32")
        np.random.seed(int_seed)
        if n == 0:
            if cn_tex is None:
                cn_tex = "c_" + str(n)
            result = OldTex(cn_tex)
            result[0][1].set_color(YELLOW)
            self.c0 = result
        else:
            result = OldTex("0")
            result.set_color(self.light_pink)
        result.next_to(brace, DOWN, SMALL_BUFF)

        coord_max = 1.25
        plane = ComplexPlane(
            x_min=-coord_max,
            x_max=coord_max,
            y_min=-coord_max,
            y_max=coord_max,
            axis_config={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "unit_size": 0.75,
            },
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
            },
        )
        plane.next_to(result, DOWN, SMALL_BUFF)

        vector = Arrow(
            plane.n2p(0),
            plane.n2p(
                (0.2 + 0.8 * np.random.random()) * np.exp(complex(
                    0, TAU * np.random.random()
                ))
            ),
            buff=0,
            color=WHITE,
        )
        circle = Circle()
        circle.set_stroke(BLUE, 2)
        circle.rotate(vector.get_angle())
        circle.set_width(2 * vector.get_length())
        circle.move_to(plane.n2p(0))

        dots = VGroup(*[
            Dot(
                circle.point_from_proportion(
                    (n * a) % 1
                ),
                radius=0.04,
                color=PINK,
                fill_opacity=0.75,
            )
            for a in np.arange(0, 1, 1 / 25)
        ])
        dot_center = center_of_mass([
            d.get_center() for d in dots
        ])

        self.play(
            FadeIn(plane),
            FadeIn(circle),
            FadeIn(vector),
        )
        self.play(
            Rotating(
                vector,
                radians=n * TAU,
                about_point=plane.n2p(0),
            ),
            ShowIncreasingSubsets(
                dots,
                int_func=np.ceil,
            ),
            rate_func=lambda t: smooth(t, 1),
            run_time=3,
        )
        dot_copies = dots.copy()
        self.play(*[
            ApplyMethod(dot.move_to, dot_center)
            for dot in dot_copies
        ])
        self.play(
            TransformFromCopy(dot_copies[0], result)
        )
        self.wait()

        self.all_average_diagrams.add(VGroup(
            plane, circle, vector,
            dots, dot_copies, result,
        ))

    #
    def fix_minuses(self, tex_mob):
        for mob in tex_mob.get_parts_by_tex("{\\cdot"):
            minus = OldTex("-")
            minus.match_style(mob[0])
            minus.set_width(
                3 * mob[0].get_width(),
                stretch=True,
            )
            minus.move_to(mob, LEFT)
            mob.submobjects[0] = minus

    def get_terms_by_tex_bounds(self, tex_mob, tex1, tex2):
        c_parts = tex_mob.get_parts_by_tex(tex1)
        t_parts = tex_mob.get_parts_by_tex(tex2)
        result = VGroup()
        for p1, p2 in zip(c_parts, t_parts):
            i1 = tex_mob.index_of_part(p1)
            i2 = tex_mob.index_of_part(p2)
            result.add(tex_mob[i1:i2 + 1])
        return result

    def get_exp_terms(self, tex_mob):
        return self.get_terms_by_tex_bounds(
            tex_mob, "c_", "{t}"
        )

    def get_integral_terms(self, tex_mob):
        return self.get_terms_by_tex_bounds(
            tex_mob, "\\int", "{dt}"
        )
