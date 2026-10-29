# ==============================================================================
# Scene:      FormulaCanBeRediscovered
# Source:     videos/_2018/eop/independence.py (lines 3234-3252)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FormulaCanBeRediscovered.py FormulaCanBeRediscovered -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


class GeneralBinomialDistributionValues(Scene):
    CONFIG = {
        "n" : 10,
        "alt_n" : 8,
        "p" : 0.49,
    }
    def construct(self):
        self.add_chart()
        self.show_a_few_values()
        self.compare_to_pascal_row()
        self.mention_center_concentration()
        self.generalize()
        self.play_with_p_value()

    def add_chart(self):
        dist = get_binomial_distribution(self.n, self.p)
        values = list(map(dist, list(range(self.n+1))))
        chart = BarChart(
            values,
            bar_names = list(range(self.n+1))
        )
        chart.to_edge(LEFT)

        full_probability = self.get_probability_expression(
            "10", "k", "(0.49)", "(0.51)"
        )
        full_probability.next_to(chart, UP, aligned_edge = LEFT)

        self.add(chart)

        self.chart = chart
        self.full_probability = full_probability

    def show_a_few_values(self):
        chart = self.chart
        probabilities = VGroup()
        for i, bar in enumerate(chart.bars):
            prob = self.get_probability_expression(
                "10", str(i), "(0.49)", "(0.51)",
                full = False
            )
            arrow = Arrow(
                UP, DOWN, 
                color = WHITE,
                tip_length = 0.15
            )
            arrow.next_to(bar, UP, SMALL_BUFF)
            prob.next_to(arrow, UP, SMALL_BUFF)
            ##
            prob.shift(LEFT)
            prob.shift_onto_screen()
            prob.shift(RIGHT)
            ##
            prob.add(arrow)            
            probabilities.add(prob)
        shown_prob = probabilities[6].copy()

        self.play(FadeIn(shown_prob))
        self.wait()
        self.play(LaggedStartMap(
            FadeIn, self.full_probability,
            run_time = 4,
            lag_ratio = 0.5,
        ))
        self.wait()
        last_k = 6
        for k in 3, 8, 5, 9, 6:
            self.play(Transform(
                shown_prob, probabilities[k],
                path_arc = -np.pi/6 if k > last_k else np.pi/6
            ))
            self.wait(2)
            last_k = k

        self.shown_prob = shown_prob

    def compare_to_pascal_row(self):
        triangle = PascalsTriangle(nrows = 11)
        triangle.set_width(6)
        triangle.to_corner(UP+RIGHT)
        last_row = VGroup(*[
            triangle.coords_to_mobs[10][k]
            for k in range(11)
        ])
        ten_choose_ks = VGroup()
        for k, mob in enumerate(last_row):
            ten_choose_k = OldTex("10 \\choose %s"%k)
            ten_choose_k.scale(0.5)
            ten_choose_k.stretch(0.8, 0)
            ten_choose_k.next_to(mob, DOWN)
            ten_choose_ks.add(ten_choose_k)
        ten_choose_ks.set_color_by_gradient(BLUE, YELLOW)

        self.play(
            LaggedStartMap(FadeIn, triangle),
            FadeOut(self.shown_prob)
        )
        self.play(
            last_row.set_color_by_gradient, BLUE, YELLOW,
            Write(ten_choose_ks, run_time = 2)
        )
        self.wait()
        self.play(ApplyWave(self.chart.bars, direction = UP))
        self.play(FocusOn(last_row))
        self.play(LaggedStartMap(
            ApplyMethod, last_row,
            lambda m : (m.scale, 1.2),
            rate_func = there_and_back,
        ))
        self.wait()

        self.pascals_triangle = triangle
        self.ten_choose_ks = ten_choose_ks

    def mention_center_concentration(self):
        bars = self.chart.bars
        bars.generate_target()
        bars.save_state()
        bars.target.arrange(UP, buff = 0)
        bars.target.stretch_to_fit_height(self.chart.height)
        bars.target.move_to(
            self.chart.x_axis.point_from_proportion(0.05),
            DOWN
        )
        brace = Brace(VGroup(*bars.target[4:7]), RIGHT)
        words = brace.get_text("Most probability \\\\ in middle values")

        self.play(MoveToTarget(bars))
        self.play(
            GrowFromCenter(brace),
            FadeIn(words)
        )
        self.wait(2)
        self.play(
            bars.restore,
            *list(map(FadeOut, [
                brace, words, 
                self.pascals_triangle,
                self.ten_choose_ks
            ]))
        )

    def generalize(self):
        alt_n = self.alt_n
        dist = get_binomial_distribution(alt_n, self.p)
        values = list(map(dist, list(range(alt_n + 1))))
        alt_chart = BarChart(
            values, bar_names = list(range(alt_n + 1))
        )
        alt_chart.move_to(self.chart)

        alt_probs = [
            self.get_probability_expression("n", "k", "(0.49)", "(0.51)"),
            self.get_probability_expression("n", "k", "p", "(1-p)"),
        ]
        for prob in alt_probs:
            prob.move_to(self.full_probability)

        self.play(FocusOn(
            self.full_probability.get_part_by_tex("choose")
        ))
        self.play(
            ReplacementTransform(self.chart, alt_chart),
            Transform(self.full_probability, alt_probs[0])
        )
        self.chart = alt_chart
        self.wait(2)
        self.play(Transform(self.full_probability, alt_probs[1]))
        self.wait()

    def play_with_p_value(self):
        p = self.p
        interval = UnitInterval(color = WHITE)
        interval.set_width(5)
        interval.next_to(self.full_probability, DOWN, LARGE_BUFF)
        interval.add_numbers(0, 0.5, 1)
        triangle = RegularPolygon(
            n=3, start_angle = -np.pi/2,
            fill_color = MAROON_B,
            fill_opacity = 1,
            stroke_width = 0,
        )
        triangle.set_height(0.25)
        triangle.move_to(interval.number_to_point(p), DOWN)
        p_mob = OldTex("p")
        p_mob.set_color(MAROON_B)
        p_mob.next_to(triangle, UP, SMALL_BUFF)
        triangle.add(p_mob)

        new_p_values = [0.8, 0.4, 0.2, 0.9, 0.97, 0.6]

        self.play(
            ShowCreation(interval),
            Write(triangle, run_time = 1)
        )
        self.wait()
        for new_p in new_p_values:
            p = new_p
            dist = get_binomial_distribution(self.alt_n, p)
            values = list(map(dist, list(range(self.alt_n + 1))))
            self.play(
                self.chart.change_bar_values, values,
                triangle.move_to, interval.number_to_point(p), DOWN
            )
            self.wait()

    #######

    def get_probability_expression(
        self, n = "n", k = "k", p = "p", q = "(1-p)",
        full = True
        ):
        args = []
        if full:
            args += ["P(", "\\# \\text{Girls}", "=", k, ")", "="]
        args += [
            "{%s \\choose %s}"%(n, k),
            p, "^%s"%k,
            q, "^{%s"%n, "-", "%s}"%k,
        ]
        result = OldTex(*args, arg_separator = "")
        color_map = {
            "Girls" : MAROON_B,
            n : WHITE,
            k : YELLOW,
            p : MAROON_B,
            q : BLUE,
        }
        result.set_color_by_tex_to_color_map(color_map)
        choose_part = result.get_part_by_tex("choose")
        choose_part.set_color(WHITE)
        VGroup(*choose_part[1:1+len(n)]).set_color(color_map[n])
        VGroup(*choose_part[-1-len(k):-1]).set_color(color_map[k])
        return result


