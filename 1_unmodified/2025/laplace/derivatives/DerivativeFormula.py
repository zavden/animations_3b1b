# ==============================================================================
# Scene:      DerivativeFormula
# Source:     videos/_2025/laplace/derivatives.py (lines 216-719)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DerivativeFormula.py DerivativeFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

tex_to_color = {
    "{t}": BLUE,
    "{s}": YELLOW,
}


class DerivativeFormula(InteractiveScene):
    tex_config = dict(t2c=tex_to_color, font_size=72)

    def construct(self):
        # Set up commutative diagram
        kw = self.tex_config
        ft, Fs, dft, sFs = terms = VGroup(
            Tex(R"f({t})", **kw),
            Tex(R"F({s})", **kw),
            Tex(R"f'({t})", **kw),
            Tex(R"{s}F({s}) - f(0)", **kw),
        )
        terms.arrange_in_grid(
            h_buff=2.0,
            v_buff=3.0,
            aligned_edge=LEFT,
            fill_rows_first=False
        )
        terms.to_edge(UP, buff=LARGE_BUFF)
        terms.shift(RIGHT)

        dist = get_norm(ft.get_bottom() - Fs.get_top()) - MED_LARGE_BUFF
        down_arrow = Vector(dist * DOWN, thickness=6)
        arrow_kw = dict(thickness=6)
        lt_arrows = VGroup(
            down_arrow.copy().next_to(term, DOWN)
            for term in [ft, dft]
        )
        lt_arrows.set_fill(GREY_A)
        for arrow in lt_arrows:
            self.add_arrow_label(arrow, R"\mathcal{L}", RIGHT)

        deriv_arrow = Arrow(ft, dft, thickness=6)
        s_mult_arrow = Arrow(Fs, sFs, thickness=6)

        self.add_arrow_label(deriv_arrow, R"d / d{t}", UP)
        self.add_arrow_label(s_mult_arrow, R"\times {s}", UP)

        # Add terms
        L_df = Tex(R"\mathcal{L}\big\{f'({t})\big\}", **kw)
        L_df.move_to(sFs, LEFT)
        equals = Tex(R"=", font_size=72).rotate(90 * DEG)
        equals.next_to(sFs["{s}F({s})"], DOWN)

        self.play(Write(ft), run_time=1)
        self.wait()
        self.play(LaggedStart(
            self.grow_arrow(deriv_arrow),
            TransformMatchingTex(ft.copy(), dft, run_time=1, path_arc=45 * DEG),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(LaggedStart(
            self.grow_arrow(lt_arrows[1]),
            TransformMatchingTex(
                dft.copy(),
                L_df,
                run_time=1.5,
                path_arc=45 * DEG,
                matched_keys=[R"f'({t})"]
            ),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(LaggedStart(
            self.grow_arrow(lt_arrows[0]),
            TransformFromCopy(ft.copy(), Fs, run_time=1.5, path_arc=45 * DEG),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(LaggedStart(
            self.grow_arrow(s_mult_arrow),
            FadeTransform(Fs.copy(), sFs[1:5]),
            TransformFromCopy(Fs[2], sFs[0]),
            L_df.animate.scale(0.7).next_to(equals, DOWN),
            Write(equals),
            lag_ratio=0.1
        ))
        self.wait()

        # Correction
        almost = Text("Almost...")
        almost.set_color(RED)
        almost.next_to(equals, RIGHT, MED_SMALL_BUFF)

        self.play(FadeIn(almost, lag_ratio=0.1))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(ft, sFs["f(0)"][0], path_arc=-45 * DEG, run_time=2),
            Write(sFs["-"]),
        ))
        self.play(
            FadeOut(almost),
            VGroup(equals, L_df).animate.space_out_submobjects(1.2).next_to(sFs, DOWN)
        )
        self.wait()

        # Highlight parts
        rect = SurroundingRectangle(deriv_arrow.label)
        rect.set_stroke(TEAL, 4)
        mid_lt_arrow = lt_arrows[0].copy().match_x(deriv_arrow)
        self.add_arrow_label(mid_lt_arrow, R"\mathcal{L}", RIGHT)
        mid_arrow_group = VGroup(mid_lt_arrow, mid_lt_arrow.label)
        mid_arrow_group.shift(0.25 * UP)
        mid_arrow_group.set_fill(opacity=0.5)

        self.play(ShowCreation(rect))
        self.wait()
        self.play(
            rect.animate.surround(s_mult_arrow.label),
            self.grow_arrow(mid_lt_arrow),
        )
        self.play(
            FadeOut(mid_arrow_group),
            FadeOut(rect),
        )
        self.wait()

        # Comment on -f(0)
        frame = self.frame
        randy = Randolph().flip()
        randy.next_to(sFs, DR, LARGE_BUFF)
        randy.shift(0.5 * LEFT)
        morty = Mortimer().flip()
        morty.next_to(randy, LEFT, buff=2.0)
        morty.body.insert_n_curves(500)
        quirk = sFs["- f(0)"][0]
        quirk_rect = SurroundingRectangle(quirk)
        quirk_rect.set_stroke(RED, 5)
        ic_words = Text("Initial\nCondition", font_size=72)
        ic_words.next_to(quirk, UR, LARGE_BUFF)
        ic_arrow = Arrow(ic_words.get_bottom(), quirk.get_right(), path_arc=-90 * DEG, thickness=6)

        self.play(LaggedStart(
            frame.animate.reorient(0, 0, 0, (2.0, -0.79, 0.0), 9.49),
            FadeOut(equals),
            FadeOut(L_df),
            ShowCreation(quirk_rect),
            VFadeIn(randy),
            randy.change("angry", quirk),
            lag_ratio=0.1
        ))
        self.play(Blink(randy))
        self.wait()
        self.play(
            VFadeIn(morty),
            morty.change("tease", randy.eyes),
            randy.change('hesitant', morty.eyes),
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty.change("raise_right_hand", ic_words),
            randy.change("pondering", ic_words),
            FadeIn(ic_words, lag_ratio=0.1, run_time=1),
            Write(ic_arrow)
        )
        self.wait()

        # Ask why
        bubble = randy.get_bubble("Why?", SpeechBubble, direction=LEFT)
        bubble.shift(0.5 * LEFT)

        exp_propety_frame = Rectangle(16, 9).replace(terms, 1)
        exp_propety_frame.next_to(terms, RIGHT, buff=1.0)
        exp_propety_frame.set_stroke(BLUE, 0)

        self.play(LaggedStart(
            randy.change("maybe"),
            Write(bubble),
            morty.change("thinking", lt_arrows),
            FadeOut(ic_words),
            FadeOut(ic_arrow),
            FadeOut(quirk_rect),
            lag_ratio=0.1
        ))
        self.play(Blink(randy))
        self.play(
            Group(frame, randy, morty, bubble).animate.scale(1.25, about_edge=UL),
        )
        self.play(
            randy.change("raise_left_hand", exp_propety_frame),
            morty.change('pondering', exp_propety_frame),
            FadeIn(exp_propety_frame),
            FadeOut(bubble),
        )
        self.wait()
        self.play(
            ShowCreationThenFadeOut(quirk_rect),
            morty.animate.look_at(quirk),
            randy.change('sassy', quirk),
        )
        self.play(Blink(randy))
        self.play(Blink(morty))
        self.wait()

        # Reset
        self.play(FadeOut(exp_propety_frame))
        self.play(
            frame.animate.reorient(0, 0, 0, (-1.0, -0.61, 0.0), 9.39),
            LaggedStartMap(FadeOut, VGroup(morty, randy), shift=DOWN),
            run_time=2
        )

        # Substitute in e^(at)
        fade_group = VGroup(
            deriv_arrow, deriv_arrow.label,
            s_mult_arrow, s_mult_arrow.label,
            lt_arrows[1], lt_arrows[1].label,
            dft,
            sFs
        )

        eat_terms = VGroup(
            Tex(R"f({t}) = e^{a{t}}", **kw),
            Tex(R"F({s}) = {1 \over {s} - a}", **kw),
            Tex(R"f'({t}) = a \cdot e^{a{t}}", **kw),
            Tex(R"{a \over {s} - a}", **kw),
        )
        for term, eat_term, corner in zip(terms, eat_terms, [DR, UR, DL, UL]):
            eat_term.move_to(term, corner)
        eat_terms[3].align_to(eat_terms[1], DOWN)

        self.remove(ft)
        self.play(
            TransformFromCopy(ft, eat_terms[0][:len(ft)]),
            Write(eat_terms[0][len(ft):]),
            s_mult_arrow.animate.scale(0.8, about_edge=UP),
            fade_group.animate.set_fill(opacity=0.2),
        )
        self.wait()
        self.play(
            TransformMatchingShapes(
                eat_terms[0][len(ft):].copy(),
                eat_terms[1][len(Fs):],
                path_arc=-45 * DEG,
                run_time=1.5,
            ),
            FadeTransform(Fs, eat_terms[1][:len(Fs)]),
            VGroup(s_mult_arrow, s_mult_arrow.label).animate.shift(0.4 * DOWN)
        )
        self.add(eat_terms[1])
        self.wait()
        self.play(
            VGroup(deriv_arrow, deriv_arrow.label, dft).animate.set_fill(opacity=1)
        )
        self.wait()
        self.remove(dft)
        self.play(
            TransformFromCopy(eat_terms[0][-3:], eat_terms[2][-3:], path_arc=-45 * DEG, run_time=1.5),
            TransformFromCopy(eat_terms[0][-4], eat_terms[2][-6], path_arc=-45 * DEG, run_time=1.5),
            TransformFromCopy(dft, eat_terms[2][:len(dft)])
        )
        self.play(
            Write(eat_terms[2][-4]),
            TransformFromCopy(eat_terms[2][-2], eat_terms[2][-5], path_arc=45 * DEG),
        )
        self.wait()

        # Show transform of right hand side
        left_group_copy = VGroup(
            eat_terms[0]["e^{a{t}}"][0],
            lt_arrows[0],
            lt_arrows[0].label,
            eat_terms[1][R"{1 \over {s} - a}"][0]
        ).copy()
        a_dot_copy = eat_terms[2][R"a \cdot"][0].copy()
        a_dot_rect = SurroundingRectangle(a_dot_copy).set_stroke(TEAL, 2)

        shift_value = eat_terms[2]["e^{a{t}}"].get_center() - left_group_copy[0].get_center()
        self.play(
            left_group_copy.animate.shift(shift_value).set_anim_args(path_arc=30 * DEG),
            sFs.animate.shift(3.0 * DOWN),
            run_time=1.5
        )
        self.play(ShowCreation(a_dot_rect))
        self.play(
            a_dot_copy.animate.next_to(left_group_copy[-1][1], LEFT),
            MaintainPositionRelativeTo(a_dot_rect, a_dot_copy),
        )
        self.wait()
        self.play(
            FadeOut(left_group_copy[:3]),
            ReplacementTransform(left_group_copy[3][1:], eat_terms[3][1:]),
            ReplacementTransform(a_dot_copy, eat_terms[3][:1]),
            FadeOut(left_group_copy[3][0], LEFT),
            FadeOut(a_dot_rect, LEFT),
            VGroup(lt_arrows[1], lt_arrows[1].label).animate.set_fill(opacity=1),
        )
        self.wait()

        # Differentiation to multiplication
        randy = Randolph(height=3)
        randy.next_to(eat_terms[1], DOWN, buff=LARGE_BUFF)
        randy.shift(2 * LEFT)
        mult_a_arrow = Arrow(
            eat_terms[1][-5:].get_bottom(),
            eat_terms[3].get_bottom(),
            path_arc=120 * DEG,
            thickness=6
        )
        rect = SurroundingRectangle(deriv_arrow.label)
        rect.set_stroke(TEAL, 4)
        mult_word = Text("Multiplication")
        times_a = Tex(R"\times a", **kw)
        for mob in [mult_word, times_a]:
            mob.next_to(mult_a_arrow, DOWN)

        self.play(
            frame.animate.reorient(0, 0, 0, (-1.1, -1.43, 0.0), 11.38),
            VFadeIn(randy),
            randy.change("shruggie", eat_terms[3]),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(ShowCreation(rect))
        self.play(LaggedStart(
            randy.change("pondering", mult_word),
            rect.animate.surround(mult_word),
            Write(mult_word),
            Write(mult_a_arrow),
            lag_ratio=0.2
        ))
        self.play(FadeOut(rect))
        self.wait()
        self.play(randy.change("erm", mult_word))
        self.play(FadeTransformPieces(mult_word, times_a))
        self.play(Blink(randy))
        self.wait()

        # Contrast against multiplication by s
        equals.next_to(eat_terms[3], DOWN, MED_LARGE_BUFF)
        q_marks = Tex(R"???", font_size=60).replicate(2)
        q_marks.set_color(RED)
        q_marks[0].next_to(s_mult_arrow.label, UP)
        q_marks[1].next_to(equals, RIGHT)

        self.play(LaggedStart(
            randy.animate.change_mode("horrified").shift(0.25 * DL).set_opacity(0),
            # FadeOut(mult_a_arrow),
            ReplacementTransform(mult_a_arrow, s_mult_arrow),
            # FadeOut(times_a),
            ReplacementTransform(times_a, s_mult_arrow.label),
            Animation(Point()),
            VGroup(s_mult_arrow, s_mult_arrow.label).animate.set_fill(opacity=1),
            Write(equals),
            sFs.animate.set_fill(opacity=1).next_to(equals, DOWN, MED_LARGE_BUFF),
            Write(q_marks),
        ))
        self.remove(randy)
        self.wait()

        # Show algebra
        added_frac = Tex(R"+ {{s} - a \over {s} - a}", **kw)
        minus_one = Tex(R"-1", **kw)
        added_frac.next_to(eat_terms[3], RIGHT, SMALL_BUFF)
        minus_one.next_to(added_frac[R"\over"], RIGHT, MED_SMALL_BUFF)

        added_frac_rect = SurroundingRectangle(added_frac, SMALL_BUFF)
        added_frac_rect.set_stroke(BLUE, 1)

        plus_one = Tex(R"+ 1", font_size=60)
        plus_one.set_color(BLUE)
        plus_one.next_to(added_frac_rect, DOWN)

        cover_rect = BackgroundRectangle(VGroup(equals, sFs), buff=MED_SMALL_BUFF)
        cover_rect.set_fill(BLACK, 0.8)

        combined_fraction = Tex(R"{a + {s} - a \over {s} - a}", **kw)
        clean_combined_fraction = Tex(R"{{s} \over {s} - a}", **kw)
        for mob in [combined_fraction, clean_combined_fraction]:
            mob.move_to(eat_terms[3], LEFT)

        self.play(
            FadeIn(cover_rect),
            FadeIn(added_frac_rect),
            Write(added_frac["+"][0]),
            *(
                TransformFromCopy(eat_terms[3][tex], added_frac[tex])
                for tex in [R"{s} - a", R"\over"]
            ),
        )
        self.play(Write(plus_one))
        self.wait()
        self.play(Write(minus_one))
        self.wait()
        self.remove(eat_terms[3], added_frac)
        self.play(
            TransformFromCopy(eat_terms[3]["a"][0], combined_fraction["a"][0]),
            TransformFromCopy(added_frac["+"][0], combined_fraction["+"][0]),
            TransformFromCopy(added_frac["{s} - a"][0], combined_fraction["{s} - a"][0]),
            TransformFromCopy(eat_terms[3][R"\over"][0], combined_fraction[R"\over"][0]),
            TransformFromCopy(added_frac[R"\over"][0], combined_fraction[R"\over"][0]),
            TransformFromCopy(eat_terms[3][R"{s} - a"][0], combined_fraction[R"{s} - a"][1]),
            TransformFromCopy(added_frac[R"{s} - a"][1], combined_fraction[R"{s} - a"][1]),
            added_frac_rect.animate.surround(combined_fraction),
            minus_one.animate.next_to(combined_fraction, RIGHT),
            FadeOut(plus_one),
            run_time=1.5
        )
        self.wait()
        self.play(
            TransformMatchingTex(combined_fraction, clean_combined_fraction, run_time=1),
            added_frac_rect.animate.surround(clean_combined_fraction),
            minus_one.animate.next_to(clean_combined_fraction, RIGHT)
        )
        self.wait()

        # Emphasize how this matches the rule
        pole = eat_terms[1][-5:]
        pole_rect = SurroundingRectangle(pole)
        pole_rect.match_style(added_frac_rect)

        self.play(
            FadeOut(added_frac_rect),
            FadeOut(q_marks[0], shift=0.25 * RIGHT, lag_ratio=0.1),
            ShowCreation(pole_rect),
        )
        self.play(
            pole_rect.animate.surround(clean_combined_fraction, SMALL_BUFF),
            TransformFromCopy(pole[1:], clean_combined_fraction[1:], path_arc=10 * DEG),
            TransformFromCopy(s_mult_arrow.label[1], clean_combined_fraction[0], path_arc=-10 * DEG),
            run_time=2
        )
        self.play(FadeOut(pole_rect, run_time=0.5))
        self.wait(0.5)

        # Emphasize minus f(0)
        low_eq_group = VGroup(equals, sFs)

        self.add(low_eq_group, cover_rect)
        self.play(
            FadeOut(cover_rect),
            low_eq_group.animate.match_x(VGroup(clean_combined_fraction, minus_one)),
            FadeOut(q_marks[1]),
        )

        quirk_rects = VGroup(
            SurroundingRectangle(minus_one, buff=SMALL_BUFF),
            SurroundingRectangle(sFs["- f(0)"][0], buff=SMALL_BUFF),
        )
        quirk_rects.set_stroke(RED, 2)
        minus_e_zero = Tex(R" - e^{a0}", **kw)
        minus_e_zero["0"].set_color(BLUE)
        minus_e_zero.next_to(quirk_rects[1], DOWN)

        self.play(ShowCreation(quirk_rects, lag_ratio=0))
        self.wait()
        self.play(
            TransformFromCopy(eat_terms[0]["= e^{a{t}}"][0], minus_e_zero, run_time=2)
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, VGroup(*quirk_rects, minus_e_zero), lag_ratio=0.5, run_time=1))

        # Maybe show more generally.
        kw["t2c"].update({"c_n": TEAL})
        exp_sum_terms = VGroup(
            Tex(R"f({t}) = \sum_{n=1}^N c_n e^{a_n {t}}", **kw),
            Tex(R"F({s}) = \sum_{n=1}^N {c_n \over {s} - a_n}", **kw),
            Tex(R"f'({t}) = \sum_{n=1}^N c_n \cdot a_n e^{a_n {t}}", **kw),
            Tex(R"\sum_{n=1}^N \left( c_n {{s} \over {s} - a_n} - c_n \right)", **kw),
        )
        for exp_sum_term, eat_term, corner in zip(exp_sum_terms, eat_terms, [DR, UR, DL, UL]):
            exp_sum_term.move_to(eat_term, corner)
        eat_terms[3].align_to(eat_terms[1], DOWN)

        self.play(
            LaggedStart(
                (TransformMatchingTex(eat_term, exp_sum_term)
                for eat_term, exp_sum_term in zip(eat_terms[:3], exp_sum_terms)),
                lag_ratio=0.2,
            ),
            FadeTransform(VGroup(clean_combined_fraction, minus_one), exp_sum_terms[-1], time_span=(1, 2)),
            LaggedStart(
                *(
                    VGroup(arrow, arrow.label).animate.shift(vect)
                    for arrow, vect in [
                        (lt_arrows[0], LEFT),
                        (deriv_arrow, 0.5 * UP),
                        (lt_arrows[1], RIGHT),
                        (s_mult_arrow, 0.5 * DOWN),
                    ]
                ),
                lag_ratio=0.5,
            ),
            self.frame.animate.reorient(0, 0, 0, (-0.15, -0.39, 0.0), 13.58),
            low_eq_group.animate.shift(DR),
            run_time=3
        )
        self.wait()

    def add_arrow_label(self, arrow, label_tex, direction, buff=SMALL_BUFF):
        arrow.label = Tex(label_tex, **self.tex_config)
        arrow.label.next_to(arrow, direction, buff=buff)

    def grow_arrow(self, arrow, run_time=1):
        """
        Assumes the arrow has a .label attribute
        """
        return AnimationGroup(
            GrowArrow(arrow),
            FadeIn(arrow.label, shift=0.25 * arrow.get_vector()),
            run_time=run_time
        )
