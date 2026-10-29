# ==============================================================================
# Scene:      WalkThroughEquationSolution
# Source:     videos/_2025/laplace/derivatives.py (lines 807-1374)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WalkThroughEquationSolution.py WalkThroughEquationSolution -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewStrategy(InteractiveScene):
    def construct(self):
        # Set up terms
        rect = Rectangle(6, 4)
        ode, lt_ode, lt_ans, ans = terms = VGroup(
            Text("Differential\nEquation"),
            Text("Transformed\nEquation"),
            Text("Transformed\nSolution"),
            Text("Solution"),
        )
        VGroup(lt_ode, lt_ans).set_color(YELLOW)
        for term, corner in zip(terms, [UL, DL, DR, UR]):
            term.move_to(rect.get_corner(corner))

        # Set up arrows
        lt_arrow = self.get_lt_arrow(ode, lt_ode, buff=MED_SMALL_BUFF)
        solve_arrow = self.get_lt_arrow(lt_ode, lt_ans, label_tex=R"\substack{\text{Solve} \\ \text{(Algebraically)}}")
        solve_arrow[1][:5].scale(1.5, about_edge=DOWN).shift(0.1 * UP)
        inv_lt_arrow = self.get_lt_arrow(lt_ans, ans, label_tex=R"\mathcal{L}^{-1}", buff=MED_SMALL_BUFF)

        arrows = VGroup(lt_arrow, solve_arrow, inv_lt_arrow)

        # Show creation of terms
        self.add(ode)
        self.wait()
        self.play(
            self.grow_lt_arrow(lt_arrow),
            TransformMatchingStrings(ode.copy(), lt_ode, key_map={"Differential": "Transformed"}),
            run_time=1.5
        )
        self.wait()
        self.play(
            self.grow_lt_arrow(solve_arrow),
            FadeTransform(lt_ode.copy(), lt_ans),
            run_time=1.5
        )
        self.wait()
        self.play(
            self.grow_lt_arrow(inv_lt_arrow),
            FadeTransform(lt_ans["Solution"][0].copy(), ans),
            run_time=1.5
        )
        self.wait()

        # Add domain backgrounds
        time_domain = FullScreenRectangle()
        time_domain.stretch(0.55, 1, about_edge=UP)
        time_domain.set_stroke(BLUE, 3)
        time_domain.set_fill(opacity=0)
        s_domain = FullScreenRectangle()
        s_domain.stretch(0.45, 1, about_edge=DOWN)
        s_domain.set_stroke(YELLOW, 3)
        s_domain.set_fill(opacity=0)

        time_label = Text("Time domain")
        s_label = Text("s domain")
        s_label.set_fill(YELLOW)

        for label, domain in [(time_label, time_domain), (s_label, s_domain)]:
            label.next_to(domain.get_corner(UL), DR)

        self.play(LaggedStart(
            FadeIn(time_domain),
            FadeIn(time_label),
            FadeIn(s_domain),
            FadeIn(s_label),
        ))
        self.wait()

    def get_lt_arrow(self, m1, m2, thickness=4, label_font_size=36, buff=0.15, label_tex=R"\mathcal{L}"):
        arrow = Arrow(m1, m2, buff=buff, thickness=thickness)
        arrow.set_fill(border_width=2)
        label = Tex(label_tex, font_size=label_font_size)
        label.move_to(arrow.get_center())
        shift_dir = rotate_vector(normalize(arrow.get_vector()), 90 * DEG)
        label.shift(1.25 * label.get_height() * shift_dir)
        return VGroup(arrow, label)

    def grow_lt_arrow(self, lt_arrow):
        return AnimationGroup(
            GrowArrow(lt_arrow[0]),
            FadeIn(lt_arrow[1], shift=0.25 * lt_arrow[0].get_vector())
        )


