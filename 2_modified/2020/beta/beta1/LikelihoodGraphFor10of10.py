# ==============================================================================
# Scene:      LikelihoodGraphFor10of10
# Source:     videos/_2020/beta/beta1.py (lines 3398-3559)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl LikelihoodGraphFor10of10.py LikelihoodGraphFor10of10 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - SIRGraph/Histogram's `self.data` clashes with manimgl's Mobject.data (it was a list); renamed to graph_data / hist_data
#   - DecimalNumber no longer stores initial_config; num_decimal_places is a direct attribute
# ==============================================================================

from manim_imports_ext import *
import scipy.stats


# ----- From _2020/beta/helpers.py -----

CMARK_TEX = "\\text{\\ding{51}}"


XMARK_TEX = "\\text{\\ding{55}}"


# CHANGE: `self.data` clashes with manimgl's Mobject.data; in Histogram it is renamed to self.hist_data
class Histogram(Group):
    CONFIG = {
        "height": 5,
        "width": 10,
        "y_max": 1,
        "y_axis_numbers_to_show": range(20, 120, 20),
        "y_axis_label_height": 0.25,
        "y_tick_freq": 0.2,
        "x_label_freq": 1,
        "include_h_lines": True,
        "h_line_style": {
            "stroke_width": 1,
            "stroke_color": GREY_B,
            # "stroke_behind": True,
        },
        "bar_style": {
            "stroke_width": 1,
            "stroke_color": WHITE,
            "fill_opacity": 1,
        },
        "bar_colors": [BLUE, GREEN]
    }

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.hist_data = data

        self.add_axes()
        if self.include_h_lines:
            self.add_h_lines()
        self.add_bars(data)
        self.add_x_axis_labels()
        self.add_y_axis_labels()

    def add_axes(self):
        n_bars = len(self.hist_data)
        axes_config = {
            "x_min": 0,
            "x_max": n_bars,
            "x_axis_config": {
                "unit_size": self.width / n_bars,
                "include_tip": False,
            },
            "y_min": 0,
            "y_max": self.y_max,
            "y_axis_config": {
                "unit_size": self.height / self.y_max,
                "include_tip": False,
                "tick_frequency": self.y_tick_freq,
            },
        }
        axes = Axes(**axes_config)
        axes.center()
        self.axes = axes
        self.add(axes)

    def add_h_lines(self):
        axes = self.axes
        axes.h_lines = VGroup()
        for tick in axes.y_axis.tick_marks:
            line = Line(**self.h_line_style)
            line.match_width(axes.x_axis)
            line.move_to(tick.get_center(), LEFT)
            axes.h_lines.add(line)
        axes.add(axes.h_lines)

    def add_bars(self, data):
        self.bars = self.get_bars(data)
        self.add(self.bars)

    def add_x_axis_labels(self):
        axes = self.axes
        axes.x_labels = VGroup()
        for x, bar in list(enumerate(self.bars))[::self.x_label_freq]:
            label = Integer(x)
            label.set_height(0.25)
            label.next_to(bar, DOWN)
            axes.x_labels.add(label)
        axes.add(axes.x_labels)

    def add_y_axis_labels(self):
        axes = self.axes
        labels = VGroup()
        for value in self.y_axis_numbers_to_show:
            label = Integer(value, unit="\\%")
            label.set_height(self.y_axis_label_height)
            label.next_to(axes.y_axis.n2p(0.01 * value), LEFT)
            labels.add(label)
        axes.y_labels = labels
        axes.y_axis.add(labels)

    # Bar manipulations
    def get_bars(self, data):
        portions = np.array(data).astype(float)
        total = portions.sum()
        if total == 0:
            portions[:] = 0
        else:
            portions /= total
        bars = VGroup()
        for x, prop in enumerate(portions):
            bar = Rectangle()
            width = get_norm(self.axes.c2p(1, 0) - self.axes.c2p(0, 0))
            height = get_norm(self.axes.c2p(0, 1) - self.axes.c2p(0, 0))
            bar.set_width(width)
            bar.set_height(height * prop, stretch=True)
            bar.move_to(self.axes.c2p(x, 0), DL)
            bars.add(bar)

        bars.set_submobject_colors_by_gradient(*self.bar_colors)
        bars.set_style(**self.bar_style)
        return bars


