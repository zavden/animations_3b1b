# ==============================================================================
# Scene:      DistanceBetweenDistributions
# Source:     videos/_2026/cross_entropy/robot.py (lines 8631-8717)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/cross_entropy/distribution.py
#
# Run from this folder:
#     manimgl DistanceBetweenDistributions.py DistanceBetweenDistributions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *


# ----- From _2026/cross_entropy/distribution.py -----

class StackedProbDistribution(VGroup):
    def __init__(
        self,
        distribution,
        width=12,
        height=0.5,
        fill_colors=(BLUE_E, TEAL_E),
        fill_opacity=1,
        stroke_width=1,
        stroke_color=WHITE,
        labels=None,
        label_height_ratio=0.5,
        label_width_ratio=0.8,
        fit_labels_to_height=True,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.distribution = distribution
        self.cdf = np.cumsum(distribution)
        self.bar_color_bounds = fill_colors
        self.label_height_ratio = label_height_ratio
        self.label_width_ratio = label_width_ratio

        # Set bars with dummy values
        self.bars = Rectangle().get_grid(1, len(distribution), buff=0)
        self.bars.set_shape(width, height)
        self.bars.set_fill(fill_colors, 1, gradient_direction=RIGHT)
        self.bars.set_stroke(stroke_color, stroke_width)

        # Initialize labels as empty
        self.labels = VGroup()

        self.add(self.bars, self.labels)

        self.set_distribution(distribution)
        self.fit_labels_to_height = fit_labels_to_height
        if labels is not None:
            self.set_labels(labels)

    def set_labels(self, labels: VMobject):
        self.labels.set_submobjects(labels)
        self.original_labels = labels.copy()
        self.reposition_labels()
        return self

    def reposition_labels(self):
        self.labels.become(self.original_labels)
        if self.fit_labels_to_height:
            self.labels.set_height(self.bars.get_height() * self.label_height_ratio)
        self.labels.move_to(self.bars)
        for label, bar in zip(self.labels, self.bars):
            label.match_x(bar)
            fill_opacity = float(label.get_width() < bar.get_width() * self.label_width_ratio)
            label.set_fill(opacity=fill_opacity)
        return self

    def set_distribution(self, distribution):
        center = self.bars.get_center().copy()
        width, height = self.bars.get_shape()[:2]
        n_bars = len(distribution)
        bar_style = self.bars[0].get_style()

        if len(self.bars) != n_bars:
            self.bars.set_submobjects(Rectangle().replicate(n_bars))

        for bar, prob in zip(self.bars, distribution):
            bar.set_shape(width * prob, height)
            bar.set_style(**bar_style)
        self.bars.arrange(RIGHT, buff=0)
        self.bars.move_to(center)
        self.bars.set_fill(self.bar_color_bounds, gradient_direction=RIGHT)

        if len(self.labels) > 0:
            self.reposition_labels()

        return self

    def highlight(self, index, color=None, other_bar_opacity=0.35, fade_labels=True):
        self.bars.set_fill(self.bar_color_bounds, opacity=other_bar_opacity, gradient_direction=RIGHT)
        self.bars[index].set_fill(color, opacity=1)
        if fade_labels:
            for idx, label in enumerate(self.labels):
                if label.get_fill_opacity() == 0:
                    op = 0
                elif idx == index:
                    op = 1
                else:
                    op = other_bar_opacity
                label.set_fill(opacity=op)
        return self

    def renormalize_around(self, index: int):
        width, height = self.get_shape()[:2]
        center = self.get_center().copy()
        bar_width = self.bars[index].get_width()
        self.bars.stretch(width / bar_width, 0)
        self.bars.shift(center - self.bars[index].get_center())
        self.reposition_labels()
        return self

    def stretch(self, factor, dim, **kwargs):
        super().stretch(factor, dim, **kwargs)
        if dim == 0:
            self.reposition_labels()
        return self

    def float_to_index(self, value: float):
        """
        Given a value in [0, 1], returns the index of the
        corresponding event from the distribution
        """
        for idx, upper_value in enumerate(self.cdf):
            if value < upper_value:
                return idx
        # Otherwise, last element
        return len(self.distribution) - 1



# ----- From _2026/cross_entropy/robot.py -----

PURE_MAGENTA = "#FF00FF"


def random_distribution(n, thresh=1 / 16):
    if n <= 0:
        return []
    if n * thresh > 1:
        raise ValueError("Threshold is too high to sum to 1")
    remaining_sum = 1 - (n * thresh)
    random_parts = np.random.dirichlet(np.ones(n), size=1).flatten()
    numbers = (random_parts * remaining_sum) + thresh
    return numbers.tolist()


class DistanceBetweenDistributions(InteractiveScene):
    def construct(self):
        # Add the two distributions
        distribution1 = random_distribution(7)
        distribution2 = random_distribution(7)
        Q = StackedProbDistribution(
            distribution1,
            labels=None,
            width=8,
            height=0.4,
            fill_colors=(LIGHT_PINK, PURE_MAGENTA),
            stroke_width=3
        ).to_edge(LEFT, buff=1.5).shift(DOWN * 1.2)
        probability_labels_1 = VGroup(*[
            Tex(
                (("q_" + str(i + 1)) if i < len(Q.bars) - 2 else R"\ldots" if i == len(Q.bars) - 2 else "q_n"),
                font_size=35
            ).set_color(interpolate_color(LIGHT_PINK, PURE_MAGENTA, i // (len(Q.bars) - 1))).set_stroke(width=15, color=BLACK, behind=True)
            for i in range(len(Q.bars))
        ])
        for label, segment in zip(probability_labels_1, Q.bars):
            label.add_updater(lambda m, segment=segment: m.next_to(segment, DOWN))

        P = StackedProbDistribution(
            distribution2,
            labels=None,
            width=8,
            height=0.4,
            fill_colors=(GREEN_B, GREEN_D),
            stroke_width=3
        ).to_edge(LEFT, buff=1.5).shift(UP * 1.2)
        probability_labels_2 = VGroup(*[
            Tex(
                (("p_" + str(i + 1)) if i < len(P.bars) - 2 else R"\ldots" if i == len(Q.bars) - 2 else "p_n"),
                font_size=35
            ).set_color(interpolate_color(GREEN_B, GREEN_D, i // (len(Q.bars) - 1))).set_stroke(width=15, color=BLACK, behind=True)
            for i in range(len(P.bars))
        ])
        for label, segment in zip(probability_labels_2, P.bars):
            label.add_updater(lambda m, segment=segment: m.next_to(segment, DOWN))

        self.add(Q, probability_labels_1, P, probability_labels_2)

        # Add Q and P symbols
        def get_kl_divergence(Q, P):
            Q_total_width = Q.get_width()
            Q_current_distribution = [bar.get_width() / Q_total_width for bar in Q.bars]
            P_total_width = P.get_width()
            P_current_distribution = [bar.get_width() / P_total_width for bar in P.bars]
            return sum([p * math.log2(p / q) for q, p in zip(Q_current_distribution, P_current_distribution)])
        Q_symbol = Tex("Q", font_size=60).set_color(PINK).set_stroke(width=15, color=BLACK, behind=True)
        P_symbol = Tex("P", font_size=60).set_color(GREEN).set_stroke(width=15, color=BLACK, behind=True)
        VGroup(Q_symbol, P_symbol).to_edge(RIGHT, buff=2)
        multiplier = 20
        Q_symbol.add_updater(lambda m: m.set_y(-multiplier * get_kl_divergence(Q, P)))
        P_symbol.add_updater(lambda m: m.set_y(multiplier * get_kl_divergence(Q, P)))
        self.add(Q_symbol, P_symbol)

        # Add the connecting line
        connecting_line = always_redraw(
            lambda:
            Line(
                Q_symbol,
                P_symbol,
                stroke_width=clip(1 / (3 * get_kl_divergence(Q, P)), 0.2, 9),
                stroke_color=BLUE_B,
                stroke_opacity=0.5
            )
        )
        self.add(connecting_line)
        connecting_line.add_updater(lambda m: self.bring_to_back(m))

        # Add Dashed lines
        dashed_lines = VGroup(*[
            DashedLine(Q.bars.get_bottom(), P.bars.get_top(), stroke_width=3)
            for _ in range(len(P.bars) + 1)
        ]).set_color(GREY).set_opacity(0.5).align_to(Q.bars, DOWN)
        for line, bar in zip(dashed_lines, P.bars):
            line.set_x(bar.get_left()[0])
        dashed_lines[-1].set_x(P.bars[-1].get_right()[0])
        self.add(dashed_lines)
        self.bring_to_back(dashed_lines)

        # Change Q to be closer / further away from P
        for i in range(15):
            self.play(Q.animate.set_distribution(random_distribution(7, thresh=1 / 10) if i != 3 else distribution2), run_time=1.5)
            self.wait(0.5)
