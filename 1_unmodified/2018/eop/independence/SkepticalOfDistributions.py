# ==============================================================================
# Scene:      SkepticalOfDistributions
# Source:     videos/_2018/eop/independence.py (lines 3282-3449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SkepticalOfDistributions.py SkepticalOfDistributions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import scipy

def get_binomial_distribution(n, p):
    return lambda k : choose(n, k)*(p**(k))*((1-p)**(n-k))


class SkepticalOfDistributions(TeacherStudentsScene):
    CONFIG = {
        "chart_height" : 3,
    }
    def construct(self):
        self.show_binomial()
        self.show_alternate_distributions()
        self.emphasize_underweighted_tails()

    def show_binomial(self):
        binomial = self.get_binomial()
        binomial.next_to(self.teacher.get_corner(UP+LEFT), UP)
        title = OldTexText("Probable scores")
        title.scale(0.85)
        title.next_to(binomial.bars, UP, 1.5*LARGE_BUFF)

        self.play(
            Write(title, run_time = 1),
            FadeIn(binomial, run_time = 1, lag_ratio = 0.5),
            self.teacher.change, "raise_right_hand"
        )
        for values in binomial.values_list:
            self.play(binomial.change_bar_values, values)
            self.wait()
        self.student_says(
            "Is that valid?", target_mode = "sassy",
            index = 0,
            run_time = 1
        )
        self.play(self.teacher.change, "guilty")
        self.wait()

        binomial.add(title)
        self.binomial = binomial

    def show_alternate_distributions(self):
        poisson = self.get_poisson()
        VGroup(poisson, poisson.title).next_to(
            self.students, UP, LARGE_BUFF
        ).shift(RIGHT)
        gaussian = self.get_gaussian()
        VGroup(gaussian, gaussian.title).next_to(
            poisson, RIGHT, LARGE_BUFF
        )


        self.play(
            FadeIn(poisson, lag_ratio = 0.5),
            RemovePiCreatureBubble(self.students[0]),
            self.teacher.change, "raise_right_hand",
            self.binomial.scale, 0.5,
            self.binomial.to_corner, UP+LEFT,
        )
        self.play(Write(poisson.title, run_time = 1))
        self.play(FadeIn(gaussian, lag_ratio = 0.5))
        self.play(Write(gaussian.title, run_time = 1))
        self.wait(2)
        self.play_student_changes(
            *["sassy"]*3,
            added_anims = [self.teacher.change, "plain"]
        )
        self.wait(2)

        self.poisson = poisson
        self.gaussian = gaussian

    def emphasize_underweighted_tails(self):
        poisson_arrows = VGroup()
        arrow_template = Arrow(
            ORIGIN, UP, color = GREEN,
            tip_length = 0.15
        )
        for bar in self.poisson.bars[-4:]:
            arrow = arrow_template.copy()
            arrow.next_to(bar, UP, SMALL_BUFF)
            poisson_arrows.add(arrow)

        gaussian_arrows = VGroup()
        for prop in 0.2, 0.8:
            point = self.gaussian[0][0].point_from_proportion(prop)
            arrow = arrow_template.copy()
            arrow.next_to(point, UP, SMALL_BUFF)
            gaussian_arrows.add(arrow)

        for arrows in poisson_arrows, gaussian_arrows:
            self.play(
                ShowCreation(
                    arrows, 
                    lag_ratio = 0.5,
                    run_time = 2
                ),
                *[
                    ApplyMethod(pi.change, "thinking", arrows)
                    for pi in self.pi_creatures
                ]
            )
            self.wait()
        self.wait(2)

    ####

    def get_binomial(self):
        k_range = list(range(11))
        dists = [
            get_binomial_distribution(10, p)
            for p in (0.2, 0.8, 0.5)
        ]
        values_list = [
            list(map(dist, k_range))
            for dist in dists
        ]
        chart = BarChart(
            values = values_list[-1],
            bar_names = k_range
        )
        chart.set_height(self.chart_height)
        chart.values_list = values_list
        return chart

    def get_poisson(self):
        k_range = list(range(11))
        L = 2
        values = [
            np.exp(-L) * (L**k) / (scipy.special.gamma(k+1))
            for k in k_range
        ]
        chart = BarChart(
            values = values,
            bar_names = k_range,
            bar_colors = [RED, YELLOW]
        )
        chart.set_height(self.chart_height)
        title = OldTexText(
            "Poisson distribution \\\\",
            "$e^{-\\lambda}\\frac{\\lambda^k}{k!}$"
        )
        title.scale(0.75)
        title.move_to(chart, UP)
        title.shift(MED_SMALL_BUFF*RIGHT)
        title[0].shift(SMALL_BUFF*UP)
        chart.title = title

        return chart

    def get_gaussian(self):
        axes = VGroup(self.binomial.x_axis, self.binomial.y_axis).copy()
        graph = FunctionGraph(
            lambda x : 5*np.exp(-x**2),
            mark_paths_closed = True,
            fill_color = BLUE_E,
            fill_opacity = 1,
            stroke_color = BLUE,
        )
        graph.set_width(axes.get_width())
        graph.move_to(axes[0], DOWN)

        title = OldTexText(
            "Gaussian distribution \\\\ ",
            "$\\frac{1}{\\sqrt{2\\pi \\sigma^2}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$"
        )
        title.scale(0.75)
        title.move_to(axes, UP)
        title.shift(MED_SMALL_BUFF*RIGHT)
        title[0].shift(SMALL_BUFF*UP)
        result = VGroup(axes, graph)
        result.title = title

        return result