def get_beta_dist_axes(y_max=20, y_unit=2, label_y=False, **kwargs):
    config = {
        "x_min": 0,
        "x_max": 1,
        "x_axis_config": {
            "unit_size": 0.1,
            "tick_frequency": 0.1,
            "include_tip": False,
        },
        "y_min": 0,
        "y_max": y_max,
        "y_axis_config": {
            "unit_size": 1,
            "tick_frequency": y_unit,
            "include_tip": False,
        },
    }
    result = Axes(**config)
    origin = result.c2p(0, 0)
    kw = {
        "about_point": origin,
        "stretch": True,
    }
    result.x_axis.set_width(11, **kw)
    result.y_axis.set_height(6, **kw)

    x_vals = np.arange(0, 1, 0.2) + 0.2
    result.x_axis.add_numbers(
        *x_vals,
        num_decimal_places=1
    )

    if label_y:
        result.y_axis.add_numbers(
            *np.arange(y_unit, y_max, y_unit)
        )
        label = OldTexText("Probability density")
        label.scale(0.5)
        label.next_to(result.y_axis.get_top(), UR, SMALL_BUFF)
        label.next_to(result.y_axis, UP, SMALL_BUFF)
        label.align_to(result.y_axis.numbers, LEFT)
        result.add(label)
        result.y_axis_label = label

    result.to_corner(DR, LARGE_BUFF)

    return result


def get_checks_and_crosses(bools, width=12):
    result = VGroup()
    for positive in bools:
        if positive:
            mob = OldTex(CMARK_TEX)
            mob.set_color(GREEN)
        else:
            mob = OldTex(XMARK_TEX)
            mob.set_color(RED)
        mob.positive = positive
        mob.set_width(0.5)
        result.add(mob)
    result.arrange(RIGHT, buff=MED_SMALL_BUFF)
    result.set_width(width)
    return result


def get_random_checks_and_crosses(n=50, s=0.95, width=12):
    return get_checks_and_crosses(
        bools=(np.random.random(n) < s),
        width=width
    )


def get_prob_review_label(n_positive, n_negative, s=0.95):
    label = OldTex(
        "P(",
        f"{n_positive}\\,{CMARK_TEX}", ",\\,",
        f"{n_negative}\\,{XMARK_TEX}",
        "\\,|\\,",
        "s = {:.2f}".format(s),
        ")",
    )
    label.set_color_by_tex_to_color_map({
        CMARK_TEX: GREEN,
        XMARK_TEX: RED,
        "0.95": YELLOW,
    })
    return label


def get_binomial_formula(n, k, p):
    n_mob = Integer(n, color=WHITE)
    k_mob = Integer(k, color=GREEN)
    nmk_mob = Integer(n - k, color=RED)
    p_mob = DecimalNumber(p, color=YELLOW)

    n_str = "N" * len(n_mob)
    k_str = "K" * len(k_mob)
    p_str = "P" * len(k_mob)
    nmk_str = "M" * len(nmk_mob)

    formula = OldTex(
        "\\left(",
        "{" + n_str,
        "\\over",
        k_str + "}",
        "\\right)",
        "(", p_str, ")",
        "^{" + k_str + "}",
        "(1 - ", p_str, ")",
        "^{" + nmk_str + "}",
    )
    parens = VGroup(formula[0], formula[4])
    parens.space_out_submobjects(0.7)
    formula.remove(formula.get_part_by_tex("\\over"))
    pairs = (
        (n_mob, n_str),
        (k_mob, k_str),
        (nmk_mob, nmk_str),
        (p_mob, p_str),
    )
    for mob, tex in pairs:
        parts = formula.get_parts_by_tex(tex)
        for part in parts:
            mob_copy = mob.copy()
            i = formula.index_of_part_by_tex(tex)
            mob_copy.match_height(part)
            mob_copy.move_to(part, DOWN)
            formula.replace_submobject(i, mob_copy)

    terms = VGroup(
        formula[:4],
        formula[4:7],
        formula[7],
        formula[8:11],
        formula[11],
    )
    ys = [term.get_y() for term in terms]
    terms.arrange(RIGHT, buff=SMALL_BUFF)
    terms[0].shift(SMALL_BUFF * LEFT)
    for term, y in zip(terms, ys):
        term.set_y(y)

    return formula


def reverse_smooth(t):
    return smooth(1 - t)



# ----- From _2020/beta/beta1.py -----

