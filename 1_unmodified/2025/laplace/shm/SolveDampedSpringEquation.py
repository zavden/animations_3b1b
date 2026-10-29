# ==============================================================================
# Scene:      SolveDampedSpringEquation
# Source:     videos/_2025/laplace/shm.py (lines 333-765)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolveDampedSpringEquation.py SolveDampedSpringEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_coef_colors(n_coefs=3):
    return [
        interpolate_color_by_hsl(TEAL, RED, a)
        for a in np.linspace(0, 1, n_coefs)
    ]


class SolveDampedSpringEquation(InteractiveScene):
    def construct(self):
        # Show x and its derivatives
        pos, vel, acc = funcs = VGroup(
            Tex(R"x(t)"),
            Tex(R"x'(t)"),
            Tex(R"x''(t)"),
        )
        funcs.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)

        labels = VGroup(
            Text("Position").set_color(BLUE),
            Text("Velocity").set_color(RED),
            Text("Acceleration").set_color(YELLOW),
        )
        colors = get_coef_colors()
        for line, label, color in zip(funcs, labels, colors):
            label.set_color(color)
            label.next_to(line, RIGHT, MED_LARGE_BUFF)
            label.align_to(labels[0], LEFT)

        VGroup(funcs, labels).to_corner(UR)

        arrows = VGroup()
        for l1, l2 in zip(funcs, funcs[1:]):
            arrow = Line(l1.get_left(), l2.get_left(), path_arc=150 * DEG, buff=0.2)
            arrow.add_tip(width=0.2, length=0.2)
            arrow.set_color(GREY_B)
            ddt = Tex(R"\frac{d}{dt}", font_size=30)
            ddt.set_color(GREY_B)
            ddt.next_to(arrow, LEFT, SMALL_BUFF)
            arrow.add(ddt)
            arrows.add(arrow)

        self.play(Write(funcs[0]), Write(labels[0]))
        self.wait()
        for func1, func2, label1, label2, arrow in zip(funcs, funcs[1:], labels, labels[1:], arrows):
            self.play(LaggedStart(
                GrowFromPoint(arrow, arrow.get_corner(UR), path_arc=30 * DEG),
                TransformFromCopy(func1, func2, path_arc=30 * DEG),
                FadeTransform(label1.copy(), label2),
                lag_ratio=0.1
            ))
            self.wait()

        deriv_group = VGroup(funcs, labels, arrows)

        # Show F=ma
        t2c = {
            "x(t)": colors[0],
            "x'(t)": colors[1],
            "x''(t)": colors[2],
        }
        equation1 = Tex(R"{m} x''(t) = -k x(t) - \mu x'(t)", t2c=t2c)
        equation1.to_corner(UL)

        ma = equation1["{m} x''(t)"][0]
        kx = equation1["-k x(t)"][0]
        mu_v = equation1[R"- \mu x'(t)"][0]
        rhs = VGroup(kx, mu_v)

        ma_brace, kx_brace, mu_v_brace = braces = VGroup(
            Brace(part, DOWN, buff=SMALL_BUFF)
            for part in [ma, kx, mu_v]
        )
        label_texs = [R"\textbf{F}", R"\text{Spring force}", R"\text{Damping}"]
        for brace, label_tex in zip(braces, label_texs):
            brace.add(brace.get_tex(label_tex))

        self.play(TransformFromCopy(acc, ma[1:], path_arc=-45 * DEG))
        self.play(LaggedStart(
            GrowFromCenter(ma_brace),
            Write(ma[0]),
            run_time=1,
            lag_ratio=0.1
        ))
        self.wait()
        self.play(LaggedStart(
            Write(equation1["= -k"][0]),
            FadeTransformPieces(ma_brace, kx_brace),
            TransformFromCopy(pos, equation1["x(t)"][0], path_arc=-45 * DEG),
        ))
        self.wait()
        self.play(LaggedStart(
            FadeTransformPieces(kx_brace, mu_v_brace),
            Write(equation1[R"- \mu"][0]),
            TransformFromCopy(vel, equation1["x'(t)"][0], path_arc=-45 * DEG),
        ))
        self.wait()
        self.play(FadeOut(mu_v_brace))

        # Rearrange
        equation2 = Tex(R"{m} x''(t) + \mu x'(t) + k x(t) = 0", t2c=t2c)
        equation2.move_to(equation1, UL)

        self.play(TransformMatchingTex(equation1, equation2, path_arc=45 * DEG))
        self.wait()

        # Hypothesis of e^st
        t2c = {"s": YELLOW, "x(t)": TEAL}
        hyp_word, hyp_tex = hypothesis = VGroup(
            Text("Hypothesis: "),
            Tex("x(t) = e^{st}", t2c=t2c),
        )
        hypothesis.arrange(RIGHT)
        hypothesis.to_corner(UR)
        sub_hyp_word = TexText(R"(For some $s$)", t2c={"$s$": YELLOW}, font_size=36, fill_color=GREY_B)
        sub_hyp_word.next_to(hyp_tex, DOWN)

        self.play(LaggedStart(
            FadeTransform(pos.copy(), hyp_tex[:4], path_arc=45 * DEG, remover=True),
            FadeOut(deriv_group),
            Write(hyp_word, run_time=1),
            Write(hyp_tex[4:], time_span=(0.5, 1.5)),
        ))
        self.add(hypothesis)
        self.wait()
        self.play(FadeIn(sub_hyp_word, 0.25 * DOWN))
        self.wait()

        # Plug it in
        t2c["s"] = YELLOW
        equation3 = Tex(R"{m} s^2 e^{st} + \mu s e^{st} + k e^{st} = 0", t2c=t2c)
        equation3.next_to(equation2, DOWN, LARGE_BUFF)
        pos_parts = VGroup(equation2["x(t)"][0], equation3["e^{st}"][-1])
        vel_parts = VGroup(equation2["x'(t)"][0], equation3["s e^{st}"][0])
        acc_parts = VGroup(equation2["x''(t)"][0], equation3["s^2 e^{st}"][0])
        matched_parts = VGroup(pos_parts, vel_parts, acc_parts)

        pos_rect, vel_rect, acc_rect = rects = VGroup(
            SurroundingRectangle(group[0], buff=0.05).set_stroke(group[0][0].get_color(), 1)
            for group in matched_parts
        )

        pos_arrow, vel_arrow, acc_arrow = arrows = VGroup(
            Arrow(*pair, buff=0.1)
            for pair in matched_parts
        )

        for rect, arrow, pair in zip(rects, arrows, matched_parts):
            self.play(ShowCreation(rect))
            self.play(
                GrowArrow(arrow),
                FadeTransform(pair[0].copy(), pair[1]),
                rect.animate.surround(pair[1]),
            )
            self.wait()
        self.play(
            LaggedStart(
                (TransformFromCopy(equation2[tex], equation3[tex])
                for tex in ["{m}", "+", "k", R"\mu", "=", "0"]),
                lag_ratio=0.05,
            ),
        )
        self.wait()
        self.play(FadeOut(arrows, lag_ratio=0.1), FadeOut(rects, lag_ratio=0.1))

        # Solve for s
        key_syms = ["s", "m", R"\mu", "k"]
        equation4, equation5, equation6 = new_equations = VGroup(
            Tex(R"e^{st} \left( ms^2 + \mu s + k \right) = 0", t2c=t2c),
            Tex(R"ms^2 + \mu s + k = 0", t2c=t2c),
            Tex(R"{s} = {{-\mu \pm \sqrt{\mu^2 - 4mk}} \over 2m}", isolate=key_syms)
        )
        rhs = equation6[2:]
        rhs.set_width(equation5.get_width() - equation6[:2].get_width(), about_edge=LEFT)
        equation6.refresh_bounding_box()
        equation6["{s}"].set_color(YELLOW)
        equation6.scale(1.25, about_edge=LEFT)

        new_equations.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)
        new_equations.move_to(equation3, UL)
        equation4 = new_equations[0]

        exp_rect = SurroundingRectangle(equation4[R"e^{st}"])
        exp_rect.set_stroke(YELLOW, 2)
        ne_0 = VGroup(Tex(R"\ne").rotate(90 * DEG), Integer(0))
        ne_0.arrange(DOWN).next_to(exp_rect, DOWN)

        self.play(
            TransformMatchingTex(
                equation3,
                equation4,
                matched_keys=[R"e^{st}"],
                run_time=1.5,
                path_arc=30 * DEG
            )
        )
        self.wait(0.5)
        self.play(ShowCreation(exp_rect))
        self.wait()
        self.play(Write(ne_0))
        self.wait()
        self.play(FadeOut(ne_0))
        self.play(
            *(
                TransformFromCopy(equation4[key], equation5[key])
                for key in [R"ms^2 + \mu s + k", "= 0"]
            ),
            FadeOut(exp_rect),
        )
        self.wait()

        # Show mirror image
        self.play(
            TransformMatchingTex(
                equation5.copy(), equation2.copy(),
                key_map={
                    "s^2": "x''(t)",
                    R"\mu s": R"\mu x(t)",
                    R"k": R"k x(t)",
                },
                # match_animation=FadeTransform,
                # mismatch_animation=FadeTransform,
                remover=True,
                rate_func=there_and_back_with_pause,
                run_time=6
            ),
            equation4.animate.set_fill(opacity=0.25),
        )
        self.play(equation4.animate.set_fill(opacity=1))
        self.wait()

        # Cover up mu terms
        boxes = VGroup(
            SurroundingRectangle(mob)
            for mob in [
                equation2[R"+ \mu x'(t)"],
                equation4[R"+ \mu s"],
                equation5[R"+ \mu s"],
            ]
        )
        boxes.set_fill(BLACK, 0)
        boxes.set_stroke(colors[1], 2)

        self.add(Point())
        self.play(FadeIn(boxes, lag_ratio=0.1))
        self.play(boxes.animate.set_fill(BLACK, 0.8).set_stroke(width=1, opacity=0.5))
        self.wait()

        # Add simple answer
        simple_answer = Tex(R"s = \pm i \sqrt{k / m}", t2c=t2c)
        simple_answer.next_to(equation5, DOWN, LARGE_BUFF, aligned_edge=RIGHT)

        omega_brace = Brace(simple_answer[R"\sqrt{k / m}"], DOWN, SMALL_BUFF)
        omega = omega_brace.get_tex(R"\omega")
        omega.set_color(PINK)

        self.play(FadeIn(simple_answer))
        self.wait()
        self.play(GrowFromCenter(omega_brace), Write(omega))
        self.wait()

        simple_answer.add(omega_brace, omega)

        # Reminder of what s represents
        s_copy = simple_answer[0].copy()
        s_rect = SurroundingRectangle(s_copy)

        self.play(ShowCreation(s_rect))
        self.wait()
        self.play(
            s_rect.animate.surround(hyp_tex["e^{st}"]).set_anim_args(path_arc=-60 * DEG),
            FadeTransform(s_copy, hyp_tex["s"], path_arc=-60 * DEG),
            run_time=2
        )
        self.wait()
        self.play(FadeOut(s_rect))

        # Move hypothesis
        frame = self.frame
        self.play(
            frame.animate.scale(1.5, about_edge=LEFT),
            hypothesis.animate.next_to(equation2, UP, LARGE_BUFF, aligned_edge=LEFT),
            FadeOut(sub_hyp_word),
            run_time=1.5
        )
        self.wait()

        # Show quadratic formula
        qf_arrow = Arrow(
            equation5.get_right(),
            equation6.get_corner(UR) + 0.5 * LEFT,
            path_arc=-150 * DEG
        )
        qf_words = Text("Quadratic\nFormula", font_size=30, fill_color=GREY_B)
        qf_words.next_to(qf_arrow.get_center(), UR)

        naked_equation = equation6.copy()
        for sym in key_syms:
            naked_equation[sym].scale(0).set_fill(opacity=0).move_to(10 * LEFT)

        qf_rect = SurroundingRectangle(equation6[2:])
        qf_rect.set_stroke(YELLOW, 1.5)

        self.play(
            FadeOut(simple_answer, DOWN),
            boxes.animate.set_fill(opacity=0).set_stroke(width=2, opacity=1)
        )
        self.play(FadeOut(boxes))
        self.wait()
        self.play(
            TransformFromCopy(equation5["s"], equation6["s"]),
            Write(equation6["="]),
            GrowFromPoint(qf_arrow, qf_arrow.get_corner(UL)),
            FadeIn(qf_words, shift=0.5 * DOWN),
        )
        self.play(
            LaggedStart(*(
                TransformFromCopy(equation5[sym], equation6[sym], time_span=(0.5, 1.5))
                for sym in key_syms[1:]
            ), lag_ratio=0.1),
            Write(naked_equation),
        )
        self.wait()
        self.remove(naked_equation)
        self.add(equation6)
        self.play(ShowCreation(qf_rect))
        self.wait()

    def old_material(self):
        # Show implied exponentials
        final_equation = new_equations[-1]
        consolidated_lines = VGroup(
            hypothesis,
            equation2,
            equation4,
            final_equation,
        )
        consolidated_lines.target = consolidated_lines.generate_target()
        consolidated_lines.target.scale(0.7)
        consolidated_lines.target.arrange(DOWN, buff=MED_LARGE_BUFF)
        consolidated_lines.target.to_corner(UL)

        implies = Tex(R"\Longrightarrow", font_size=60)
        implies.next_to(consolidated_lines.target[0], RIGHT, buff=0.75)

        t2c = {"x(t)": TEAL, R"\omega": PINK}
        imag_exps = VGroup(
            Tex(R"x(t) = e^{+i \omega t}", t2c=t2c),
            Tex(R"x(t) = e^{-i \omega t}", t2c=t2c),
        )
        imag_exps.arrange(RIGHT, buff=2.0)
        imag_exps.next_to(implies, RIGHT, buff=0.75)

        self.remove(final_equation)
        self.play(LaggedStart(
            FadeOut(arrows),
            FadeOut(equation3, 0.5 * UP),
            FadeOut(sub_hyp_word),
            MoveToTarget(consolidated_lines),
            Write(implies),
        ))
        for imag_exp, sgn in zip(imag_exps, "+-"):
            self.play(
                TransformFromCopy(hyp_tex["x(t) ="][0], imag_exp["x(t) ="][0]),
                TransformFromCopy(hyp_tex["e"][0], imag_exp["e"][0]),
                TransformFromCopy(hyp_tex["t"][-1], imag_exp["t"][-1]),
                FadeTransform(final_equation[R"\pm i"][0].copy(), imag_exp[Rf"{sgn}i"][0]),
                FadeTransform(final_equation[R"\sqrt{k/m}"][0].copy(), imag_exp[R"\omega"][0]),
            )

        omega_brace = Brace(final_equation[R"\sqrt{k/m}"], DOWN, SMALL_BUFF)
        omega_label = omega_brace.get_tex(R"\omega").set_color(PINK)
        self.play(GrowFromCenter(omega_brace), Write(omega_label))
        self.wait()

        # Combine two solutions
        cos_equation = Tex(R"e^{+i \omega t} + e^{-i \omega t} = 2\cos(\omega t)", t2c={R"\omega": PINK})
        cos_equation.move_to(imag_exps)
        omega_brace2 = omega_brace.copy()
        omega_brace2.stretch(0.5, 0).match_width(cos_equation[R"\omega"][-1])
        omega_brace2.next_to(cos_equation[R"\omega"][-1], DOWN, SMALL_BUFF)
        omega_brace2_tex = omega_brace2.get_tex(R"\sqrt{k / m}", buff=SMALL_BUFF, font_size=24)

        self.remove(imag_exps)
        self.play(
            TransformFromCopy(imag_exps[0][R"e^{+i \omega t}"], cos_equation[R"e^{+i \omega t}"]),
            TransformFromCopy(imag_exps[1][R"e^{-i \omega t}"], cos_equation[R"e^{-i \omega t}"]),
            FadeOut(imag_exps[0][R"x(t) ="]),
            FadeOut(imag_exps[1][R"x(t) ="]),
            Write(cos_equation["+"][1]),
        )
        self.wait()
        self.play(Write(cos_equation[R"= 2\cos(\omega t)"]))
        self.wait()
        self.play(GrowFromCenter(omega_brace2), Write(omega_brace2_tex))

        # Clear the board
        self.play(LaggedStart(
            FadeOut(implies),
            FadeOut(cos_equation),
            FadeOut(omega_brace2),
            FadeOut(omega_brace2_tex),
            FadeOut(consolidated_lines[2:]),
            FadeOut(omega_brace),
            FadeOut(omega_label),
            lag_ratio=0.1
        ))

        # Add damping term
        t2c = {"x''(t)": colors[2], "x'(t)": colors[1], "x(t)": colors[0], "{s}": YELLOW}
        new_lines = VGroup(
            Tex(R"m x''(t) + \mu x'(t) + k x(t) = 0", t2c=t2c),
            Tex(R"m ({s}^2 e^{{s}t}) + \mu ({s} e^{{s}t}) + k (e^{{s}t}) = 0", t2c=t2c),
            Tex(R"e^{{s}t}\left(m {s}^2 + \mu {s} + k \right) = 0", t2c=t2c),
            Tex(R"m {s}^2 + \mu {s} + k = 0", t2c=t2c),
            Tex(R"{s} = {{-\mu \pm \sqrt{\mu^2 - 4mk}} \over 2m}", t2c=t2c),
        )
        new_lines.scale(0.7)
        new_lines.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        new_lines.move_to(equation2, UL)

        self.play(
            TransformMatchingTex(
                equation2,
                new_lines[0],
                matched_keys=t2c.keys(),
                run_time=1
            )
        )
        self.wait()
        for line1, line2 in zip(new_lines, new_lines[1:]):
            if line1 is new_lines[0]:
                key_map = {
                    "x''(t)": R"({s}^2 e^{{s}t})",
                    "x'(t)": R"({s} e^{{s}t})",
                    "x(t)": R"(e^{{s}t})",
                }
            else:
                key_map = dict()
            self.play(TransformMatchingTex(line1.copy(), line2, key_map=key_map, run_time=1, lag_ratio=0.01))
            self.wait()