class PointOutSimplicityOfFormula(TeacherStudentsScene, GeneralBinomialDistributionValues):
    def construct(self):
        prob = self.get_probability_expression(full = False)
        corner = self.teacher.get_corner(UP+LEFT)
        prob.next_to(corner, UP, MED_LARGE_BUFF)
        prob.save_state()
        prob.move_to(corner)
        prob.set_fill(opacity = 0)

        self.play(
            prob.restore,
            self.teacher.change_mode, "raise_right_hand"
        )
        self.play_student_changes(
            *["pondering"]*3,
            look_at = prob
        )
        self.wait()
        self.student_says(
            "Simpler than I feared",
            target_mode = "hooray",
            index = 0,
            added_anims = [prob.to_corner, UP+RIGHT]
        )
        self.wait()
        self.teacher_says("Due to \\\\ independence")
        self.wait(2)


class FormulaCanBeRediscovered(PointOutSimplicityOfFormula):
    def construct(self):
        prob = self.get_probability_expression(full = False)
        corner = self.teacher.get_corner(UP+LEFT)
        prob.next_to(corner, UP, MED_LARGE_BUFF)
        brace = Brace(prob, UP)
        rediscover = brace.get_text("Rediscover")

        self.play(
            Write(prob),
            self.teacher.change, "hesitant", prob
        )
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(rediscover, run_time = 1)
        )
        self.play_student_changes(*["happy"]*3)
        self.wait(2)