class SimulationsOf50Reviews(Scene):
    CONFIG = {
        "s": 0.95,
        "histogram_config": {
            "x_label_freq": 5,
            "y_axis_numbers_to_show": range(10, 70, 10),
            "y_max": 0.6,
            "y_tick_freq": 0.1,
            "height": 5,
            "bar_colors": [BLUE],
        },
        "random_seed": 1,
    }

    def construct(self):
        self.add_s_label()

        data = np.zeros(51)
        histogram = self.get_histogram(data)

        row = self.get_row()
        count = self.get_count(row)
        original_count = count.get_value()
        count.set_value(0)

        self.add(histogram)
        self.play(
            ShowIncreasingSubsets(row),
            ChangeDecimalToValue(count, original_count)
        )

        # Run many samples
        arrow = Vector(0.5 * DOWN)
        arrow.set_stroke(width=5)
        arrow.set_color(YELLOW)
        arrow.next_to(histogram.bars[10], UP, SMALL_BUFF)

        total_data_label = VGroup(
            OldTexText("Total samples: "),
            Integer(1),
        )
        total_data_label.arrange(RIGHT)
        total_data_label.next_to(row, DOWN)
        total_data_label.add_updater(
            lambda m: m[1].set_value(data.sum())
        )

        def update(dummy, n_added_data_points=0):
            new_row = self.get_row()
            row.become(new_row)
            num_positive = sum([m.positive for m in new_row])
            count.set_value(num_positive)
            data[num_positive] += 1
            if n_added_data_points:
                values = np.random.random((n_added_data_points, 50))
                counts = (values < self.s).sum(1)
                for i in range(len(data)):
                    data[i] += (counts == i).sum()
            histogram.bars.become(histogram.get_bars(data))
            histogram.bars.set_fill(GREY_C)
            histogram.bars[48].set_fill(GREEN)
            arrow.next_to(histogram.bars[num_positive], UP, SMALL_BUFF)

        self.add(arrow, total_data_label)
        group = VGroup(histogram.bars, row, count, arrow)
        self.play(
            UpdateFromFunc(group, update),
            run_time=4
        )
        self.play(
            UpdateFromFunc(
                group,
                lambda m: update(m, 1000)
            ),
            run_time=4
        )
        random.seed(0)
        np.random.seed(0)
        update(group)
        self.wait()

        # Show 48 bar
        axes = histogram.axes
        y = choose(50, 48) * (self.s)**48 * (1 - self.s)**2
        line = DashedLine(
            axes.c2p(0, y),
            axes.c2p(51, y),
        )
        label = OldTex("{:.1f}\\%".format(100 * y))
        fix_percent(label.family_members_with_points()[-1])
        label.next_to(line, RIGHT)

        self.play(
            ShowCreation(line),
            FadeInFromPoint(label, line.get_start())
        )

    def add_s_label(self):
        s_label = OldTex("s = 0.95")
        s_label.set_height(0.3)
        s_label.to_corner(UL, buff=MED_SMALL_BUFF)
        s_label.shift(0.8 * DOWN)
        s_label.set_color(YELLOW)
        self.add(s_label)

    def get_histogram(self, data):
        histogram = Histogram(
            data, **self.histogram_config
        )
        histogram.to_edge(DOWN)
        return histogram

    def get_row(self, n=50):
        row = get_random_checks_and_crosses(n, self.s)
        row.move_to(3.5 * UP)
        return row

    def get_count(self, row):
        count = Integer(sum([m.positive for m in row]))
        count.set_height(0.3)
        count.next_to(row, RIGHT)
        return count


