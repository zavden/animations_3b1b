# ==============================================================================
# Scene:      TotalPopulationVsSymptomatic
# Source:     videos/_2020/med_test.py (lines 6481-7011)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TotalPopulationVsSymptomatic.py TotalPopulationVsSymptomatic -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TotalPopulationVsSymptomatic(Scene):
    def construct(self):
        # Titles
        v_line = Line(UP, DOWN).set_height(2 * FRAME_HEIGHT)
        v_line.to_edge(UP)
        self.add(v_line)

        titles = VGroup(
            OldTexText("Population"),
            OldTexText("Population", " \\emph{with symptoms}"),
        )
        titles[1][1].set_color(BLUE)
        for title, u in zip(titles, [-1, 1]):
            title.move_to(u * RIGHT * FRAME_WIDTH / 4)
        titles.to_edge(UP)

        self.add(titles[0])

        # Actual populations
        full_pop = VGroup(*(Dot() for x in range(10000)))
        full_pop.arrange_in_grid(
            buff=full_pop[0].get_width()
        )
        full_pop.set_width(FRAME_WIDTH / 2 - 1)
        full_pop.next_to(titles[0], DOWN)
        full_pop.to_edge(DOWN, buff=SMALL_BUFF)
        covid_pop = full_pop[:10]
        covid_pop.set_fill(YELLOW)
        covid_pop.save_state()
        covid_pop.scale(8, about_edge=UL)
        covid_pop.shift(DOWN)

        full_pop_words = VGroup(
            OldTexText("10 ", "with COVID", color=YELLOW),
            OldTexText("9990 ", "without COVID", color=GREY_B),
        )
        full_pop_words.arrange(RIGHT, buff=LARGE_BUFF)
        full_pop_words.scale(0.7)
        full_pop_words.next_to(full_pop, UP, SMALL_BUFF, LEFT)

        self.play(
            FadeIn(full_pop_words[0]),
            Write(covid_pop),
            run_time=1
        )
        self.play(
            FadeIn(full_pop_words[1]),
            ShowIncreasingSubsets(full_pop[10:]),
            Restore(covid_pop),
        )
        self.wait()

        # Mention symptoms
        self.play(
            TransformFromCopy(titles[0][0], titles[1][0]),
            FadeInFromPoint(titles[1][1], titles[0].get_center()),
        )
        self.wait()

        arrow = Vector(DOWN).next_to(titles[1][1], DOWN)
        arrow.set_color(BLUE)
        prop_ex = OldTex("\\sim \\frac{1}{50}", "\\text{, say}")
        prop_ex[0].set_color(BLUE)
        prop_ex.next_to(arrow, DOWN)

        self.play(
            GrowArrow(arrow),
            FadeIn(prop_ex, DOWN)
        )
        self.wait()

        # Symptomatic population
        left_sym_pop = VGroup(*random.sample(list(full_pop[10:]), 200))
        sym_pop = left_sym_pop.copy()
        sym_pop.generate_target()
        buff = get_norm(full_pop[1].get_left() - full_pop[0].get_right())
        sym_pop.target.arrange_in_grid(buff=buff)
        sym_pop.target.set_width(3.5)
        sym_pop.target.match_x(titles[1])
        sym_pop.target.align_to(full_pop, UP)
        sym_pop.target.shift(DOWN)
        sym_pop.target.set_color(BLUE)

        sym_pop_label = OldTexText("$\\sim 200$", " without COVID")
        sym_pop_label.set_color(GREY_B)
        sym_pop_label.scale(0.7)
        sym_pop_label.next_to(sym_pop.target, UP, buff=0.2)

        self.play(
            sym_pop.set_color, BLUE,
            MoveToTarget(sym_pop, lag_ratio=0.01, run_time=2),
            prop_ex.to_edge, DOWN,
            FadeOut(arrow),
            Write(sym_pop_label),
        )
        self.wait()

        sym_covid_pop = covid_pop[:5].copy()
        sym_covid_pop.generate_target()
        sym_covid_pop.target.arrange(DOWN, buff=buff)
        sym_covid_pop.target.scale(
            sym_pop[0].get_height() / sym_covid_pop[0].get_height()
        )
        sym_covid_pop.target.next_to(sym_pop, LEFT, aligned_edge=UP)

        sym_covid_pop_label = OldTexText("5", " with COVID")
        sym_covid_pop_label.scale(0.7)
        sym_covid_pop_label.next_to(sym_covid_pop.target, UP, buff=0.2)
        sym_covid_pop_label.set_color(YELLOW)

        self.play(ShowCreationThenFadeAround(sym_pop_label))
        self.play(
            VGroup(sym_pop, sym_pop_label).to_edge, RIGHT,
            MoveToTarget(sym_covid_pop),
            FadeIn(sym_covid_pop_label),
        )
        self.wait()

        # Apply test
        left_movers = VGroup(
            full_pop, full_pop_words,
            titles[0], v_line,
        )
        right_movers = VGroup(
            titles[1],
            sym_covid_pop, sym_covid_pop_label,
            sym_pop, sym_pop_label,
        )
        v_line_copy = v_line.copy()

        left_vect = (FRAME_WIDTH + SMALL_BUFF) * LEFT / 2
        self.play(
            LaggedStartMap(
                ApplyMethod, left_movers,
                lambda m: (m.shift, left_vect),
                lag_ratio=0.05,
            ),
            ApplyMethod(
                right_movers.shift, left_vect,
                rate_func=squish_rate_func(smooth, 0.3, 1),
            ),
            FadeOut(prop_ex),
            run_time=2,
        )
        self.wait()

        # With test result
        right_title = OldTexText(
            "Population ", "\\emph{with symptoms}\\\\",
            "and a positive test result"
        )
        right_title.set_color_by_tex("symptoms", BLUE)
        right_title.set_color_by_tex("positive", GREEN)
        right_title.set_x(FRAME_WIDTH / 4)
        right_title.to_edge(UP)
        titles.add(right_title)

        self.play(
            ShowCreation(v_line_copy),
            FadeIn(right_title),
        )
        self.wait()

        right_vect = FRAME_WIDTH * RIGHT / 2

        pc_pop = sym_covid_pop.copy()
        pn_pop = VGroup(*random.sample(list(sym_pop), 2)).copy()

        pn_pop.generate_target()
        buff = get_norm(sym_pop[1].get_left() - sym_pop[0].get_right())
        pn_pop.target.arrange(DOWN, buff=buff)
        pn_pop.target.next_to(sym_pop_label, DOWN)
        pn_pop.target.shift(right_vect)
        pn_pop.target.scale(1.5, about_edge=UP)

        black_rect = BackgroundRectangle(pc_pop[-1], fill_opacity=1)
        black_rect.stretch(0.5, 1, about_edge=DOWN)
        pc_pop.add(black_rect)
        pc_pop.set_opacity(0)

        pc_pop_label = OldTexText("4.5 with COVID", color=YELLOW)
        pn_pop_label = OldTexText("~2 without COVID", color=GREY_B)
        labels = VGroup(pc_pop_label, pn_pop_label)
        labels.scale(0.7)
        labels.set_opacity(0)

        pc_pop_label.move_to(sym_covid_pop_label)
        pn_pop_label.move_to(sym_pop_label)

        def get_test_rects(mob):
            return VGroup(*(
                SurroundingRectangle(
                    part,
                    color=GREEN,
                    buff=buff / 2,
                    stroke_width=2,
                )
                for part in mob
            ))

        self.play(
            pc_pop_label.shift, right_vect,
            pc_pop_label.set_opacity, 1,
            pc_pop.shift, right_vect,
            pc_pop.set_opacity, 1,
            pc_pop.scale, 1.5, {"about_edge": UP}
        )
        pc_pop_rects = get_test_rects(pc_pop[:5])
        self.play(FadeIn(pc_pop_rects, lag_ratio=0.3))
        self.wait()
        self.play(
            pn_pop_label.shift, right_vect,
            pn_pop_label.set_opacity, 1,
            MoveToTarget(pn_pop),
        )
        pn_pop_rects = get_test_rects(pn_pop)
        self.play(FadeIn(pn_pop_rects, lag_ratio=0.3))
        self.wait()

        # Final fraction
        equation = OldTex(
            "{4.5 \\over 4.5 + {2}} \\approx 69.2\\%",
            tex_to_color_map={
                "4.5": YELLOW,
                "{2}": GREY_B,
            }
        )
        equation.move_to(FRAME_WIDTH * RIGHT / 4)
        equation.to_edge(DOWN, buff=LARGE_BUFF)

        self.play(FadeIn(equation, lag_ratio=0.1))
        self.wait()

        # Zoom out
        frame = self.camera.frame

        self.play(
            frame.scale, 1.5, {"about_edge": UR},
            run_time=3,
        )
        self.wait()

        # Prepare population groups to move
        pop_groups = VGroup(
            VGroup(
                full_pop, full_pop_words,
            ),
            VGroup(
                sym_covid_pop, sym_covid_pop_label,
                sym_pop, sym_pop_label,
            ),
            VGroup(
                pc_pop, pc_pop_label, pc_pop_rects,
                pn_pop, pn_pop_label, pn_pop_rects,
                equation
            ),
        )
        pop_groups.generate_target()
        for group in pop_groups.target:
            group.scale(0.5, about_edge=DOWN)
            group.shift(4.5 * DOWN)

        pop_groups.target[0][0].set_opacity(0.5)

        h_line = Line(pop_groups.get_left(), pop_groups.get_right())
        h_line.next_to(pop_groups.target, UP)
        h_line.set_stroke(WHITE, 1)

        # Relevant odds labels
        def get_odds_label(n, k, n_color=YELLOW, k_color=GREY_B):
            result = VGroup(
                OldTexText("Odds = "),
                Integer(n, color=n_color, edge_to_fix=UR),
                OldTexText(":"),
                Integer(k, color=k_color, edge_to_fix=UL),
            )
            result.scale(1.5)
            result.arrange(RIGHT, buff=0.25)
            result[3].align_to(result[1], UP)
            return result

        odds_labels = VGroup(
            get_odds_label(1, 999),
            get_odds_label(25, 1000),
            get_odds_label(40, 90),
        )
        for label, title in zip(odds_labels, titles):
            label.move_to(title, UP)
            label.shift(2 * DOWN)

        odds_underlines = VGroup(*(
            Underline(label[1:])
            for label in odds_labels
        ))
        odds_arrows = VGroup(*(
            Arrow(o1.get_right(), o2.get_left())
            for o1, o2 in zip(odds_labels, odds_labels[1:])
        ))
        odds_arrows.set_fill(GREY_B)
        for arrow in odds_arrows:
            arrow.set_angle(0)

        self.play(
            MoveToTarget(pop_groups),
            FadeIn(odds_labels[0]),
            ShowCreation(h_line),
        )
        for i in (1, 2):
            self.play(
                FadeIn(odds_labels[i][0], RIGHT),
                FadeIn(odds_underlines[i], RIGHT),
                GrowArrow(odds_arrows[i - 1]),
            )
        self.wait()

        # Bayes factors
        bf_labels = VGroup(
            OldTexText(
                "Bayes factor for symptoms",
                tex_to_color_map={"for symptoms": BLUE}
            ),
            OldTexText(
                "Bayes factor positive test",
                tex_to_color_map={"positive test": GREEN}
            ),
        )
        for label, title in zip(bf_labels, titles[1:]):
            label.move_to(title, UP)
            label.shift(4.5 * DOWN)

        t2c = {
            "\\text{COVID}": YELLOW,
            "\\text{No COVID}": GREY_B,
            "\\text{Symp}": BLUE,
            "+": GREEN,
            "=": WHITE,
        }
        bf_equations = VGroup(
            OldTex(
                """
                {P(\\text{Symp} \\,|\\, \\text{COVID})
                \\over
                P(\\text{Symp} \\,|\\, \\text{No COVID})}
                = {50\\% \\over 2\\%} = 25
                """,
                tex_to_color_map=t2c,
            ),
            OldTex(
                """
                {P(+ \\,|\\, \\text{COVID}) \\over P(+ \\,|\\, \\text{No COVID})}
                = {90\\% \\over 1\\%} = 90
                """,
                tex_to_color_map=t2c,
            ),
        )
        for label, eq in zip(bf_labels, bf_equations):
            eq.scale(0.75)
            eq[-1].scale(2, about_edge=LEFT)
            eq.next_to(label, DOWN, buff=0.75)

        assumption_brace = Brace(bf_equations[0][-3:], DOWN)
        assumption_word = OldTexText("Assumption")
        assumption_word.next_to(assumption_brace, DOWN)

        self.play(
            Write(bf_labels[0]),
            FadeIn(bf_equations[0][:-3]),
        )
        self.wait()
        self.play(
            GrowFromCenter(assumption_brace),
            FadeIn(assumption_word, shift=0.2 * DOWN),
            FadeIn(bf_equations[0][-3:]),
        )
        self.wait()

        self.play(ShowCreationThenFadeOut(odds_underlines[0]))
        new_left_odds = get_odds_label(1, 1000)[1:]
        new_left_odds.move_to(odds_labels[0][1:], UL)
        approx = OldTex("\\approx", font_size=72)
        approx.rotate(90 * DEGREES)
        approx.next_to(odds_labels[0][1:], DOWN, buff=0.5)
        self.play(
            FadeIn(approx, 0.25 * DOWN),
            odds_labels[0][1:].next_to, approx, DOWN, {"buff": 0.5},
            FadeIn(new_left_odds, 0.5 * DOWN),
            odds_arrows[0].scale, 0.7, {"about_edge": RIGHT},
        )
        self.wait()

        curr_odds = new_left_odds.copy()
        self.play(
            curr_odds.move_to, odds_labels[1][1:], UR,
            path_arc=-30 * DEGREES
        )
        self.play(ChangeDecimalToValue(curr_odds[0], 25))
        self.wait()

        new_odds = curr_odds.copy()
        new_odds[0].set_value(1)
        new_odds[2].set_value(40)
        self.play(
            FadeOut(curr_odds, 0.5 * UP),
            FadeIn(new_odds, 0.5 * UP),
        )
        curr_odds = new_odds
        self.wait()

        self.play(
            Write(bf_labels[1]),
            FadeIn(bf_equations[1]),
        )
        self.wait()

        mid_odds = curr_odds.copy()
        self.add(mid_odds)

        self.play(
            curr_odds.move_to, odds_labels[2][1:], UR,
            path_arc=-30 * DEGREES
        )
        self.play(
            ChangeDecimalToValue(curr_odds[0], 90)
        )
        self.wait()
        new_odds = curr_odds.copy()
        new_odds[0].set_value(9)
        new_odds[2].set_value(4)
        self.play(
            FadeOut(curr_odds, 0.5 * UP),
            FadeIn(new_odds, 0.5 * UP),
        )
        curr_odds = new_odds
        self.wait()

        # Posterior as a probability
        final_frac = OldTex(
            "{{9} \\over {9} + {4}} \\approx 69.2\\%",
            tex_to_color_map={
                "{9}": YELLOW,
                "{4}": GREY_B,
            }
        )

        final_frac.next_to(odds_labels[2], DOWN, buff=0.4)
        self.play(FadeIn(final_frac, lag_ratio=0.2))
        self.wait()

        # Get rid of population
        self.play(
            LaggedStartMap(FadeOut, pop_groups, shift=DOWN, lag_ratio=0.3),
            FadeOut(h_line),
        )

        # Change symptom Bayes factor
        old_assumption = bf_equations[0][-3:]
        new_assumption = OldTex("2")
        new_assumption.replace(old_assumption, 1)
        new_assumption.scale(0.8)
        new_assumption.set_color(BLUE)

        change_word = OldTexText("Change this", font_size=72)
        change_word.next_to(assumption_word, DOWN, buff=1.5)
        change_word.shift(LEFT)
        change_word.set_color(RED)
        change_arrow = Arrow(change_word.get_top(), assumption_word.get_bottom())
        change_arrow.match_color(change_word)

        self.play(
            Write(change_word, run_time=1),
            GrowArrow(change_arrow),
        )
        self.wait()
        self.play(
            FadeOut(old_assumption, shift=0.5 * UP),
            FadeIn(new_assumption, shift=0.5 * UP),
            assumption_brace.set_width,
            1.5 * new_assumption.get_width(), {"stretch": True},
            FadeOut(mid_odds),
            FadeOut(curr_odds),
            FadeOut(final_frac),
        )
        self.wait()

        # New odds calculation
        curr_odds = new_left_odds.copy()

        self.play(
            curr_odds.move_to, mid_odds, UP,
            curr_odds.shift, SMALL_BUFF * RIGHT,
            FadeOut(odds_underlines[1]),
            path_arc=-30 * DEGREES,
        )
        self.play(ChangeDecimalToValue(curr_odds[2], 500))
        self.wait()

        mid_odds = curr_odds.copy()
        self.add(mid_odds)

        self.play(
            curr_odds.move_to, odds_labels[2][1:], UR,
            curr_odds.shift, 0.35 * RIGHT,
            FadeOut(odds_underlines[2]),
            path_arc=-30 * DEGREES,
        )
        self.play(ChangeDecimalToValue(curr_odds[0], 90))
        self.wait()

        new_odds = curr_odds.copy()
        new_odds[0].set_value(9)
        new_odds[2].set_value(50)
        new_odds.move_to(curr_odds, LEFT)
        self.play(
            FadeIn(new_odds, shift=0.5 * UP),
            FadeOut(curr_odds, shift=0.5 * UP),
        )
        curr_odds = new_odds
        self.wait()

        # Prob calculation
        new_final_frac = OldTex(
            "{{9} \\over {9} + {50}} \\approx 15.3\\%",
            tex_to_color_map={
                "{9}": YELLOW,
                "{50}": GREY_B,
            }
        )
        new_final_frac.replace(final_frac, 1)

        self.play(FadeIn(new_final_frac, lag_ratio=0.3))
        self.wait()
