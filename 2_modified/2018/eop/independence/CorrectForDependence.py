# ==============================================================================
# Scene:      CorrectForDependence
# Source:     videos/_2018/eop/independence.py (lines 2968-3093)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CorrectForDependence.py CorrectForDependence -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - removed in_place=True from Rotate (not a GL kwarg; GL rotates about the mobject center by default)
# ==============================================================================

from manim_imports_ext import *

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


class NameBinomial(Scene):
    CONFIG = {
        "flip_indices" : [0, 2, 4, 5, 6, 7],
    }
    def construct(self):
        self.name_distribution()
        self.add_quiz_questions()
        self.change_to_gender()
        self.change_bar_chart_for_gender_example()
        self.point_out_example_input()
        self.write_probability_of_girl()
        self.think_through_probabilities()

    def name_distribution(self):
        ns = [3, 10]
        p = 0.65
        charts = VGroup()
        for n in ns:
            dist = get_binomial_distribution(n, p)
            values = list(map(dist, list(range(n+1))))
            chart = BarChart(values, bar_names = list(range(n+1)))
            chart.to_edge(LEFT)
            charts.add(chart)

        probability = OldTex(
            "P(", "\\checkmark", ")", "=", str(p)
        )
        probability.set_color_by_tex("checkmark", GREEN)
        probability.move_to(charts, UP)

        title = OldTexText("``Binomial distribution''")
        title.next_to(charts, UP)
        title.to_edge(UP)
        formula = OldTex(
            "P(X=", "k", ")=", 
            "{n \\choose k}", 
            "p", "^k",
            "(1-", "p", ")", "^{n-", "k}",
            arg_separator = ""
        )
        formula.set_color_by_tex("p", YELLOW)
        formula.set_color_by_tex("k", GREEN)
        choose_part = formula.get_part_by_tex("choose")
        choose_part.set_color(WHITE)
        choose_part[-2].set_color(GREEN)
        formula.to_corner(UP+RIGHT)

        self.add(charts[0], probability)
        self.wait()
        self.play(Write(title))
        self.wait()
        self.play(ReplacementTransform(*charts))
        self.play(Write(formula))
        self.wait()
        self.play(
            formula.scale, 0.7,
            formula.next_to, charts, DOWN,
        )

        self.chart = charts[1]
        self.probability = probability
        self.title = title
        self.formula = formula

    def add_quiz_questions(self):
        n = 10
        checkmarks = VGroup(*[
            OldTex("\\checkmark").set_color(GREEN)
            for x in range(n)
        ])
        checkmarks.arrange(DOWN, buff = 0.3)
        crosses = VGroup()
        arrows = VGroup()
        for checkmark in checkmarks:
            cross = OldTex("\\times")
            cross.set_color(RED)
            cross.next_to(checkmark, RIGHT, LARGE_BUFF)
            crosses.add(cross)
            arrow = Arrow(
                checkmark, cross,
                tip_length = 0.15,
                color = WHITE
            )
            arrows.add(arrow)
        full_group = VGroup(checkmarks, crosses, arrows)
        full_group.center().to_corner(UP + RIGHT, buff = MED_LARGE_BUFF)
        flip_indices = self.flip_indices
        flipped_arrows, faded_crosses, full_checks = [
            VGroup(*[group[i] for i in flip_indices])
            for group in (arrows, crosses, checkmarks)
        ]
        faded_checkmarks = VGroup(*[m for m in checkmarks if m not in full_checks])

        self.play(*[
            LaggedStartMap(
                Write, mob,
                run_time = 3,
                lag_ratio = 0.3
            )
            for mob in full_group
        ])
        self.wait()
        self.play(
            LaggedStartMap(
                Rotate, flipped_arrows,
                angle = np.pi,
                # CHANGE: Rotate(in_place=True) is not a GL kwarg; GL Rotate already rotates about the mobject center by default

                run_time = 2,
                lag_ratio = 0.5
            ),
            faded_crosses.set_fill, None, 0.5,
            faded_checkmarks.set_fill, None, 0.5,
        )
        self.wait()

        self.checkmarks = checkmarks
        self.crosses = crosses
        self.arrows = arrows

    def change_to_gender(self):
        flip_indices = self.flip_indices
        male = self.get_male()
        female = self.get_female()

        girls, boys = [
            VGroup(*[
                template.copy().move_to(mob)
                for mob in group
            ])
            for template, group in [
                (female, self.checkmarks), (male, self.crosses)
            ]
        ]
        for i in range(len(boys)):
            mob = boys[i] if i in flip_indices else girls[i]
            mob.set_fill(opacity = 0.5)

        brace = Brace(girls, LEFT)
        words = brace.get_text("$n$ children")

        self.play(
            GrowFromCenter(brace),
            FadeIn(words)
        )
        for m1, m2 in (self.crosses, boys), (self.checkmarks, girls):
            self.play(ReplacementTransform(
                m1, m2,
                lag_ratio = 0.5,
                run_time = 3
            ))
        self.wait()

        self.boys = boys
        self.girls = girls
        self.children_brace = brace
        self.n_children_words = words

    def change_bar_chart_for_gender_example(self):
        checkmark = self.probability.get_part_by_tex("checkmark")
        p_mob = self.probability[-1]

        female = self.get_female()
        female.move_to(checkmark)
        new_p_mob = OldTex("0.49")
        new_p_mob.move_to(p_mob, LEFT)

        dist = get_binomial_distribution(10, 0.49)
        values = list(map(dist, list(range(11))))

        self.play(
            Transform(checkmark, female),
            Transform(p_mob, new_p_mob),
        )
        self.play(self.chart.change_bar_values, values)
        self.wait()

    def point_out_example_input(self):
        boy_girl_groups = VGroup(*[
            VGroup(boy, girl)
            for boy, girl in zip(self.boys, self.girls)
        ])
        girl_rects = VGroup(*[
            SurroundingRectangle(
                boy_girl_groups[i], 
                color = MAROON_B,
                buff = SMALL_BUFF,
            )
            for i in sorted(self.flip_indices)
        ])

        chart = self.chart
        n_girls = len(girl_rects)
        chart_rect = SurroundingRectangle(
            VGroup(chart.bars[n_girls], chart.bar_labels[n_girls]),
            buff = SMALL_BUFF
        )

        prob = OldTex(
            "P(", "\\# \\text{Girls}", "=", "6", ")"
        )
        prob.set_color_by_tex("Girls", MAROON_B)
        arrow = Arrow(UP, ORIGIN, tip_length = 0.15)
        arrow.set_color(MAROON_B)
        arrow.next_to(prob, DOWN)
        prob.add(arrow)
        prob.next_to(chart_rect, UP)
        girls = VGroup(*[self.girls[i] for i in self.flip_indices])


        self.play(ShowCreation(chart_rect))
        self.play(LaggedStartMap(
            ShowCreation, girl_rects,
            run_time = 2,
            lag_ratio = 0.5,
        ))
        self.wait()

        self.play(Write(prob))
        self.play(LaggedStartMap(
            Indicate, girls,
            run_time = 3,
            lag_ratio = 0.3,
            rate_func = there_and_back
        ))
        self.play(FadeOut(prob))
        self.wait()

        self.chart_rect = chart_rect
        self.girl_rects = girl_rects

    def write_probability_of_girl(self):
        probability = self.probability
        probability_copies = VGroup(*[
            probability.copy().scale(0.7).next_to(
                girl, LEFT, MED_LARGE_BUFF
            )
            for girl in self.girls
        ])

        self.play(FocusOn(probability))
        self.play(Indicate(probability[-1]))
        self.wait()
        self.play(
            ReplacementTransform(
                VGroup(probability.copy()), probability_copies
            ),
            FadeOut(self.children_brace),
            FadeOut(self.n_children_words),
        )
        self.wait()

        self.probability_copies = probability_copies

    def think_through_probabilities(self):
        randy = Randolph().scale(0.5)
        randy.next_to(self.probability_copies, LEFT, LARGE_BUFF)

        self.play(FadeIn(randy))
        self.play(randy.change, "pondering")
        self.play(Blink(randy))
        self.wait()

    ##

    def get_male(self):
        return OldTex("\\male").scale(1.3).set_color(BLUE)

    def get_female(self):
        return OldTex("\\female").scale(1.3).set_color(MAROON_B)