class ShowBinomialFormula(SimulationsOf50Reviews):
    CONFIG = {
        "histogram_config": {
            "x_label_freq": 5,
            "y_axis_numbers_to_show": range(10, 40, 10),
            "y_max": 0.3,
            "y_tick_freq": 0.1,
            "height": 2.5,
            "bar_colors": [BLUE],
        },
        "random_seed": 0,
    }

    def construct(self):
        # Add histogram
        dist = scipy.stats.binom(50, self.s)
        data = np.array([
            dist.pmf(x)
            for x in range(0, 51)
        ])
        histogram = self.get_histogram(data)
        histogram.bars.set_fill(GREY_C)
        histogram.bars[48].set_fill(GREEN)
        self.add(histogram)

        row = self.get_row()
        self.add(row)

        # Formula
        prob_label = get_prob_review_label(48, 2)
        eq = OldTex("=")
        formula = get_binomial_formula(50, 48, self.s)

        equation = VGroup(
            prob_label,
            eq,
            formula,
        )
        equation.arrange(RIGHT)
        equation.next_to(histogram, UP, LARGE_BUFF)
        equation.to_edge(RIGHT)

        prob_label.save_state()
        arrow = Vector(DOWN)
        arrow.next_to(histogram.bars[48], UP, SMALL_BUFF)
        prob_label.next_to(arrow, UP)

        self.play(
            FadeIn(prob_label),
            GrowArrow(arrow),
        )
        for mob in prob_label[1::2]:
            line = Underline(mob)
            line.match_color(mob)
            self.play(ShowCreationThenDestruction(line))
            self.wait(0.5)
        self.play(
            Restore(prob_label),
            FadeIn(equation[1:], lag_ratio=0.1),
        )
        self.wait()

        self.explain_n_choose_k(row, formula)

        # Circle formula parts
        rect1 = SurroundingRectangle(formula[4:8])
        rect2 = SurroundingRectangle(formula[8:])
        rect1.set_stroke(GREEN, 2)
        rect2.set_stroke(RED, 2)

        for rect in rect1, rect2:
            self.play(ShowCreation(rect))
            self.wait()
            self.play(FadeOut(rect))

        # Show numerical answer
        eq2 = OldTex("=")
        value = DecimalNumber(dist.pmf(48), num_decimal_places=5)
        rhs = VGroup(eq2, value)
        rhs.arrange(RIGHT)
        rhs.match_y(eq)
        rhs.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        self.play(
            FadeIn(value, LEFT),
            FadeIn(eq2),
            equation.next_to, eq2, LEFT,
        )
        self.wait()

        # Show alternate values of k
        n = 50
        for k in it.chain(range(47, 42, -1), range(43, 51), [49, 48]):
            new_prob_label = get_prob_review_label(k, n - k)
            new_prob_label.replace(prob_label)
            prob_label.become(new_prob_label)
            new_formula = get_binomial_formula(n, k, self.s)
            new_formula.replace(formula)
            formula.set_submobjects(new_formula)

            value.set_value(dist.pmf(k))
            histogram.bars.set_fill(GREY_B)
            histogram.bars[k].set_fill(GREEN)
            arrow.next_to(histogram.bars[k], UP, SMALL_BUFF)

            new_row = get_checks_and_crosses((n - k) * [False] + k * [True])
            new_row.replace(row)
            row.become(new_row)
            self.wait(0.5)

        # Name it as the Binomial distribution
        long_equation = VGroup(prob_label, eq, formula, eq2, value)
        bin_name = OldTexText("Binomial", " Distribution")
        bin_name.scale(1.5)
        bin_name.next_to(histogram, UP, MED_LARGE_BUFF)

        underline = Underline(bin_name[0])
        underline.set_stroke(PINK, 2)
        nck_rect = SurroundingRectangle(formula[:4])
        nck_rect.set_stroke(PINK, 2)

        self.play(
            long_equation.next_to, self.slots, DOWN, MED_LARGE_BUFF,
            long_equation.to_edge, RIGHT,
            FadeIn(bin_name, DOWN),
        )
        self.wait()
        self.play(ShowCreationThenDestruction(underline))
        self.wait()
        bools = [True] * 50
        bools[random.randint(0, 49)] = False
        bools[random.randint(0, 49)] = False
        row.become(get_checks_and_crosses(bools).replace(row))
        self.play(ShowIncreasingSubsets(row, run_time=4))
        self.wait()

        # Show likelihood and posterior labels
        likelihood_label = OldTex(
            "P(",
            "\\text{data}", "\\,|\\,",
            "\\text{success rate}",
            ")",
        )
        posterior_label = OldTex(
            "P(",
            "\\text{success rate}",
            "\\,|\\,",
            "\\text{data}",
            ")",
        )
        for label in (likelihood_label, posterior_label):
            label.set_color_by_tex_to_color_map({
                "data": GREEN,
                "success": YELLOW,
            })

        likelihood_label.next_to(
            prob_label, DOWN, LARGE_BUFF, aligned_edge=LEFT
        )

        right_arrow = Vector(RIGHT)
        right_arrow.next_to(likelihood_label, RIGHT)
        ra_label = OldTexText("But we want")
        ra_label.match_width(right_arrow)
        ra_label.next_to(right_arrow, UP, SMALL_BUFF)
        posterior_label.next_to(right_arrow, RIGHT)

        self.play(
            FadeIn(likelihood_label, UP),
            bin_name.set_height, 0.4,
            bin_name.set_y, histogram.axes.c2p(0, .25)[1]
        )
        self.wait()
        self.play(
            GrowArrow(right_arrow),
            FadeIn(ra_label, 0.5 * LEFT),
        )
        anims = []
        for i, j in enumerate([0, 3, 2, 1, 4]):
            anims.append(
                TransformFromCopy(
                    likelihood_label[i],
                    posterior_label[j],
                    path_arc=-45 * DEGREES,
                    run_time=2,
                )
            )
        self.play(*anims)
        self.add(posterior_label)
        self.wait()

        # Prepare for new plot
        histogram.add(bin_name)
        always(arrow.next_to, histogram.bars[48], UP, SMALL_BUFF)
        self.play(
            FadeOut(likelihood_label),
            FadeOut(posterior_label),
            FadeOut(right_arrow),
            FadeOut(ra_label),
            FadeOut(row, UP),
            FadeOut(self.slots, UP),
            histogram.scale, 0.7,
            histogram.to_edge, UP,
            arrow.scale, 0.5,
            arrow.set_stroke, None, 4,
            long_equation.center,
            run_time=1.5,
        )
        self.add(arrow)

        # x_labels = histogram.axes.x_labels
        # underline = Underline(x_labels)
        # underline.set_stroke(GREEN, 3)
        # self.play(
        #     LaggedStartMap(
        #         ApplyFunction, x_labels,
        #         lambda mob: (
        #             lambda m: m.scale(1.5).set_color(GREEN),
        #             mob,
        #         ),
        #         rate_func=there_and_back,
        #     ),
        #     ShowCreationThenDestruction(underline),
        # )
        # num_checks = OldTex("\\# " + CMARK_TEX)
        # num_checks.set_color(GREEN)
        # num_checks.next_to(
        #     x_labels, RIGHT,
        #     MED_LARGE_BUFF,
        #     aligned_edge=DOWN,
        # )
        # self.play(Write(num_checks))
        # self.wait()

        low_axes = get_beta_dist_axes(y_max=0.3, y_unit=0.1, label_y=False)
        low_axes.y_axis.set_height(
            2,
            about_point=low_axes.c2p(0, 0),
            stretch=True,
        )
        low_axes.to_edge(DOWN)
        low_axes.x_axis.numbers.set_color(YELLOW)
        y_label_copies = histogram.axes.y_labels.copy()
        y_label_copies.set_height(0.6 * low_axes.get_height())
        y_label_copies.next_to(low_axes, LEFT, 0, aligned_edge=UP)
        y_label_copies.shift(SMALL_BUFF * UP)
        low_axes.y_axis.add(y_label_copies)
        low_axes.y_axis.set_opacity(0)

        # Show alternate values of s
        s_tracker = ValueTracker(self.s)

        s_tip = ArrowTip(start_angle=-90 * DEGREES)
        s_tip.set_color(YELLOW)
        s_tip.axis = low_axes.x_axis
        s_tip.st = s_tracker
        s_tip.add_updater(
            lambda m: m.next_to(m.axis.n2p(m.st.get_value()), UP, buff=0)
        )

        pl_decimal = DecimalNumber(self.s)
        pl_decimal.set_color(YELLOW)
        pl_decimal.replace(prob_label[-2][2:])
        prob_label[-2][2:].set_opacity(0)

        s_label = VGroup(prob_label[-2][:2], pl_decimal).copy()
        sl_rect = SurroundingRectangle(s_label)
        sl_rect.set_stroke(YELLOW, 2)

        self.add(pl_decimal)
        self.play(
            ShowCreation(sl_rect),
            Write(low_axes),
        )
        self.play(
            s_label.next_to, s_tip, UP, 0.2, ORIGIN, s_label[1],
            ReplacementTransform(sl_rect, s_tip)
        )
        always(s_label.next_to, s_tip, UP, 0.2, ORIGIN, s_label[1])

        decimals = VGroup(pl_decimal, s_label[1], formula[5], formula[9])
        decimals.s_tracker = s_tracker

        histogram.s_tracker = s_tracker
        histogram.n = n
        histogram.rhs_value = value

        def update_decimals(decs):
            for dec in decs:
                dec.set_value(decs.s_tracker.get_value())

        def update_histogram(hist):
            new_dist = scipy.stats.binom(hist.n, hist.s_tracker.get_value())
            new_data = np.array([
                new_dist.pmf(x)
                for x in range(0, 51)
            ])
            new_bars = hist.get_bars(new_data)
            new_bars.match_style(hist.bars)
            hist.bars.become(new_bars)
            hist.rhs_value.set_value(new_dist.pmf(48))

        bar_copy = histogram.bars[48].copy()
        # CHANGE: DecimalNumber no longer stores initial_config; num_decimal_places is a direct attribute
        value.num_decimal_places = 3
        value.set_value(value.get_value())
        bar_copy.next_to(value, RIGHT, aligned_edge=DOWN)
        bar_copy.add_updater(
            lambda m: m.set_height(
                max(
                    histogram.bars[48].get_height() * 0.75,
                    1e-6,
                ),
                stretch=True,
                about_edge=DOWN,
            )
        )
        self.add(bar_copy)

        self.add(histogram)
        self.add(decimals)
        for s in [0.95, 0.5, 0.99, 0.9]:
            self.play(
                s_tracker.set_value, s,
                UpdateFromFunc(decimals, update_decimals),
                UpdateFromFunc(histogram, update_histogram),
                UpdateFromFunc(value, lambda m: m),
                UpdateFromFunc(s_label, lambda m: m.update),
                run_time=5,
            )
            self.wait()

        # Plot
        def func(x):
            return scipy.stats.binom(50, x).pmf(48) + 1e-5
        graph = low_axes.get_graph(func, step_size=0.05)
        graph.set_stroke(BLUE, 3)

        v_line = Line(DOWN, UP)
        v_line.axes = low_axes
        v_line.st = s_tracker
        v_line.graph = graph
        v_line.add_updater(
            lambda m: m.put_start_and_end_on(
                m.axes.c2p(m.st.get_value(), 0),
                m.axes.input_to_graph_point(
                    m.st.get_value(),
                    m.graph,
                ),
            )
        )
        v_line.set_stroke(GREEN, 2)
        dot = Dot()
        dot.line = v_line
        dot.set_height(0.05)
        dot.add_updater(lambda m: m.move_to(m.line.get_end()))

        self.play(
            ApplyMethod(
                histogram.bars[48].stretch, 2, 1, {"about_edge": DOWN},
                rate_func=there_and_back,
                run_time=2,
            ),
        )
        self.wait()
        self.play(low_axes.y_axis.set_opacity, 1)
        self.play(
            FadeIn(graph),
            FadeOut(s_label),
            FadeOut(s_tip),
        )
        self.play(
            TransformFromCopy(histogram.bars[48], v_line),
            FadeIn(dot),
        )

        self.add(histogram)
        decimals.remove(decimals[1])
        for s in [0.9, 0.96, 1, 0.8, 0.96]:
            self.play(
                s_tracker.set_value, s,
                UpdateFromFunc(decimals, update_decimals),
                UpdateFromFunc(histogram, update_histogram),
                UpdateFromFunc(value, lambda m: m),
                run_time=5,
            )
            self.wait()

        # Write formula
        clean_form = OldTex(
            "P(", "\\text{data}", "\\,|\\,", "{s}", ")", "=",
            "c", "\\cdot",
            "{s}", "^{\\#" + CMARK_TEX + "}",
            "(1 - ", "{s}", ")", "^{\\#" + XMARK_TEX + "}",
            tex_to_color_map={
                "{s}": YELLOW,
                "\\#" + CMARK_TEX: GREEN,
                "\\#" + XMARK_TEX: RED,
            }
        )
        clean_form.next_to(formula, DOWN, MED_LARGE_BUFF)
        clean_form.save_state()
        clean_form[:6].align_to(equation[1], RIGHT)
        clean_form[6].match_x(formula[2])
        clean_form[7].set_opacity(0)
        clean_form[7].next_to(clean_form[6], RIGHT, SMALL_BUFF)
        clean_form[8:11].match_x(formula[4:8])
        clean_form[11:].match_x(formula[8:])
        clean_form.saved_state.move_to(clean_form, LEFT)

        fade_rects = VGroup(
            BackgroundRectangle(equation[:2]),
            BackgroundRectangle(formula),
            BackgroundRectangle(VGroup(eq2, bar_copy)),
        )
        fade_rects.set_fill(BLACK, 0.8)
        fade_rects[1].set_fill(opacity=0)

        pre_c = formula[:4].copy()
        pre_s = formula[4:8].copy()
        pre_1ms = formula[8:].copy()

        self.play(
            FadeIn(fade_rects),
            FadeIn(clean_form[:6])
        )
        self.play(ShowCreationThenFadeAround(clean_form[3]))
        self.wait()
        for cf, pre in (clean_form[6], pre_c), (clean_form[8:11], pre_s), (clean_form[11:], pre_1ms):
            self.play(
                GrowFromPoint(cf, pre.get_center()),
                pre.move_to, cf,
                pre.scale, 0,
            )
            self.remove(pre)
            self.wait()

        self.wait()
        self.play(Restore(clean_form))

        # Show with 480 and 20
        top_fade_rect = BackgroundRectangle(histogram)
        top_fade_rect.shift(SMALL_BUFF * DOWN)
        top_fade_rect.scale(1.5, about_edge=DOWN)
        top_fade_rect.set_fill(BLACK, 0)

        new_formula = get_binomial_formula(500, 480, 0.96)
        new_formula.move_to(formula)

        def func500(x):
            return scipy.stats.binom(500, x).pmf(480) + 1e-5

        graph500 = low_axes.get_graph(func500, step_size=0.05)
        graph500.set_stroke(TEAL, 3)

        self.play(
            top_fade_rect.set_opacity, 1,
            fade_rects.set_opacity, 1,
            FadeIn(new_formula)
        )

        self.clear()
        self.add(new_formula, clean_form, low_axes, graph, v_line, dot)
        self.add(low_axes.y_axis)

        self.play(TransformFromCopy(graph, graph500))
        self.wait()

        y_axis = low_axes.y_axis
        y_axis.save_state()
        sf = 3
        y_axis.stretch(sf, 1, about_point=low_axes.c2p(0, 0))
        for label in y_label_copies:
            label.stretch(1 / sf, 1)

        v_line.suspend_updating()
        v_line.graph = graph500
        self.play(
            Restore(y_axis, rate_func=reverse_smooth),
            graph.stretch, sf, 1, {"about_edge": DOWN},
            graph500.stretch, sf, 1, {"about_edge": DOWN},
        )
        v_line.resume_updating()
        self.add(v_line, dot)

        sub_decimals = VGroup(new_formula[5], new_formula[9])
        sub_decimals.s_tracker = s_tracker

        for s in [0.94, 0.98, 0.96]:
            self.play(
                s_tracker.set_value, s,
                UpdateFromFunc(sub_decimals, update_decimals),
                run_time=5,
            )
            self.wait()

    def explain_n_choose_k(self, row, formula):
        row.add_updater(lambda m: m)

        brace = Brace(formula[:4], UP, buff=SMALL_BUFF)
        words = brace.get_text("``50 choose 48''")

        slots = self.slots = VGroup()
        for sym in row:
            line = Underline(sym)
            line.scale(0.9)
            slots.add(line)
        for slot in slots:
            slot.match_y(slots[0])

        formula[1].counted = slots
        k_rect = SurroundingRectangle(formula[2])
        k_rect.set_stroke(GREEN, 2)

        checks = VGroup()
        for sym in row:
            if sym.positive:
                checks.add(sym)

        self.play(
            GrowFromCenter(brace),
            FadeInFromDown(words),
        )
        self.wait()
        self.play(FadeOut(words))
        formula.save_state()
        self.play(
            ShowIncreasingSubsets(slots),
            UpdateFromFunc(
                formula[1],
                lambda m: m.set_value(len(m.counted))
            ),
            run_time=2,
        )
        formula.restore()
        self.add(formula)
        self.wait()
        self.play(
            LaggedStartMap(
                ApplyMethod, checks,
                lambda m: (m.shift, 0.3 * DOWN),
                rate_func=there_and_back,
                lag_ratio=0.05,
            ),
            ShowCreationThenFadeOut(k_rect),
            run_time=2,
        )
        self.remove(checks)
        self.add(row)
        self.wait()

        # Example orderings
        row_target = VGroup()
        for sym in row:
            sym.generate_target()
            row_target.add(sym.target)

        row_target.sort(submob_func=lambda m: -int(m.positive))
        row_target.arrange(
            RIGHT, buff=get_norm(row[0].get_right() - row[1].get_left())
        )
        row_target.move_to(row)
        self.play(
            LaggedStartMap(
                MoveToTarget, row,
                path_arc=30 * DEGREES,
                lag_ratio=0,
            ),
        )
        self.wait()
        row.sort()
        self.play(Swap(*row[-3:-1]))
        self.add(row)
        self.wait()

        # All orderings
        nck_count = Integer(2)
        nck_count.next_to(brace, UP)
        nck_top = nck_count.get_top()
        always(nck_count.move_to, nck_top, UP)

        combs = list(it.combinations(range(50), 48))
        bool_lists = [
            [i in comb for i in range(50)]
            for comb in combs
        ]
        row.counter = nck_count
        row.bool_lists = bool_lists

        def update_row(r):
            i = r.counter.get_value() - 1
            new_row = get_checks_and_crosses(r.bool_lists[i])
            new_row.replace(r, dim_to_match=0)
            r.set_submobjects(new_row)

        row.add_updater(update_row)
        self.add(row)
        self.play(
            ChangeDecimalToValue(nck_count, choose(50, 48)),
            run_time=10,
        )
        row.clear_updaters()
        self.wait()
        self.play(
            FadeOut(nck_count),
            FadeOut(brace),
        )


