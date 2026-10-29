# ==============================================================================
# Scene:      AskAboutLargeSumOfSquares
# Source:     videos/_2026/spheres_talk/random_puzzles.py (lines 411-447)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutLargeSumOfSquares.py AskAboutLargeSumOfSquares -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntervalWithSample(Group):
    def __init__(
        self,
        width=4,
        numbers_font_size=36,
        x_range=(-1, 1, 0.25),
        label_step=0.5,
        marker_length=0.25,
        marker_width=(0, 15),
        marker_color=BLUE_B,
        dec_label_font_size=30,
    ):
        self.number_line = NumberLine(x_range, width=width)
        self.number_line.add_numbers(
            (-1, 0, 1),
            font_size=numbers_font_size,
            num_decimal_places=0
        )
        self.x_tracker = ValueTracker()
        get_x = self.x_tracker.get_value

        self.marker = Line(ORIGIN, marker_length * UP)
        self.marker.set_stroke(marker_color, width=marker_width, flat=True)
        self.marker.add_updater(lambda m: m.put_start_on(self.number_line.n2p(get_x())))

        self.dec_label = DecimalNumber(font_size=dec_label_font_size)
        self.dec_label.add_updater(lambda m: m.set_value(get_x()))
        self.dec_label.add_updater(
            lambda m: m.next_to(self.marker.get_end(), normalize(self.marker.get_vector()), SMALL_BUFF)
        )

        super().__init__(
            self.x_tracker,
            self.number_line,
            self.marker,
            self.dec_label
        )


class RandomSumsOfSquares(InteractiveScene):
    tex_to_color = {"x": BLUE, "y": YELLOW, "z": RED, "w": PINK}

    def get_intervals(self, n_intervals, buff=MED_LARGE_BUFF, **kwargs):
        result = Group(IntervalWithSample(**kwargs) for n in range(n_intervals))
        result.arrange(DOWN, buff=buff)
        return result

    def get_labeled_intervals(self, label_texs, font_size=48, buff=MED_LARGE_BUFF):
        intervals = self.get_intervals(len(label_texs), buff=buff)
        labels = VGroup(
            Tex(tex, font_size=font_size, t2c=self.tex_to_color)
            for tex in label_texs
        )
        for label, interval in zip(labels, intervals):
            label.next_to(interval.number_line.get_start(), LEFT, MED_LARGE_BUFF)
            interval.label = label
            interval.add(label)
        return intervals

    def get_probability_question(self, sum_tex="x^2 + y^2"):
        question = Tex(Rf"P\left({sum_tex} \le 1 \right)", t2c=self.tex_to_color)
        question.to_corner(UR, buff=LARGE_BUFF)
        return question

    def get_evaluation_object(self, intervals):
        equation = Tex(" + ".join(["(+0.00)^2"] * len(intervals)) + "= 1.00")
        x_terms = equation.make_number_changeable("+0.00", replace_all=True, include_sign=True)
        for x_term, interval in zip(x_terms, intervals):
            if hasattr(interval, "label"):
                x_term.match_color(interval.label[0])
            x_term.f_always.set_value(interval.x_tracker.get_value)
        rhs = equation.make_number_changeable("1.00")
        rhs.add_updater(lambda m: m.set_value(sum([
            interval.x_tracker.get_value()**2
            for interval in intervals
        ])))

        marks = VGroup(
            Checkmark().set_color(GREEN),
            Exmark().set_color(RED),
        )
        marks.set_width(0.75 * rhs.get_width())
        marks[0].add_updater(lambda m: m.set_opacity(float(rhs.get_value() <= 1)))
        marks[1].add_updater(lambda m: m.set_opacity(float(rhs.get_value() > 1)))
        marks.next_to(rhs, DOWN)
        equation.add(marks)

        return equation

    def set_interval_values_randomly(self, intervals):
        for interval in intervals:
            value = random.uniform(*interval.number_line.x_range[:2])
            interval.x_tracker.set_value(value)

    def randomize_intervals(self, intervals, run_time=3, frequency=0.1):
        intervals.value_at_last_change = -1

        def update_intervals(intervals, alpha):
            curr_value = int(alpha * run_time / frequency)
            if curr_value != intervals.value_at_last_change:
                self.set_interval_values_randomly(intervals)
                intervals.value_at_last_change = curr_value

        return UpdateFromAlphaFunc(intervals, update_intervals, rate_func=linear, run_time=run_time)


class AskAboutLargeSumOfSquares(RandomSumsOfSquares):
    def construct(self):
        # Test
        intervals = self.get_intervals(
            8,
            width=6,
            numbers_font_size=24,
            dec_label_font_size=24,
            marker_length=0.15
        )
        intervals.set_height(7)
        intervals.to_edge(LEFT, buff=LARGE_BUFF)
        to_remove = intervals[-3:-1]
        dots = Tex(R"\vdots", font_size=90)
        dots.move_to(to_remove)
        intervals.remove(*to_remove)

        labels = VGroup(
            Tex(Rf"x_{{{int(n)}}}", font_size=36)
            for n in [*range(1, 6), 100]
        )
        labels.set_submobject_colors_by_gradient(BLUE, YELLOW)
        for label, interval in zip(labels, intervals):
            label.next_to(interval.number_line.get_start(), LEFT, MED_SMALL_BUFF)

        question = Tex(
            R"P\left(x_1^2 + x_2^2 + \cdots + x_{100}^2 \le 1 \right)",
            t2c={"x_1": labels[0].get_color(), "x_2": labels[1].get_color(), "x_{100}": labels[-1].get_color()}
        )
        question.to_corner(UR)

        self.add(intervals)
        self.add(labels)
        self.add(dots)
        self.add(question)

        self.play(self.randomize_intervals(intervals, run_time=20, frequency=0.2))
