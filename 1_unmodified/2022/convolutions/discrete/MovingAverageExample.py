# ==============================================================================
# Scene:      MovingAverageExample
# Source:     videos/_2022/convolutions/discrete.py (lines 1092-1187)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MovingAverageExample.py MovingAverageExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

def get_aligned_pairs(group1, group2, n):
    return VGroup(*(
        VGroup(m1, m2)
        for m1 in group1
        for m2 in group2
        if m1.index + m2.index == n
    ))


def get_row_shift(top_row, low_row, n):
    min_index = low_row[0].index
    max_index = top_row[-1].index
    max_sum = min_index + max_index
    if n <= max_sum:
        x_shift = top_row[n - 2 * min_index].get_x() - low_row[0].get_x()
    else:
        x_shift = top_row[-1].get_x() - low_row[n - max_sum].get_x()
    return low_row.animate.shift(x_shift * RIGHT)


def dist_to_bars(dist, bar_width=0.5, height=2.0, bar_colors=(BLUE_D, GREEN_D)):
    bars = Rectangle(width=bar_width).get_grid(1, len(dist), buff=0)
    bars.set_color_by_gradient(*bar_colors)
    bars.set_fill(opacity=1)
    bars.set_stroke(WHITE, 1)
    for bar, value, index in zip(bars, dist, it.count()):
        bar.set_height(value, stretch=True, about_edge=DOWN)
        bar.index = index
    bars.set_height(height, stretch=True)
    bars.center()
    return bars


def get_bar_dividing_lines(bars):
    v_lines = VGroup()
    for bar in bars:
        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(GREY_C, 1, 0.75)
        v_line.set_x(bar.get_left()[0])
        v_line.set_y(0)
        v_lines.add(v_line)
    v_lines.add(v_lines[-1].copy().set_x(bars.get_right()[0]))
    return v_lines


def add_labels_to_bars(bars, dist, width_ratio=0.7, **number_config):
    labels = VGroup(*(DecimalNumber(x, **number_config) for x in dist))
    labels.set_max_width(width_ratio * bars[0].get_width())
    for label, bar in zip(labels, bars):
        label.next_to(bar, UP, SMALL_BUFF)
        bar.value_label = label
        bar.push_self_into_submobjects()
        bar.add(label)
    return bars


class MovingAverageExample(InteractiveScene):
    dist1 = [*5 * [0.1], *5 * [1], *5 * [0.1], *5 * [1], *5 * [0.1]]
    dist2 = 5 * [0.2]
    march_anim_run_time = 1.0
    always_preview_result = True

    def construct(self):
        # All bars
        self.camera.frame.scale(1.01)
        dist1 = np.array(self.dist1)
        dist2 = np.array(self.dist2)
        conv_dist = np.convolve(dist1, dist2)

        top_bars = dist_to_bars(dist1, height=1.5, bar_colors=(BLUE_D, TEAL_D))
        low_bars = dist_to_bars(dist2, height=1.5, bar_colors=(RED_D, GOLD_E))
        conv_bars = dist_to_bars(conv_dist, height=1.5, bar_colors=(GREEN_D, YELLOW_E))

        top_bars.center().to_edge(UP)
        low_bars.stretch(max(dist2), 1, about_edge=DOWN)
        low_bars.arrange(LEFT, aligned_edge=DOWN, buff=0)
        low_bars.next_to(top_bars, DOWN, buff=1.2, aligned_edge=LEFT)
        conv_bars.match_x(top_bars)
        conv_bars.to_edge(DOWN, LARGE_BUFF)
        v_lines = get_bar_dividing_lines(conv_bars)

        add_labels_to_bars(top_bars, dist1, num_decimal_places=1, width_ratio=0.4)
        add_labels_to_bars(low_bars, dist2, num_decimal_places=1, width_ratio=0.4)
        add_labels_to_bars(conv_bars, conv_dist, num_decimal_places=2)

        self.add(v_lines)
        self.play(FadeIn(top_bars, lag_ratio=0.1, run_time=2))
        self.play(FadeIn(low_bars))

        lb_rect = SurroundingRectangle(low_bars)
        lb_rect.round_corners().set_stroke(YELLOW, 2)
        sum_label = Tex(R"\sum_i y_i = 1")
        sum_label.set_color(YELLOW)
        sum_label.next_to(lb_rect)
        self.play(ShowCreation(lb_rect))
        self.play(Write(sum_label, run_time=1))
        self.wait()
        self.play(FadeOut(lb_rect), FadeOut(sum_label))

        # March!
        last_rects = VGroup()
        for n, conv_bar in enumerate(conv_bars):
            rect = conv_bar[0]
            value = conv_bar[1]

            rect.save_state()
            rect.stretch(0, 1, about_edge=DOWN)
            rect.set_opacity(0)

            self.play(
                get_row_shift(top_bars, low_bars, n),
                FadeOut(last_rects),
                run_time=self.march_anim_run_time,
            )

            pairs = get_aligned_pairs(top_bars, low_bars, n)
            label_pairs = VGroup(*(VGroup(m1.value_label, m2.value_label) for m1, m2 in pairs))
            rects = VGroup(*(
                SurroundingRectangle(lp, buff=0.05).set_stroke(YELLOW, 2).round_corners()
                for lp in label_pairs
            ))
            rects.set_stroke(YELLOW, 2)

            self.play(
                FadeIn(rects, lag_ratio=0.5),
                conv_bars[:n].animate.set_opacity(0.5),
                run_time=self.march_anim_run_time,
            )

            self.play(
                *(
                    FadeTransform(label.copy(), value)
                    for lp in label_pairs
                    for label in lp
                ),
                Restore(rect),
                run_time=self.march_anim_run_time,
            )

            if self.always_preview_result:
                self.add(conv_bars)
                conv_bars.set_opacity(0.5)
                conv_bar.set_opacity(1)

            self.wait(0.5)

            last_rects = rects

        self.play(
            FadeOut(last_rects),
            conv_bars.animate.set_opacity(1),
        )