class LikelihoodGraphFor10of10(ShowBinomialFormula):
    CONFIG = {
        "histogram_config": {
            "x_label_freq": 2,
            "y_axis_numbers_to_show": range(25, 125, 25),
            "y_max": 1,
            "y_tick_freq": 0.25,
            "height": 2,
            "bar_colors": [BLUE],
        },
    }

    def construct(self):
        # Add histogram
        dist = scipy.stats.binom(10, self.s)
        data = np.array([
            dist.pmf(x)
            for x in range(0, 11)
        ])
        histogram = self.get_histogram(data)
        histogram.bars.set_fill(GREY_C)
        histogram.bars[10].set_fill(GREEN)
        histogram.to_edge(UP)

        x_label = OldTex("\\#" + CMARK_TEX)
        x_label.set_color(GREEN)
        x_label.next_to(histogram.axes.x_axis.get_end(), RIGHT)
        histogram.add(x_label)
        self.add(histogram)

        arrow = Vector(DOWN)
        arrow.next_to(histogram.bars[10], UP, SMALL_BUFF)
        self.add(arrow)

        # Add formula
        prob_label = get_prob_review_label(10, 0)
        eq = OldTex("=")
        formula = get_binomial_formula(10, 10, self.s)
        eq2 = OldTex("=")
        value = DecimalNumber(dist.pmf(10), num_decimal_places=2)

        equation = VGroup(prob_label, eq, formula, eq2, value)
        equation.arrange(RIGHT)
        equation.next_to(histogram, DOWN, MED_LARGE_BUFF)

        # Add lower axes
        low_axes = get_beta_dist_axes(y_max=1, y_unit=0.25, label_y=False)
        low_axes.y_axis.set_height(
            2,
            about_point=low_axes.c2p(0, 0),
            stretch=True,
        )
        low_axes.to_edge(DOWN)
        low_axes.x_axis.numbers.set_color(YELLOW)
        y_label_copies = histogram.axes.y_labels.copy()
        y_label_copies.set_height(0.7 * low_axes.get_height())
        y_label_copies.next_to(low_axes, LEFT, 0, aligned_edge=UP)
        y_label_copies.shift(SMALL_BUFF * UP)
        low_axes.y_axis.add(y_label_copies)

        # Add lower plot
        s_tracker = ValueTracker(self.s)

        def func(x):
            return x**10
        graph = low_axes.get_graph(func, step_size=0.05)
        graph.set_stroke(BLUE, 3)

        v_line = Line(DOWN, UP)
        v_line.axes = low_axes
        v_line.st = s_tracker
        v_line.graph = graph
        v_line.add_updater(
            lambda m: m.put_start_and_end_on(
                m.axes.c2p(m.st.get_value(), 0),
                m.axes.input_to_graph_point(
                    m.st.get_value(),
                    m.graph,
                ),
            )
        )
        v_line.set_stroke(GREEN, 2)
        dot = Dot()
        dot.line = v_line
        dot.set_height(0.05)
        dot.add_updater(lambda m: m.move_to(m.line.get_end()))

        # Show simpler formula
        brace = Brace(formula, DOWN, buff=SMALL_BUFF)
        simpler_formula = OldTex("s", "^{10}")
        simpler_formula.set_color_by_tex("s", YELLOW)
        simpler_formula.set_color_by_tex("10", GREEN)
        simpler_formula.next_to(brace, DOWN)

        rects = VGroup(
            BackgroundRectangle(formula[:4]),
            BackgroundRectangle(formula[8:]),
        )
        rects.set_opacity(0.75)

        self.wait()
        self.play(FadeIn(equation))

        self.wait()
        self.play(
            FadeIn(rects),
            GrowFromCenter(brace),
            FadeIn(simpler_formula, UP)
        )
        self.wait()

        # Show various values of s
        pl_decimal = DecimalNumber(self.s)
        pl_decimal.set_color(YELLOW)
        pl_decimal.replace(prob_label[-2][2:])
        prob_label[-2][2:].set_opacity(0)

        decimals = VGroup(pl_decimal, formula[5], formula[9])
        decimals.s_tracker = s_tracker

        histogram.s_tracker = s_tracker
        histogram.n = 10
        histogram.rhs_value = value

        def update_decimals(decs):
            for dec in decs:
                dec.set_value(decs.s_tracker.get_value())

        def update_histogram(hist):
            new_dist = scipy.stats.binom(hist.n, hist.s_tracker.get_value())
            new_data = np.array([
                new_dist.pmf(x)
                for x in range(0, 11)
            ])
            new_bars = hist.get_bars(new_data)
            new_bars.match_style(hist.bars)
            hist.bars.become(new_bars)
            hist.rhs_value.set_value(new_dist.pmf(10))

        self.add(histogram)
        self.add(decimals, rects)
        self.play(
            FadeIn(low_axes),
        )
        self.play(
            ShowCreation(v_line),
            FadeIn(dot),
        )
        self.add(graph, v_line, dot)
        self.play(ShowCreation(graph))
        self.wait()

        always(arrow.next_to, histogram.bars[10], UP, SMALL_BUFF)
        for s in [0.8, 1]:
            self.play(
                s_tracker.set_value, s,
                UpdateFromFunc(decimals, update_decimals),
                UpdateFromFunc(histogram, update_histogram),
                UpdateFromFunc(value, lambda m: m),
                run_time=5,
            )
            self.wait()
