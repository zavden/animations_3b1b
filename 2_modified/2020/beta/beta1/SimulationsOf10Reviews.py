# ==============================================================================
# Scene:      SimulationsOf10Reviews
# Source:     videos/_2020/beta/beta1.py (lines 2345-2496)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl SimulationsOf10Reviews.py SimulationsOf10Reviews -w -m --fps 15
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


def get_random_num_row(s, n=10):
    values = np.random.random(n)
    nums = VGroup()
    syms = VGroup()
    for x, value in enumerate(values):
        num = DecimalNumber(value)
        num.set_height(0.25)
        num.move_to(x * RIGHT)
        num.positive = (num.get_value() < s)
        if num.positive:
            num.set_color(GREEN)
            sym = OldTex(CMARK_TEX)
        else:
            num.set_color(RED)
            sym = OldTex(XMARK_TEX)
        sym.match_color(num)
        sym.match_height(num)
        sym.positive = num.positive
        sym.next_to(num, UP)

        nums.add(num)
        syms.add(sym)

    row = VGroup(nums, syms)
    row.nums = nums
    row.syms = syms
    row.n_positive = sum([m.positive for m in nums])

    row.set_width(10)
    row.center().to_edge(UP)
    return row



# ----- From _2020/beta/beta1.py -----

class SimulationsOf10Reviews(Scene):
    CONFIG = {
        "s": 0.95,
        "histogram_height": 5,
        "histogram_width": 10,
    }

    def construct(self):
        # Add s label
        s_label = OldTex("s = 0.95")
        s_label.set_height(0.3)
        s_label.to_corner(UL, buff=MED_SMALL_BUFF)
        s_label.set_color(YELLOW)
        self.add(s_label)
        self.camera.frame.shift(LEFT)
        s_label.shift(LEFT)

        # Add random row
        np.random.seed(0)
        row = get_random_num_row(self.s)
        count = self.get_count(row)
        count.add_updater(
            lambda m: m.set_value(
                sum([s.positive for s in row.syms])
            )
        )

        def update_nums(nums):
            for num in nums:
                num.set_value(np.random.random())

        row.nums.save_state()
        row.nums.set_color(WHITE)
        self.play(
            UpdateFromFunc(row.nums, update_nums),
            run_time=2,
        )
        row.nums.restore()
        self.wait()

        self.add(count)
        self.play(
            ShowIncreasingSubsets(row.syms),
            run_time=2,
            rate_func=linear,
        )
        count.clear_updaters()
        self.wait()

        # Histogram
        data = np.zeros(11)
        histogram = self.get_histogram(data)

        stacks = VGroup()
        for bar in histogram.bars:
            stacks.add(VGroup(bar.copy()))

        def put_into_histogram(row_count_group):
            row, count = row_count_group
            count.clear_updaters()
            index = int(count.get_value())
            stack = stacks[index]

            row.set_width(stack.get_width() - SMALL_BUFF)
            row.next_to(stack, UP, SMALL_BUFF)
            count.replace(histogram.axes.x_labels[index])
            stack.add(row)
            return row_count_group

        # Random samples in histogram
        self.play(
            FadeIn(histogram),
            ApplyFunction(
                put_into_histogram,
                VGroup(row, count),
            )
        )
        self.wait()
        for x in range(2):
            row = get_random_num_row(self.s)
            count = self.get_count(row)
            group = VGroup(row, count)
            self.play(FadeIn(group, lag_ratio=0.2))
            self.wait(0.5)
            self.play(
                ApplyFunction(
                    put_into_histogram,
                    VGroup(row, count),
                )
            )

        # More!
        for x in range(40):
            row = get_random_num_row(self.s)
            count = self.get_count(row)
            lower_group = VGroup(row, count).copy()
            put_into_histogram(lower_group)
            self.add(row, count, lower_group)
            self.wait(0.1)
            self.remove(row, count)

        data = np.array([len(stack) - 1 for stack in stacks])
        self.add(row, count)
        self.play(
            FadeOut(stacks),
            FadeOut(count),
            histogram.bars.become, histogram.get_bars(data),
            histogram.axes.y_labels.set_opacity, 1,
            histogram.axes.h_lines.set_opacity, 1,
            histogram.axes.y_axis.set_opacity, 1,
        )
        self.remove(stacks)

        arrow = Vector(0.5 * DOWN)
        arrow.set_stroke(width=5)
        arrow.set_color(YELLOW)
        arrow.next_to(histogram.bars[10], UP, SMALL_BUFF)

        def update(dummy):
            new_row = get_random_num_row(self.s)
            row.become(new_row)
            count = sum([m.positive for m in new_row.nums])
            data[count] += 1
            histogram.bars.become(histogram.get_bars(data))
            arrow.next_to(histogram.bars[count], UP, SMALL_BUFF)

        self.add(arrow)
        self.play(
            UpdateFromFunc(Group(row, arrow, histogram.bars), update),
            run_time=10,
        )

    #
    def get_histogram(self, data):
        histogram = Histogram(
            data,
            bar_colors=[RED, RED, BLUE, GREEN],
            height=self.histogram_height,
            width=self.histogram_width,
        )
        histogram.to_edge(DOWN)

        histogram.axes.y_labels.set_opacity(0)
        histogram.axes.h_lines.set_opacity(0)
        return histogram

    def get_count(self, row):
        count = Integer()
        count.set_height(0.75)
        count.next_to(row, DOWN, buff=0.65)
        count.set_value(sum([s.positive for s in row.syms]))
        return count
