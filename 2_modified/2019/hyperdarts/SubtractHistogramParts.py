# ==============================================================================
# Scene:      SubtractHistogramParts
# Source:     videos/_2019/hyperdarts.py (lines 1785-1867)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SubtractHistogramParts.py SubtractHistogramParts -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Remove layer [0] of Brace: GL exposes the strokes of the brace directly.
# ==============================================================================

from manim_imports_ext import *

class ShowDistributionOfScores(Scene):
    CONFIG = {
        "axes_config": {
            "x_min": -1,
            "x_max": 10,
            "x_axis_config": {
                "unit_size": 1.2,
                "tick_frequency": 1,
            },
            "y_min": 0,
            "y_max": 100,
            "y_axis_config": {
                "unit_size": 0.065,
                "tick_frequency": 10,
                "include_tip": False,
            },
        },
        "random_seed": 1,
    }

    def construct(self):
        # Add axes
        axes = self.get_axes()
        self.add(axes)

        # setup scores
        n_scores = 10000
        scores = np.array([self.get_random_score() for x in range(n_scores)])
        index_tracker = ValueTracker(n_scores)

        def get_index():
            value = np.clip(index_tracker.get_value(), 0, n_scores - 1)
            return int(value)

        # Setup histogram
        bars = self.get_histogram_bars(axes)
        bars.add_updater(
            lambda b: self.set_histogram_bars(
                b, scores[:get_index()], axes
            )
        )
        self.add(bars)

        # Add score label
        score_label = VGroup(
            OldTexText("Last score: "),
            Integer(1)
        )
        score_label.scale(1.5)
        score_label.arrange(RIGHT)
        score_label[1].align_to(score_label[0][0][-1], DOWN)

        score_label[1].add_updater(
            lambda m: m.set_value(scores[get_index() - 1])
        )
        score_label[1].add_updater(
            lambda m: m.set_fill(bars[scores[get_index() - 1]].get_fill_color())
        )

        n_trials_label = VGroup(
            OldTexText("\\# Games: "),
            Integer(0),
        )
        n_trials_label.scale(1.5)
        n_trials_label.arrange(RIGHT, aligned_edge=UP)
        n_trials_label[1].add_updater(
            lambda m: m.set_value(get_index())
        )

        n_trials_label.to_corner(UR, buff=LARGE_BUFF)
        score_label.next_to(
            n_trials_label, DOWN,
            buff=LARGE_BUFF,
            aligned_edge=LEFT,
        )

        self.add(score_label)
        self.add(n_trials_label)

        # Add curr_score_arrow
        curr_score_arrow = Arrow(0.25 * UP, ORIGIN, buff=0)
        curr_score_arrow.set_stroke(WHITE, 5)
        curr_score_arrow.add_updater(
            lambda m: m.next_to(bars[scores[get_index() - 1] - 1], UP, SMALL_BUFF)
        )
        self.add(curr_score_arrow)

        # Add mean bar
        mean_line = DashedLine(ORIGIN, 4 * UP)
        mean_line.set_stroke(YELLOW, 2)

        def get_mean():
            return np.mean(scores[:get_index()])

        mean_line.add_updater(
            lambda m: m.move_to(axes.c2p(get_mean(), 0), DOWN)
        )
        mean_label = VGroup(
            OldTexText("Mean = "),
            DecimalNumber(num_decimal_places=3),
        )
        mean_label.arrange(RIGHT)
        mean_label.match_color(mean_line)
        mean_label.add_updater(lambda m: m.next_to(mean_line, UP, SMALL_BUFF))
        mean_label[1].add_updater(lambda m: m.set_value(get_mean()))

        # Show many runs
        index_tracker.set_value(1)
        for value in [10, 100, 1000, 10000]:
            anims = [
                ApplyMethod(
                    index_tracker.set_value, value,
                    rate_func=linear,
                    run_time=5,
                ),
            ]
            if value == 10:
                anims.append(
                    FadeIn(
                        VGroup(mean_line, mean_label),
                        rate_func=squish_rate_func(smooth, 0.5, 1),
                        run_time=2,
                    ),
                )
            self.play(*anims)
        self.wait()

    #
    def get_axes(self):
        axes = Axes(**self.axes_config)
        axes.to_corner(DL)

        axes.x_axis.add_numbers(*range(1, 12))
        axes.y_axis.add_numbers(
            *range(20, 120, 20),
            unit="\\%"
        )
        x_label = OldTexText("Score")
        x_label.next_to(axes.x_axis.get_right(), UR, buff=0.5)
        x_label.shift_onto_screen()
        axes.x_axis.add(x_label)

        y_label = OldTexText("Relative proportion")
        y_label.next_to(axes.y_axis.get_top(), RIGHT, buff=0.75)
        y_label.to_edge(UP, buff=MED_SMALL_BUFF)
        axes.y_axis.add(y_label)

        return axes

    def get_histogram_bars(self, axes):
        bars = VGroup()
        for x in range(1, 10):
            bar = Rectangle(width=axes.x_axis.unit_size)
            bar.move_to(axes.c2p(x, 0), DOWN)
            bar.x = x
            bars.add(bar)
        bars.set_fill(opacity=0.7)
        bars.set_color_by_gradient(BLUE, YELLOW, RED)
        bars.set_stroke(WHITE, 1)
        return bars

    def get_relative_proportion_map(self, all_scores):
        scores = set(all_scores)
        n_scores = len(all_scores)
        return dict([
            (s, np.sum(all_scores == s) / n_scores)
            for s in set(scores)
        ])

    def set_histogram_bars(self, bars, scores, axes):
        prop_map = self.get_relative_proportion_map(scores)
        epsilon = 1e-6
        for bar in bars:
            prop = prop_map.get(bar.x, epsilon)
            bar.set_height(
                prop * axes.y_axis.unit_size * 100,
                stretch=True,
                about_edge=DOWN,
            )

    def get_random_score(self):
        score = 1
        radius = 1
        while True:
            point = np.random.uniform(-1, 1, size=2)
            hit_radius = get_norm(point)
            if hit_radius > radius:
                return score
            else:
                score += 1
                radius = np.sqrt(radius**2 - hit_radius**2)


