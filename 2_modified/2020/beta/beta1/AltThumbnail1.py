# ==============================================================================
# Scene:      AltThumbnail1
# Source:     videos/_2020/beta/beta1.py (lines 41-68)
# Category:   2 · Renders with modifications
# Includes code copied from: _2020/beta/helpers.py
#
# Run from this folder:
#     manimgl AltThumbnail1.py AltThumbnail1 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - SIRGraph/Histogram's `self.data` clashes with manimgl's Mobject.data (it was a list); renamed to graph_data / hist_data
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/beta/helpers.py -----

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



# ----- From _2020/beta/beta1.py -----

class AltThumbnail1(Scene):
    def construct(self):
        N = 20
        n_trials = 10000
        p = 0.7
        outcomes = (np.random.random((N, n_trials)) < p).sum(0)
        counts = []
        for k in range(N + 1):
            counts.append((outcomes == k).sum())

        hist = Histogram(
            counts,
            y_max=0.3,
            y_tick_freq=0.05,
            y_axis_numbers_to_show=[10, 20, 30],
            x_label_freq=10,
        )
        hist.set_width(FRAME_WIDTH - 1)
        hist.bars.set_submobject_colors_by_gradient(YELLOW, YELLOW, GREEN, BLUE)
        hist.bars.set_stroke(WHITE, 2)

        title = OldTexText("Binomial distribution")
        title.set_width(12)
        title.to_corner(UR, buff=0.8)
        title.add_background_rectangle()

        self.add(hist)
        self.add(title)