class WalkThroughEquationSolution(PreviewStrategy):
    def construct(self):
        # Add ode
        x_colors, t2c = self.get_x_colors_and_t2c()
        ode = Tex(R"m x''(t) + \mu x'(t) + k x(t) = F_0 \cos(\omega t)", t2c=t2c)
        ode.to_edge(UP)

        xt = ode["x(t)"][0]
        dxt = ode["x'(t)"][0]
        ddxt = ode["x''(t)"][0]
        xt_group = VGroup(xt, dxt, ddxt)

        self.add(ode)

        # Transform of the full equation
        ode_lt_lhs = Tex(R"""
            m\Big({s}^2 X({s}) - {s} x_0 - v_0 \Big)
            + \mu \Big( {s} X({s}) - x_0 \Big)
            + k X({s})
        """, t2c=t2c)
        factored_ode_lt_lhs = Tex(R"""
            X({s})\big(m{s}^2 + \mu{s} + k\big)
            - m v_0 - (m{s} + \mu)x_0
        """, t2c=t2c)
        ode_lt_lhs.next_to(xt_group, DOWN, buff=1.5)
        factored_ode_lt_lhs.next_to(ode_lt_lhs, DOWN, buff=1.5)

        x_lt = ode_lt_lhs[R"X({s})"][-1]
        dx_lt = ode_lt_lhs[R"{s} X({s}) - x_0"][-1]
        ddx_lt = ode_lt_lhs[R"{s}^2 X({s}) - {s} x_0 - v_0"][0]
        x_lt_parts = VGroup(x_lt, dx_lt, ddx_lt)

        # Show each transform
        for part in x_lt_parts:
            part.save_state()
        x_lt_parts[:2].match_x(xt_group)

        xt_rect = SurroundingRectangle(xt, buff=0.05)
        dxt_rect = SurroundingRectangle(dxt, buff=0.05)
        ddxt_rect = SurroundingRectangle(ddxt, buff=0.05)
        xt_rects = VGroup(xt_rect, dxt_rect, ddxt_rect)
        for rect, color in zip(xt_rects, x_colors):
            rect.set_stroke(color, width=2)

        xt_arrow = self.get_lt_arrow(xt_rect, x_lt)
        dxt_arrow = self.get_lt_arrow(dxt_rect, dx_lt)
        ddx_arrow = self.get_lt_arrow(ddxt_rect, ddx_lt)

        self.play(ShowCreation(xt_rect))
        self.play(
            self.grow_lt_arrow(xt_arrow),
            FadeTransform(xt.copy(), x_lt)
        )
        self.wait()
        self.play(ShowCreation(dxt_rect))
        self.play(
            self.grow_lt_arrow(dxt_arrow),
            FadeTransform(dxt.copy(), dx_lt)
        )
        self.wait()

        # Ask about L{x''(t)}
        ddx_lt_rect = SurroundingRectangle(ddx_lt, buff=SMALL_BUFF)
        ddx_lt_rect.set_stroke(RED, 1)

        self.play(ShowCreation(ddxt_rect)),
        self.play(LaggedStart(
            self.grow_lt_arrow(ddx_arrow),
            TransformFromCopy(ddxt_rect, ddx_lt_rect),
            Restore(x_lt),
            Transform(xt_arrow, self.get_lt_arrow(xt_rect, x_lt.saved_state)),
            Restore(dx_lt),
            Transform(dxt_arrow, self.get_lt_arrow(dxt_rect, dx_lt.saved_state)),
        ))
        self.wait()

        # Show second derivative rule
        ddx_lt_lhs = Tex(R"\mathcal{L}\Big\{x''(t)\Big\}", t2c=t2c)
        ddx_lt_rhss = VGroup(
            Tex(R"= {s} \mathcal{L}\Big\{x'(t)\Big\} - x'(0)", t2c=t2c),
            Tex(R"= {s} \mathcal{L}\Big\{x'(t)\Big\} - v_0", t2c=t2c),
            Tex(R"= {s} \Big({s}X({s}) - x_0 \Big) - v_0", t2c=t2c),
            Tex(R"= {s}^2 X({s}) - {s} x_0 - v_0", t2c=t2c),
        )
        ddx_lt_lhs.to_edge(DOWN, buff=1.5)
        ddx_lt_lhs.to_edge(LEFT, buff=2.0)
        for rhs in ddx_lt_rhss:
            rhs.next_to(ddx_lt_lhs, RIGHT)
        for rhs in ddx_lt_rhss[2:]:
            rhs.next_to(ddx_lt_rhss[1], RIGHT)

        v0_rect = SurroundingRectangle(ddx_lt_rhss[0][R"x'(0)"])
        v0_rect.set_stroke(x_colors[1], 2)

        self.play(
            TransformFromCopy(ddx_arrow[1], ddx_lt_lhs[0]),
            TransformFromCopy(ddxt, ddx_lt_lhs[R"x''(t)"][0]),
            Write(ddx_lt_lhs[R"\Big\{"]),
            Write(ddx_lt_lhs[R"\Big\}"]),
        )
        self.wait()
        self.play(
            TransformMatchingTex(ddx_lt_lhs.copy(), ddx_lt_rhss[0], path_arc=30 * DEG, run_time=1)
        )
        self.wait()
        self.play(ShowCreation(v0_rect))
        self.play(
            TransformMatchingTex(
                ddx_lt_rhss[0],
                ddx_lt_rhss[1],
                matched_keys=[R"= {s} \mathcal{L}\Big\{x'(t)\Big\} - "],
                key_map={R"x'(0)": R"v_0"},
                run_time=1,
            ),
            v0_rect.animate.surround(ddx_lt_rhss[1][R"v_0"])
        )
        self.play(FadeOut(v0_rect))
        self.wait()
        self.play(
            TransformMatchingTex(
                ddx_lt_rhss[1].copy(),
                ddx_lt_rhss[2],
                key_map={R"\mathcal{L}\Big\{x'(t)\Big\}": R"\Big({s}X({s}) - x_0 \Big)"},
                matched_keys=[R"- v_0"],
                run_time=1.5,
                path_arc=30 * DEG,
            ),
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                ddx_lt_rhss[2],
                ddx_lt_rhss[3],
                matched_keys=[R"- v_0", "x_0", "X({s})"],
                run_time=1.5,
                path_arc=30 * DEG,
            ),
        )
        self.wait()
        self.play(
            FadeOut(ddx_lt_lhs),
            FadeOut(ddx_lt_rhss[1]),
            FadeOut(ddx_lt_rhss[3][0]),
            FadeTransform(ddx_lt_rhss[3][1:], ddx_lt),
            run_time=2
        )
        self.play(FadeOut(ddx_lt_rect))
        self.wait()

        # Bring along constants
        eq_index = ode.submobjects.index(ode["="][0][0])
        ode_lhs_rect = SurroundingRectangle(ode[:eq_index])
        ode_lhs_rect.set_stroke(BLUE, 2)
        ode_lt_lhs_rect = SurroundingRectangle(ode_lt_lhs)
        ode_lt_lhs_rect.set_stroke(YELLOW, 2)
        lhs_arrow = self.get_lt_arrow(ode_lhs_rect, ode_lt_lhs_rect.copy().shift(0.5 * RIGHT))

        self.play(
            LaggedStart(
                *(
                    TransformFromCopy(ode[tex][0], ode_lt_lhs[tex][0])
                    for tex in ["m", R"\mu", "k"]
                ),
                lag_ratio=0.5
            ),
            AnimationGroup(*(
                FadeIn(ode_lt_lhs[tex])
                for tex in [R"\Big(", R"\Big)", "+"]
            ))
        )
        self.wait()
        self.play(LaggedStart(
            FadeOut(xt_arrow),
            FadeOut(ddx_arrow),
            FadeOut(xt_rect),
            FadeOut(ddxt_rect),
            ReplacementTransform(dxt_rect, ode_lhs_rect),
            ReplacementTransform(dxt_arrow, lhs_arrow),
            FadeIn(ode_lt_lhs_rect),
        ))
        self.wait()

        # Factor out X(s)
        Xs_parts = VGroup(
            ode_lt_lhs[R"m\Big({s}^2 X({s})"][0],
            ode_lt_lhs[R"\mu \Big( {s} X({s})"][0],
            ode_lt_lhs[R"k X({s})"][0],
        )
        Xs_part_rects = VGroup(
            SurroundingRectangle(part, buff=0.1)
            for part in Xs_parts
        )
        Xs_part_rects[2].match_height(Xs_part_rects, stretch=True)
        Xs_part_rects.set_stroke(YELLOW, 2)

        ode_lt_lhs.set_fill(opacity=0.35)
        Xs_parts.set_fill(opacity=1)
        Xs_parts[0][1].set_fill(opacity=0.25)
        Xs_parts[1][1].set_fill(opacity=0.25)
        ode_lt_lhs.save_state()
        ode_lt_lhs.set_fill(opacity=1)

        self.remove(ode_lt_lhs_rect)
        self.play(
            FadeOut(ode_lt_lhs_rect),
            FadeIn(Xs_part_rects),
            Restore(ode_lt_lhs),
            lhs_arrow.animate.scale(0.75, about_edge=UL)
        )
        self.wait()
        self.play(LaggedStart(
            *[
                TransformFromCopy(ode_lt_lhs[tex][index0], factored_ode_lt_lhs[tex][index1])
                for tex in [R"X({s})", "m", R"{s}^2", R"\mu", R"{s}", "k"]
                for index0 in [3 if tex == R"{s}" else 0]
                for index1 in [2 if tex == R"{s}" else 0]
            ] + [
                Write(factored_ode_lt_lhs["+"][:2]),
                Write(factored_ode_lt_lhs[R"\big("]),
                Write(factored_ode_lt_lhs[R"\big)"]),
            ],
            lag_ratio=0.1,
            run_time=3
        ))
        self.wait()

        # Show initial conditions
        ic_parts = VGroup(
            ode_lt_lhs[R"- {s} x_0 - v_0"][0],
            ode_lt_lhs[R"- x_0"][0],
        )
        ic_part_consts = VGroup(
            ode_lt_lhs[R"m\Big("][0],
            ode_lt_lhs[R"\Big)"][0],
            ode_lt_lhs[R"\mu \Big("][0],
            ode_lt_lhs[R"\Big)"][1],
        ).copy().set_fill(opacity=1)
        ic_part_rects = VGroup(SurroundingRectangle(part, buff=SMALL_BUFF) for part in ic_parts)
        ic_part_rects.set_stroke(TEAL, 2)
        factored_ic_part = factored_ode_lt_lhs[R"- m v_0 - (m{s} + \mu)x_0"]

        self.play(
            FadeOut(Xs_part_rects),
            FadeIn(ic_part_rects),
            Xs_parts.animate.set_fill(opacity=0.25),
            ic_parts.animate.set_fill(opacity=1),
            FadeIn(ic_part_consts),
        )
        self.play(
            Write(factored_ic_part),
        )
        self.wait()

        # Comment on initial conditions
        ic_rect = SurroundingRectangle(factored_ic_part, buff=0.15)
        ic_rect.set_stroke(TEAL, 3)

        ic_words = Text("Initial conditions")
        ic_words.next_to(ic_rect, DOWN)
        zero_ic = Tex(R"\text{Let’s assume } x_0 = v_0 = 0", t2c=t2c)
        zero_ic.next_to(ic_words, DOWN, aligned_edge=LEFT)

        poly_part = Tex(R"X({s})\big(m{s}^2 + \mu{s} + k\big)", t2c=t2c)
        poly_part.move_to(factored_ode_lt_lhs[poly_part.get_tex()][0])

        lt_equals = Tex(R"=")
        lt_equals.match_y(ode_lt_lhs)
        lt_equals.match_x(ode["="])

        self.play(
            ShowCreation(ic_rect),
            Write(ic_words),
            run_time=1
        )
        self.wait()
        self.play(FadeIn(zero_ic, 0.5 * DOWN))
        self.wait()

        self.play(
            FadeOut(ode_lt_lhs, UP),
            FadeOut(ic_part_rects, UP),
            FadeOut(ic_part_consts, UP),
            poly_part.animate.next_to(lt_equals, LEFT),
            lhs_arrow.animate.scale(1 / 0.75, about_edge=UL),
        )
        self.play(
            LaggedStartMap(FadeOut, VGroup(factored_ode_lt_lhs, ic_rect, ic_words, zero_ic), lag_ratio=0.25),
            run_time=2,
        )
        self.wait()

        # Mirror image
        ode_rhs = ode[R"F_0 \cos(\omega t)"][0]

        part_pairs = [
            # CHANGE: poly_part_copy is defined much further down (UnboundLocalError); poly_part is used, the line the original left commented out.
            [ode[tex1][index].copy(), poly_part[tex2][index].copy()]
            for tex1, tex2, index in [
                ("m", "m", 0),
                ("x''(t)", R"{s}^2", 0),
                ("+", "+", 0),
                (R"\mu", R"\mu", 0),
                (R"x'(t)", R"{s}", -1),
                ("+", "+", 1),
                ("k", "k", 0),
            ]
        ]

        self.play(LaggedStart(
            ode_rhs.animate.set_fill(opacity=0.25),
            FadeOut(ode_lhs_rect.copy()),
            ShowCreation(ode_lhs_rect),
            lag_ratio=0.5
        ))
        self.wait()
        self.play(LaggedStart(
            *(TransformFromCopy(*pair) for pair in part_pairs),
            lag_ratio=0.025
        ))
        self.wait()
        self.play(LaggedStart(
            *(TransformFromCopy(*reversed(pair)) for pair in part_pairs),
            lag_ratio=0.025
        ))
        self.wait()

        for pair in part_pairs:
            self.remove(*pair)
        self.add(poly_part)

        # Transform cosine
        ode_lt_rhs = Tex(R"{F_0 {s} \over {s}^2 + \omega^2}", t2c=t2c)
        ode_lt_rhs.next_to(lt_equals, RIGHT)

        rhs_arrow = self.get_lt_arrow(ode_rhs, ode_lt_rhs)

        self.play(
            Write(lt_equals),
            TransformFromCopy(lhs_arrow, rhs_arrow),
            ode_rhs.animate.set_fill(opacity=1),
            ode_lhs_rect.animate.surround(ode_rhs),
        )
        self.wait()
        self.play(LaggedStart(
            *(
                TransformFromCopy(ode[tex][0], ode_lt_rhs[tex][0])
                for tex in ["F_0", R"\omega"]
            ),
            FadeIn(ode_lt_rhs[R"{s} \over {s}^2 +"][0]),
            FadeIn(ode_lt_rhs[R"^2"][1]),
        ))
        self.add(ode_lt_rhs)
        self.wait()

        # Walk through cosine transform
        cos_transform_parts = VGroup(
            Tex(R"\mathcal{L}\big\{\cos(\omega t)\big\}", t2c=t2c),
            Tex(R"= \mathcal{L}\left\{\frac{1}{2}e^{i \omega t} + \frac{1}{2} e^{\minus i \omega t} \right\}", t2c=t2c),
            Tex(R"= \frac{1}{2} \mathcal{L}\big\{e^{i \omega t}\big\} + \frac{1}{2} \mathcal{L}\big\{e^{\minus i \omega t}\big\}", t2c=t2c),
            Tex(R"= \frac{1}{2} {1 \over {s} - \omega i} + \frac{1}{2} {1 \over {s} + \omega i}", t2c=t2c),
            Tex(R"= {{s} \over {s}^2 + \omega^2}", t2c=t2c),
        )
        cos_transform_parts.arrange(RIGHT)
        cos_transform_parts.to_edge(DOWN, buff=1.5)
        cos_transform_parts.to_edge(LEFT, buff=0.5)
        for part in cos_transform_parts[1:]:
            part.next_to(cos_transform_parts[0], RIGHT)
        cos_transform_parts[-1].next_to(cos_transform_parts[-2], RIGHT, aligned_edge=DOWN)

        self.play(LaggedStart(
            TransformFromCopy(ode[R"\cos(\omega t)"], cos_transform_parts[0][R"\cos(\omega t)"]),
            FadeTransform(rhs_arrow[1].copy(), cos_transform_parts[0][R"\mathcal{L}"]),
            Write(cos_transform_parts[0][R"\big\{"]),
            Write(cos_transform_parts[0][R"\big\}"]),
        ))
        self.wait()
        self.play(
            TransformMatchingTex(
                cos_transform_parts[0].copy(),
                cos_transform_parts[1],
                matched_keys=[R"\omega"],
                run_time=1
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                cos_transform_parts[1],
                cos_transform_parts[2],
                matched_keys=[R"\mathcal{L}", R"e^{i \omega t}", R"e^{\minus i \omega t}"],
                key_map={R"\left\{": R"\big\{", R"\right\}": R"\big\}", },
                run_time=1
            )
        )
        self.wait()
        self.play(
            TransformMatchingTex(
                cos_transform_parts[2],
                cos_transform_parts[3],
                matched_keys=[R"\frac{1}{2}", "+"],
                key_map={
                    R"\mathcal{L}\big\{e^{i \omega t}\big\}": R"{1 \over {s} - \omega i}",
                    R"\mathcal{L}\big\{e^{\minus i \omega t}\big\}": R"{1 \over {s} + \omega i}",
                },
                run_time=1,
                path_arc=30 * DEG,
            )
        )
        self.wait()
        self.play(Write(cos_transform_parts[4], run_time=1))
        self.wait()
        self.play(
            *(FadeOut(cos_transform_parts[i]) for i in [0, 3, 4]),
            FadeOut(ode_lhs_rect)
        )
        self.wait()

        # Divide out
        poly_tex = R"\big(m{s}^2 + \mu{s} + k\big)"
        cos_lt_denom_tex = R"\left({s}^2 + \omega^2 \right)"
        true_poly_part = poly_part[poly_tex][0]
        final_answer = Tex(R"X({s}) = {F_0 {s} \over " + cos_lt_denom_tex + poly_tex + "}", t2c=t2c)
        final_answer.next_to(lt_equals, DOWN, buff=1.5)

        poly_rect = SurroundingRectangle(true_poly_part, buff=SMALL_BUFF)
        poly_rect.set_stroke(TEAL, 2)

        self.play(ShowCreation(poly_rect))
        self.play(LaggedStart(
            AnimationGroup(
                TransformFromCopy(true_poly_part, final_answer[poly_tex][0]),
                poly_rect.animate.surround(final_answer[poly_tex][0])
            ),
            TransformFromCopy(poly_part["X({s})"], final_answer["X({s})"]),
            AnimationGroup(
                TransformFromCopy(ode_lt_rhs[R"F_0 {s} \over"], final_answer[R"F_0 {s} \over"]),
                TransformFromCopy(ode_lt_rhs[R"{s}^2 + \omega^2"], final_answer[R"{s}^2 + \omega^2"]),
            ),
            Write(final_answer["="]),
            Write(final_answer[R"\left("]),
            Write(final_answer[R"\right)"]),
            lag_ratio=0.1,
            run_time=3
        ))
        self.play(FadeOut(poly_rect))
        self.wait()

        # Pull up final answer
        self.play(
            LaggedStartMap(FadeOut, VGroup(lhs_arrow, rhs_arrow, poly_part, lt_equals, ode_lt_rhs), shift=0.2 * UP, lag_ratio=0.2, run_time=1),
            LaggedStart(
                final_answer.animate.next_to(ode, DOWN, MED_LARGE_BUFF).shift(RIGHT),
                ode.animate.scale(0.75, about_edge=UP),
                run_time=2,
                lag_ratio=0.25,
            )
        )
        self.wait()

        # Write L{x(t)}
        final_lhs = Tex(R"\mathcal{L}\left\{x(t)\right\} = ", t2c=t2c)
        final_lhs.next_to(final_answer, LEFT)
        final_lhs.shift(SMALL_BUFF * UP)
        xt_copy = ode["x(t)"][0].copy()

        self.play(xt_copy.animate.replace(final_lhs["x(t)"]))
        self.play(Write(final_lhs))
        self.remove(xt_copy)
        self.wait()

        # Reference inversion
        rhs_tex = final_answer.get_tex().split( "= ")[1]
        inverse_equation = Tex(
            R"x(t) = \mathcal{L}^{-1}\left\{" + rhs_tex + R"\right\}",
            t2c=t2c
        )
        inverse_equation.next_to(final_answer, DOWN, LARGE_BUFF)
        inverse_equation.set_x(0)

        self.play(LaggedStart(
            *(
                TransformFromCopy(final_lhs[tex], inverse_equation[tex])
                for tex in ["x(t)", R"\mathcal{L}", R"\left\{", R"\right\}", "="]
            ),
            FadeInFromPoint(inverse_equation["-1"], final_lhs.get_center()),
            TransformFromCopy(final_answer[rhs_tex], inverse_equation[rhs_tex]),
            lag_ratio=0.025,
            run_time=1.5
        ))
        self.wait()
        self.play(FadeOut(inverse_equation, DOWN))

        # Ask about denominator
        denom_tex = cos_lt_denom_tex + poly_tex
        sub_texs = [rhs_tex, denom_tex, poly_tex, cos_lt_denom_tex]
        rhs, denom, poly_part, cos_lt_denom = answer_parts = VGroup(
            final_answer[tex][0]
            for tex in sub_texs
        )
        rect = SurroundingRectangle(rhs, buff=0.05)
        rect.set_stroke(YELLOW, 2)

        zero_question = Text("When is this 0?")
        zero_question.next_to(rect, DOWN)

        self.play(ShowCreation(rect))
        self.wait()
        self.play(
            final_lhs.animate.set_fill(opacity=0.5),
            final_answer[:final_answer.submobjects.index(cos_lt_denom[0])].animate.set_fill(opacity=0.5),
            rect.animate.surround(denom),
            FadeIn(zero_question, lag_ratio=0.1)
        )
        self.wait()

        # Show quadratic formula
        implies = Tex(R"\Longrightarrow", font_size=72)
        implies.rotate(-90 * DEG)
        implies.next_to(poly_part, DOWN)
        eq_0 = Tex(R"=0", font_size=36)
        eq_0.next_to(implies, RIGHT, buff=0)
        implies.add(eq_0)
        implies.add(eq_0.copy().fade(1).next_to(implies, LEFT, buff=0))

        quadratic_form = Tex(R"{s} = {-\mu \pm \sqrt{\mu^2 - 4mk} \over 2m}", t2c=t2c, font_size=36)
        quadratic_form.next_to(implies, DOWN)

        poly_part_copy = Tex(poly_tex, t2c=t2c)
        poly_part_copy.replace(poly_part)

        self.play(
            FadeTransformPieces(zero_question, eq_0),
            Write(implies),
            rect.animate.surround(poly_part),
            cos_lt_denom.animate.set_fill(opacity=0.5)
        )
        self.wait()
        self.play(
            TransformMatchingTex(poly_part_copy, quadratic_form, lag_ratio=0.01)
        )
        self.wait()

        # Show omega i and -omega i roots
        cos_poles = Tex(R"{s} = \pm \omega i", t2c=t2c)
        cos_poles.next_to(implies, DOWN)
        cos_poles.match_x(cos_lt_denom)

        self.play(
            cos_lt_denom.animate.set_fill(opacity=1),
            poly_part.animate.set_fill(opacity=0.5),
            rect.animate.surround(cos_lt_denom),
            implies.animate.match_x(cos_lt_denom),
            FadeTransformPieces(quadratic_form, cos_poles)
        )
        self.wait()

    def get_x_colors_and_t2c(self):
        x_colors = color_gradient([TEAL, RED], 3, interp_by_hsl=True)
        t2c = {
            "x(t)": x_colors[0],
            "x'(t)": x_colors[1],
            "x''(t)": x_colors[2],
            "x_0": x_colors[0],
            "v_0": x_colors[1],
            R"\omega": PINK,
            "{s}": YELLOW,
        }
        return x_colors, t2c
