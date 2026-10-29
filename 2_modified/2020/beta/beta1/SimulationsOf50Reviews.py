# ==============================================================================
# Scene:      SimulationsOf50Reviews
# Source:     videos/_2020/beta/beta1.py (lines 2511-2632)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl SimulationsOf50Reviews.py SimulationsOf50Reviews -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - SIRGraph/Histogram's `self.data` clashes with manimgl's Mobject.data (it was a list); renamed to graph_data / hist_data
# ==============================================================================

from manim_imports_ext import *


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
