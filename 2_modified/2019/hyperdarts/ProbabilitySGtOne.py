# ==============================================================================
# Scene:      ProbabilitySGtOne
# Source:     videos/_2019/hyperdarts.py (lines 2076-2207)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ProbabilitySGtOne.py ProbabilitySGtOne -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Index new_brace[2] directly; in GL Cairo's outer layer does not exist.
#   - GL's Brace is a flat list of pieces (in Cairo brace[0] was the group): brace[:2] and final_brace[2].
# ==============================================================================

# CHANGE: index the pieces of Brace directly, without Cairo's extra layer.
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


class HistogramScene(ShowDistributionOfScores):
    CONFIG = {
        "n_scores": 10000,
        "mean_line_height": 4,
    }

    def setup(self):
        self.scores = np.array([
            self.get_random_score()
            for x in range(self.n_scores)
        ])
        self.axes = self.get_axes()
        self.bars = self.get_histogram_bars(self.axes)
        self.set_histogram_bars(self.bars, self.scores, self.axes)

        self.add(self.axes)
        self.add(self.bars)

    def get_mean_label(self):
        mean_line = DashedLine(ORIGIN, self.mean_line_height * UP)
        mean_line.set_stroke(YELLOW, 2)

        mean = np.mean(self.scores)
        mean_line.move_to(self.axes.c2p(mean, 0), DOWN)
        mean_label = VGroup(
            *TexText("E[S]", "="),
            DecimalNumber(mean, num_decimal_places=3),
        )
        mean_label.arrange(RIGHT)
        mean_label.match_color(mean_line)
        mean_label.next_to(
            mean_line.get_end(), UP, SMALL_BUFF,
            index_of_submobject_to_align=0,
        )

        return VGroup(mean_line, *mean_label)


class ProbabilitySGtOne(HistogramScene):
    def construct(self):
        axes = self.axes
        bars = self.bars

        brace = Brace(bars[1:], UP)
        label = brace.get_tex("P(S > 1)")
        # CHANGE: GL's Brace is a flat list of pieces (in Cairo, brace[0] was the group of pieces)
        brace[:2].stretch(1.5, 0, about_edge=LEFT)

        outlines = bars[1:].copy()
        for bar in outlines:
            bar.set_stroke(bar.get_fill_color(), 2)
            bar.set_fill(opacity=0)

        self.play(
            GrowFromEdge(brace, LEFT),
            bars[0].set_opacity, 0.2,
            bars[1:].set_opacity, 0.8,
            ShowCreationThenFadeOut(outlines),
            FadeIn(label, LEFT),
        )
        self.wait()

        square = Square()
        square.set_fill(BLUE, 0.75)
        square.set_stroke(WHITE, 1)
        square.set_height(0.5)

        circle = Circle()
        circle.set_fill(RED, 0.75)
        circle.set_stroke(WHITE, 1)
        circle.set_height(0.5)

        bar = Line(LEFT, RIGHT)
        bar.set_stroke(WHITE, 3)
        bar.set_width(0.5)

        geo_frac = VGroup(circle, bar, square)
        geo_frac.arrange(DOWN, SMALL_BUFF, buff=SMALL_BUFF)

        rhs = VGroup(
            OldTex("="),
            geo_frac,
            OldTex("= \\frac{\\pi}{4}")
        )
        rhs.arrange(RIGHT)
        rhs.next_to(label)

        shift_val = 2.05 * LEFT + 0.25 * UP
        rhs.shift(shift_val)

        self.play(
            label.shift, shift_val,
            FadeIn(rhs, LEFT)
        )
        self.wait()

        # P(S > 2)
        new_brace = brace.copy()
        new_brace.next_to(
            bars[2], UP,
            buff=SMALL_BUFF,
            aligned_edge=LEFT,
        )
        self.add(new_brace)

        new_label = OldTex(
            "P(S > 2)", "=", "\\,???"
        )
        new_label.next_to(new_brace[2], UP)

        self.play(
            bars[1].set_opacity, 0.2,
            label.set_opacity, 0.5,
            rhs.set_opacity, 0.5,
            brace.set_opacity, 0.5,
            GrowFromEdge(new_brace, LEFT),
            ReplacementTransform(
                new_label.copy().fade(1).move_to(label, LEFT),
                new_label,
            )
        )
        self.wait()

        new_rhs = OldTex(
            "{\\text{4d ball}", " \\over", " \\text{4d cube}}",
            # "=",
            # "{\\pi^2 / 2", "\\over", "2^4}"
        )
        new_rhs[0].set_color(RED)
        new_rhs[2].set_color(BLUE)
        new_rhs.move_to(new_label[-1], LEFT)
        shift_val = 0.75 * LEFT + 0.15 * UP

        new_rhs.shift(shift_val)

        new_label.generate_target()
        new_label.target.shift(shift_val)
        new_label.target[-1].set_opacity(0)

        self.play(
            MoveToTarget(new_label),
            FadeIn(new_rhs, LEFT)
        )
        self.wait()

        # P(S > 3)
        final_brace = brace.copy()
        final_brace.set_opacity(1)
        final_brace.next_to(
            bars[3], UP,
            buff=SMALL_BUFF,
            aligned_edge=LEFT,
        )
        self.add(final_brace)

        final_label = OldTex("P(S > 3)")
        # CHANGE: as above, the tip of GL's Brace is final_brace[2]
        final_label.next_to(final_brace[2], UP, SMALL_BUFF)

        self.play(
            bars[2].set_opacity, 0.2,
            new_label[:-1].set_opacity, 0.5,
            new_rhs.set_opacity, 0.5,
            new_brace.set_opacity, 0.5,
            GrowFromEdge(final_brace, LEFT),
            ReplacementTransform(
                final_label.copy().fade(1).move_to(new_label, LEFT),
                final_label,
            ),
            axes.x_axis[-1].set_opacity, 0,
        )
        self.wait()