class SubtractHistogramParts(ShowDistributionOfScores):
    def construct(self):
        n_scores = 10000
        scores = np.array([self.get_random_score() for x in range(n_scores)])
        axes = self.get_axes()
        bars = self.get_histogram_bars(axes)
        self.set_histogram_bars(bars, scores, axes)

        self.add(axes)
        self.add(bars)

        # P(S = 2)
        p2_arrow = Vector(
            0.75 * DOWN,
            max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.35,
        )
        p2_arrow.next_to(bars[1], UP, SMALL_BUFF)
        p2_arrow = VGroup(
            p2_arrow.copy().set_stroke(BLACK, 9),
            p2_arrow,
        )

        p2_label = OldTex("P(S = 2)")
        p2_label.next_to(p2_arrow, UP, SMALL_BUFF)
        p2_label.set_color(bars[1].get_fill_color())

        self.play(
            GrowFromPoint(p2_arrow, p2_arrow.get_top()),
            FadeInFromDown(p2_label),
            bars[0].set_opacity, 0.1,
            bars[2:].set_opacity, 0.1,
        )
        self.wait()

        # Culumative probabilities
        rhs = OldTex("=", "P(S > 1)", "-", "P(S > 2)")
        rhs[1].set_color(YELLOW)
        rhs[3].set_color(bars[2].get_fill_color())
        rhs[2:].set_opacity(0.2)
        rhs.next_to(p2_label, RIGHT)

        # CHANGE: GL's Brace already exposes the pieces directly; do not take only the first stroke.
        brace1 = Brace(bars[1:5], UP)
        brace1.next_to(rhs[1], DOWN)
        brace1.match_color(rhs[1])

        rf = 3.5
        lf = 1.4
        brace1[:2].stretch(rf, 0, about_edge=LEFT)
        brace1[0].stretch(1 / rf, 0, about_edge=LEFT)
        brace1[4:].stretch(lf, 0, about_edge=RIGHT)
        brace1[5:].stretch(1 / lf, 0, about_edge=RIGHT)

        brace2 = Brace(bars[2:], UP)
        brace2.match_color(rhs[3])
        brace2.set_width(10, about_edge=LEFT)
        brace2.shift(1.5 * UP)

        self.add(brace1, p2_arrow)
        self.play(
            FadeIn(rhs),
            bars[2:].set_opacity, 1,
            GrowFromPoint(brace1, rhs[1].get_bottom()),
            p2_arrow.set_opacity, 0.5,
        )
        self.wait()
        self.play(
            rhs[:2].set_opacity, 0.2,
            brace1.set_opacity, 0.2,
            rhs[2:].set_opacity, 1,
            bars[1].set_opacity, 0.1,
            GrowFromCenter(brace2),
        )
        self.wait()

        self.play(
            bars[2:].set_opacity, 0.1,
            bars[1].set_opacity, 1,
            rhs.set_opacity, 1,
            brace1.set_opacity, 1,
            p2_arrow.set_opacity, 1,
        )
        self.wait()
