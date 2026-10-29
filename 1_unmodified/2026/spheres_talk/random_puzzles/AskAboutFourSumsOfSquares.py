# ==============================================================================
# Scene:      AskAboutFourSumsOfSquares
# Source:     videos/_2026/spheres_talk/random_puzzles.py (lines 406-408)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutFourSumsOfSquares.py AskAboutFourSumsOfSquares -w -m --fps 15
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


class AskAboutThreeSumsOfSquares(RandomSumsOfSquares):
    label_texs = "xyz"
    square_sum_tex = "x^2 + y^2 + z^2"

    def construct(self):
        intervals = self.get_labeled_intervals(self.label_texs, buff=LARGE_BUFF)
        intervals.to_edge(LEFT)
        question = self.get_probability_question(self.square_sum_tex)
        question.to_corner(UR)
        evaluation = self.get_evaluation_object(intervals)
        evaluation.set_width(6.5)
        evaluation.next_to(question, DOWN, LARGE_BUFF)
        evaluation.to_edge(RIGHT)

        self.add(intervals)
        self.add(question)
        self.add(evaluation)

        self.play(self.randomize_intervals(intervals, frequency=0.2, run_time=30))


class AskAboutFourSumsOfSquares(AskAboutThreeSumsOfSquares):
    label_texs = "xyzw"
    square_sum_tex = "x^2 + y^2 + z^2 + w^2"
