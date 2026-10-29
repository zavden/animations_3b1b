# ==============================================================================
# Scene:      CumulantsOfScaledSum
# Source:     videos/_2023/clt_proof/main.py (lines 1260-1545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CumulantsOfScaledSum.py CumulantsOfScaledSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CumulantsOfScaledSum(InteractiveScene):
    def construct(self):
        # Setup
        kw = dict(
            t2c={
                "{t}": MAROON_B,
                R"\frac{t^2}{2}": MAROON_B,
                R"\frac{t^3}{6}": MAROON_B,
                R"\frac{t^m}{m!}": MAROON_B,
            }
        )
        clt_var_tex = R"{X_1 + \cdots + X_n \over \sigma \sqrt{n}}"
        clt_var_flat = R"(X_1 + \cdots + X_n) / \sigma \sqrt{n}"
        cgf_def = Tex(R"""
            K_X({t})
            = \log\left(\mathds{E}\left[e^{{t}X}\right]\right)
            = \sum_{m=1}^\infty K_m[X] \frac{t^m}{m!}
        """, **kw)
        cgf_of_clt_var = Tex(
            Rf"""
                \mathds{{E}}\left[{clt_var_tex}\right] {{t}} 
                + \text{{Var}}\left({clt_var_tex}\right) \frac{{t^2}}{{2}}
                + K_3\left[{clt_var_tex}\right] \frac{{t^3}}{{6}}
                + \cdots 
            """,
        )
        cgf_of_clt_var.set_max_width(FRAME_WIDTH - 1)
        cgf_of_clt_var.to_edge(UP)

        clt_var = Tex(clt_var_tex, **kw)

        # Highlight scaled sum
        clt_var.set_height(1.5)
        clt_var.move_to(ORIGIN, DOWN)
        rect = SurroundingRectangle(clt_var)
        rect.set_stroke(YELLOW, 2)
        limit_words = TexText(R"What happens to \\ this as $n \to \infty$?")
        limit_words.next_to(rect, DOWN)
        limit_words.next_to(rect, DOWN)

        self.add(clt_var)
        self.play(
            FlashAround(clt_var, run_time=1.5),
            ShowCreation(rect),
            FadeIn(limit_words, lag_ratio=0.1),
        )
        self.wait()

        # Bring in CGF
        cgf_def.to_edge(UP)
        cgf_of_clt_sum = Tex(Rf"""
            K_{{{clt_var_flat}}}({{t}})
            = \sum_{{m=1}}^\infty
            K_m\left[{clt_var_tex}\right]
            \frac{{t^m}}{{m!}}
        """, **kw)
        cumulant_of_clt_var = cgf_of_clt_sum[Rf"K_m\left[{clt_var_tex}\right]"][0]
        cgf_of_clt_sum.save_state()
        cgf_of_clt_sum.set_opacity(0)
        cumulant_of_clt_var.set_opacity(1)
        cumulant_of_clt_var.center()
        cumulant_of_clt_var.set_height(1.5)

        self.play(
            clt_var.animate.center(),
            FadeIn(cgf_def, lag_ratio=0.1),
            FadeOut(limit_words),
            FadeOut(rect),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                clt_var,
                cgf_of_clt_sum[clt_var_tex][0],
                path_arc=45 * DEGREES,
            ),
            Write(cumulant_of_clt_var[:3]),
            Write(cumulant_of_clt_var[-1:]),
        )
        self.wait()
        self.play(Restore(cgf_of_clt_sum))
        self.wait()

        # Discuss scaling
        sigma_sqrt_n = cgf_of_clt_sum[R"\sigma \sqrt{n}"][0]
        sigma_sqrt_n_rect = SurroundingRectangle(sigma_sqrt_n, buff=0.05)
        sigma_sqrt_n_rect.set_stroke(YELLOW, 2)

        scaling_equation = Tex(
            R"""
                K_{cX}(t)
                = \log\left(\mathds{E}\left[e^{tcX} \right]\right)
                = \sum_{m=1}^\infty K_m[X] c^m \frac{t^m}{m!}
            """,
            t2c={
                "t": MAROON_B,
                R"\frac{t^m}{m!}": MAROON_B,
                "c": YELLOW,
            }
        )
        part1 = scaling_equation["K_{cX}(t)"][0]
        part2 = scaling_equation[re.compile(r"=.*\\right\)")][0]
        part3 = scaling_equation[re.compile(r"= \\sum.*m\!\}")][0]
        arrow = Vector(LEFT).next_to(part1, RIGHT)
        question = Text("How does this expand?")
        question.next_to(arrow)

        cX_rect = SurroundingRectangle(scaling_equation["cX"][1], buff=0.05)
        tc_rect = SurroundingRectangle(scaling_equation["tc"][0], buff=0.05)
        new_K_rect = SurroundingRectangle(scaling_equation["K_m[X] c^m"], buff=0.1)
        VGroup(cX_rect, tc_rect).set_stroke(BLUE, 2)
        new_K_rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(sigma_sqrt_n_rect))
        self.wait()
        self.play(
            TransformFromCopy(
                cgf_of_clt_sum[f"K_{{{clt_var_flat}}}({{t}})"][0],
                part1,
            ),
            Write(question),
            GrowArrow(arrow),
            cgf_of_clt_sum.animate.scale(0.75).to_edge(DOWN, buff=LARGE_BUFF),
            FadeOut(sigma_sqrt_n_rect, 2 * DOWN + 0.2 * RIGHT),
        )
        self.wait()
        self.play(
            FadeOut(question, lag_ratio=0.1),
            arrow.animate.next_to(part2, RIGHT),
            FadeIn(part2, lag_ratio=0.1)
        )
        self.wait()
        self.play(ShowCreation(cX_rect))
        self.wait()
        self.play(ReplacementTransform(cX_rect, tc_rect))
        self.wait()
        self.play(
            FadeOut(tc_rect),
            arrow.animate.next_to(part3, RIGHT),
            FadeIn(part3, lag_ratio=0.1)
        )
        self.wait()
        self.play(ShowCreation(new_K_rect))
        self.wait()
        self.play(
            FadeOut(cgf_def, UP),
            FadeOut(arrow, UP),
            scaling_equation.animate.to_edge(UP),
            MaintainPositionRelativeTo(new_K_rect, scaling_equation),
        )

        # Scaling rule for cumulant
        scaling_rule = Tex(R"K_m[cX] = c^m K_m[X]", t2c={"c": YELLOW})
        var_example = TexText(R"""
            For example, $\text{Var}(cX) = c^2 \text{Var}(X)$
        """, t2c={"c": YELLOW})
        var_example.move_to(scaling_rule.get_bottom())

        self.play(Write(scaling_rule["K_m[cX] = "][0]))
        self.wait()
        self.play(
            new_K_rect.animate.move_to(scaling_rule["c^m K_m[X]"]),
            LaggedStart(*(
                TransformFromCopy(
                    scaling_equation[tex][0],
                    scaling_rule[tex][0],
                    path_arc=45 * DEGREES,
                )
                for tex in ["K_m[X]", "c^m"]
            ))
        )
        self.play(FadeOut(new_K_rect))
        self.wait()
        self.play(
            scaling_rule.animate.next_to(var_example, UP, buff=0.5),
            FadeIn(var_example, 0.5 * DOWN)
        )
        self.wait()

        # Apply to the cummulant of the clt variable
        lhs = cumulant_of_clt_var.copy()
        scaling_rule.generate_target()
        scaling_rule.target.center().to_edge(UP)
        implies = Tex(R"\Downarrow", font_size=72)
        implies.next_to(scaling_rule.target, DOWN, buff=0.5)
        rhs = Tex(R"""
            = \left({1 \over \sigma \sqrt{n}} \right)^m
            K_m[X_1 + \cdots + X_n]
        """, font_size=42)
        rhs[R"\left({1 \over \sigma \sqrt{n}} \right)"].set_color(YELLOW)
        lhs.next_to(implies, DOWN, buff=0.5)

        self.play(
            FadeOut(var_example, UP),
            FadeOut(scaling_equation, UP),
            MoveToTarget(scaling_rule),
        )
        self.play(
            Write(implies),
            TransformFromCopy(cumulant_of_clt_var, lhs),
        )
        denom = lhs[-5:-1]
        self.play(
            FlashAround(denom),
            denom.animate.set_color(YELLOW)
        )
        self.wait()

        center_point = lhs.get_center() + LEFT
        rhs.next_to(center_point, RIGHT, buff=0.1)
        self.play(
            lhs.animate.next_to(center_point, LEFT, 0.1),
            TransformMatchingShapes(lhs.copy(), rhs),
        )
        self.wait()

        # Expand sum
        K_of_sum = rhs[R"K_m[X_1 + \cdots + X_n]"]
        K_of_sum_rect = SurroundingRectangle(K_of_sum, buff=0.1)
        K_of_sum_rect.set_stroke(BLUE, 2)

        sum_of_K = Tex(R"K_m[X_1] + \cdots + K_m[X_n]", font_size=42)
        nK = Tex(R"n \cdot K_m[X]", font_size=42)
        equals = Tex("=").rotate(90 * DEGREES).replicate(2)
        stack = VGroup(equals[0], sum_of_K, equals[1], nK)
        stack.arrange(DOWN)
        stack.next_to(K_of_sum_rect, DOWN)

        self.play(ShowCreation(K_of_sum_rect))
        self.wait()
        self.play(
            Write(equals[0]),
            TransformMatchingShapes(K_of_sum.copy(), sum_of_K, run_time=1.5)
        )
        self.wait()
        self.play(
            Write(equals[1]),
            TransformMatchingTex(sum_of_K.copy(), nK, run_time=1.5),
            cgf_of_clt_sum.animate.set_height(0.75).shift(3 * LEFT)
        )
        self.wait()
        nK.target = nK.generate_target()
        nK.target.move_to(K_of_sum, LEFT)
        self.play(
            MoveToTarget(nK),
            FadeOut(equals, UP),
            FadeOut(sum_of_K, UP),
            FadeOut(K_of_sum, UP),
            K_of_sum_rect.animate.match_points(SurroundingRectangle(nK.target))
        )
        self.play(
            FadeOut(K_of_sum_rect),
        )
        self.wait()

        # Emphasize expression
        cumulant_of_clt_var_equation = VGroup(
            lhs, rhs[re.compile(r"=.*\^m")], nK
        )
        full_rect = SurroundingRectangle(cumulant_of_clt_var_equation, buff=0.5)
        full_rect.set_stroke(TEAL, 3)
        words = TexText(f"Excellent! This is a complete(?) description of ${clt_var_tex}$")
        words.next_to(full_rect, UP, buff=MED_LARGE_BUFF)

        self.play(
            ShowCreation(full_rect),
            FadeOut(scaling_rule, UP),
            FadeOut(implies, 2 * UP),
        )
        self.play(Write(words))
        self.wait()

        # Clean up
        clean_rhs = Tex(R"""
            \frac{1}{\sigma^m}
            \frac{n}{n^{m / 2}}
            K_m[X]
        """)

        self.play(
            FadeOut(words, UP),
            FadeOut(full_rect, 2 * UP),
            FadeOut(cgf_of_clt_sum),
            cumulant_of_clt_var_equation.animate.to_edge(UP),
        )
        self.wait()
