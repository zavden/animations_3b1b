# ==============================================================================
# Scene:      TwoValuesEvenlySpaceAroundZero
# Source:     videos/_2021/quick_eigen.py (lines 2389-2427)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoValuesEvenlySpaceAroundZero.py TwoValuesEvenlySpaceAroundZero -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


class TwoValuesEvenlySpaceAroundZero(Scene):
    def construct(self):
        nl = NumberLine((-2, 2, 0.25), width=6)
        nl.add_numbers(np.arange(-2, 3, 1.0), num_decimal_places=1, font_size=24)
        d_tracker = ValueTracker(2)
        get_d = d_tracker.get_value
        dots = VGroup(*(Dot() for x in range(2)))
        labels = VGroup(OldTex("\\lambda_1"), OldTex("\\lambda_2"))
        for group in dots, labels:
            group.set_submobject_colors_by_gradient(*EIGEN_COLORS)

        def update_dots(dots):
            dots[0].move_to(nl.n2p(-get_d()))
            dots[1].move_to(nl.n2p(get_d()))

        def update_labels(labels):
            for label, dot in zip(labels, dots):
                label.match_color(dot)
                label.next_to(dot, UP, SMALL_BUFF)

        dots.add_updater(update_dots)
        labels.add_updater(update_labels)

        prod_label = VGroup(
            labels.copy().clear_updaters().arrange(RIGHT, buff=SMALL_BUFF),
            OldTex("="),
            DecimalNumber(-4),
        )
        prod_label[-1].match_height(prod_label[0])
        prod_label.arrange(RIGHT)
        prod_label.next_to(labels, UP, LARGE_BUFF)
        prod_label[-1].add_updater(lambda m: m.set_value(-get_d()**2))

        self.add(nl, dots, labels, prod_label)

        self.play(d_tracker.animate.set_value(0.5), run_time=3)
        self.play(d_tracker.animate.set_value(1.5), run_time=3)
        self.play(d_tracker.animate.set_value(1.0), run_time=2)
        self.wait()