class CorrectForDependence(NameBinomial):
    CONFIG = {
        "flip_indices" : [3, 6, 8],
    }
    def setup(self):
        self.force_skipping()
        self.name_distribution()
        self.add_quiz_questions()
        self.revert_to_original_skipping_status()

    def construct(self):
        self.mention_dependence()
        self.show_tendency_to_align()
        self.adjust_chart()

    def mention_dependence(self):
        brace = Brace(self.checkmarks, LEFT)
        words = brace.get_text("What if there's \\\\ correlation?")
        formula = self.formula
        cross = Cross(formula)

        self.play(
            GrowFromCenter(brace),
            Write(words)
        )
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()

    def show_tendency_to_align(self):
        checkmarks = self.checkmarks
        arrows = self.arrows
        crosses = self.crosses
        groups = [
            VGroup(*trip)
            for trip in zip(checkmarks, arrows, crosses)
        ]
        top_rect = SurroundingRectangle(groups[0])
        top_rect.set_color(GREEN)
        indices_to_follow = [1, 4, 5, 7]

        self.play(ShowCreation(top_rect))
        self.play(*self.get_arrow_flip_anims([0]))
        self.wait()
        self.play(*self.get_arrow_flip_anims(indices_to_follow))
        self.play(FocusOn(self.chart.bars))

    def adjust_chart(self):
        chart = self.chart
        bars = chart.bars
        old_bars = bars.copy()
        old_bars.generate_target()
        bars.generate_target()
        for group, vect in (old_bars, LEFT), (bars, RIGHT):
            for bar in group.target:
                side = bar.get_edge_center(vect)
                bar.stretch(0.5, 0)
                bar.move_to(side, vect)
        for bar in old_bars.target:
            bar.set_color(average_color(RED_E, BLACK))

        dist = get_binomial_distribution(10, 0.65)
        values = np.array(list(map(dist, list(range(11)))))
        alt_values = values + 0.1
        alt_values[0] -= 0.06
        alt_values[1] -= 0.03
        alt_values /= sum(alt_values)
        arrows = VGroup()
        arrow_template = Arrow(
            0.5*UP, ORIGIN, buff = 0, 
            tip_length = 0.15,
            color = WHITE
        )
        for value, alt_value, bar in zip(values, alt_values, bars):
            arrow = arrow_template.copy()
            if value < alt_value:
                arrow.rotate(np.pi, about_point = ORIGIN)
            arrow.next_to(bar, UP)
            arrows.add(arrow)

        self.play(
            MoveToTarget(old_bars),
            MoveToTarget(bars),
        )
        self.wait()
        self.play(*list(map(ShowCreation, arrows)))
        self.play(chart.change_bar_values, alt_values)

    ######

    def get_arrow_flip_anims(self, indices):
        checkmarks, arrows, crosses = movers = [
            VGroup(*[
                group[i]
                for i in range(len(group))
                if i in indices
            ])
            for group in (self.checkmarks, self.arrows, self.crosses)
        ]
        for arrow in arrows:
            arrow.target = arrow.deepcopy()
            arrow.target.rotate(np.pi)
        for group in checkmarks, crosses:
            for mob, arrow in zip(group, arrows):
                mob.generate_target()
                c = mob.get_center()
                start, end = arrow.target.get_start_and_end()
                to_end = get_norm(c - end)
                to_start = get_norm(c - start)
                if to_end < to_start:
                    mob.target.set_fill(opacity = 1)
                else:
                    mob.target.set_fill(opacity = 0.5)
        for checkmark in checkmarks:
            checkmark.target.scale(1.2)

        kwargs = {"path_arc" : np.pi}
        if len(indices) > 1:
            kwargs.update({"run_time" : 2})
        return [
            LaggedStartMap(
                MoveToTarget, mover,
                **kwargs
            )
            for mover in movers
        ]
