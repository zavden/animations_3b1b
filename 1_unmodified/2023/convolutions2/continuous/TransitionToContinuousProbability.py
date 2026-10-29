# ==============================================================================
# Scene:      TransitionToContinuousProbability
# Source:     videos/_2023/convolutions2/continuous.py (lines 35-231)
# Category:   1 · Renders unmodified
# Includes code copied from: _2022/convolutions/discrete.py
#
# Run from this folder:
#     manimgl TransitionToContinuousProbability.py TransitionToContinuousProbability -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2022/convolutions/discrete.py -----

def get_die_faces(**kwargs):
    result = VGroup(*(DieFace(n, **kwargs) for n in range(1, 7)))
    result.arrange(RIGHT, buff=MED_LARGE_BUFF)
    return result



# ----- From _2023/convolutions2/continuous.py -----

class TransitionToContinuousProbability(InteractiveScene):
    def construct(self):
        # Setup axes and initial graph
        axes = Axes((0, 12), (0, 1, 0.2), width=14, height=5)
        axes.to_edge(LEFT, LARGE_BUFF)
        axes.to_edge(DOWN, buff=1.25)

        def pd(x):
            return (x**4) * np.exp(-x) / 8.0

        graph = axes.get_graph(pd)
        graph.set_stroke(WHITE, 2)
        bars = axes.get_riemann_rectangles(graph, dx=1, x_range=(0, 6), input_sample_type="right")
        bars.set_stroke(WHITE, 3)

        y_label = Text("Probability", font_size=48)
        y_label.next_to(axes.y_axis, UP, SMALL_BUFF)
        y_label.shift_onto_screen()

        self.add(axes)
        self.add(y_label)
        self.add(*bars)

        self.frame.move_to(0.5 * DOWN)

        # Label as die probabilities
        dice = get_die_faces(fill_color=BLUE_E, dot_color=WHITE, stroke_width=1)
        dice.set_height(0.5)
        for bar, die in zip(bars, dice):
            die.next_to(bar, DOWN)

        self.play(FadeIn(dice, 0.1 * UP, lag_ratio=0.05, rate_func=overshoot))
        self.wait()
        self.play(FadeOut(dice, RIGHT, rate_func=running_start, run_time=1, path_arc=-PI / 5, lag_ratio=0.01))

        # Make continuous
        all_rects = VGroup(*(
            axes.get_riemann_rectangles(
                graph,
                x_range=(0, min(6 + n, 12)),
                dx=(1 / n),
                input_sample_type="right",
            ).set_stroke(WHITE, width=(2.0 / n), opacity=(2.0 / n), behind=False)
            for n in (*range(1, 10), *range(10, 20, 2), *range(20, 100, 5))
        ))
        area = all_rects[-1]
        area.set_stroke(width=0)

        self.remove(bars)
        self.play(
            ShowSubmobjectsOneByOne(all_rects, rate_func=bezier([0, 0, 0, 0, 1, 1])),
            FadeOut(y_label),
            run_time=5
        )
        self.remove(all_rects)
        self.add(area, graph)
        self.play(ShowCreation(graph))
        self.wait()

        # Show continuous value
        x_tracker = ValueTracker(0)
        get_x = x_tracker.get_value
        tip = ArrowTip(angle=PI / 2)
        tip.set_height(0.25)
        tip.add_updater(lambda m: m.move_to(axes.c2p(get_x(), 0), UP))
        x_label = DecimalNumber(font_size=36)
        x_label.add_updater(lambda m: m.set_value(get_x()))
        x_label.add_updater(lambda m: m.next_to(tip, DOWN, buff=0.2))

        self.play(FadeIn(tip), FadeIn(x_label))
        self.play(x_tracker.animate.set_value(12), run_time=6)

        # Labels
        x_labels = VGroup(*(
            Text(text)
            for text in [
                "Temperature tomorrow at noon",
                "Value of XYZ next year",
                "Time before the next bus comes",
            ]
        ))
        for x_label in x_labels:
            x_label.next_to(axes.c2p(4, 0), DOWN, buff=0.2)

        self.play(Write(x_labels[0], run_time=1))
        for xl1, xl2 in zip(x_labels, x_labels[1:]):
            self.wait()
            self.play(
                FadeOut(xl1, 0.5 * UP),
                FadeIn(xl2, 0.5 * UP),
            )
        self.wait()
        self.play(
            FadeOut(x_labels[-1]),
            x_tracker.animate.set_value(0).set_anim_args(run_time=3),
        )
        self.play(
            x_tracker.animate.set_value(12), run_time=5
        )
        self.remove(tip, x_label)

        # Label density
        density = Text("Probability density")
        density.match_height(y_label)
        density.move_to(y_label, LEFT)
        cross = Cross(y_label)
        cross.set_stroke(RED, width=(0, 8, 8, 8, 0))

        self.play(FadeIn(y_label))
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            VGroup(y_label, cross).animate.shift(0.75 * UP),
            FadeIn(density),
            self.frame.animate.set_y(0),
        )
        self.wait()

        # Interpretation
        range_tracker = ValueTracker([0, 12])
        sub_area_opacity_tracker = ValueTracker(0)

        def get_subarea():
            result = axes.get_area_under_graph(
                graph, range_tracker.get_value()
            )
            result.set_stroke(width=0)
            result.set_fill(TEAL, sub_area_opacity_tracker.get_value())
            return result

        sub_area = always_redraw(get_subarea)

        v_lines = Line(DOWN, UP).replicate(2)
        v_lines.set_stroke(GREY_A, 1)
        v_lines.set_height(FRAME_HEIGHT)

        def update_v_lines(v_lines):
            values = range_tracker.get_value()
            for value, line in zip(values, v_lines):
                line.move_to(axes.c2p(value, 0), DOWN)

        v_lines.add_updater(update_v_lines)

        bound_labels = Tex("ab")
        bound_labels[0].add_updater(lambda m: m.move_to(v_lines[0], DOWN).shift(0.5 * DOWN))
        bound_labels[1].add_updater(lambda m: m.move_to(v_lines[1], DOWN).shift(0.5 * DOWN))
        bound_labels.add_updater(lambda m: m.set_opacity(sub_area_opacity_tracker.get_value()))

        prob_label = Tex(R"P(a < x < b) = \text{This area}")
        prob_label.move_to(2 * UR)
        rhs = prob_label[R"\text{This area}"]
        prob_arrow = Arrow(LEFT, RIGHT)
        prob_arrow.add_updater(lambda m: m.put_start_and_end_on(
            rhs.get_bottom() + 0.1 * DOWN,
            sub_area.get_center(),
        ))

        self.add(area, sub_area, graph, bound_labels)
        self.play(
            area.animate.set_opacity(0.1),
            range_tracker.animate.set_value([3, 4.5]),
            sub_area_opacity_tracker.animate.set_value(1),
            VFadeIn(v_lines),
            FadeIn(prob_label),
            VFadeIn(prob_arrow),
            run_time=2,
        )
        self.wait()
        for pair in [(5, 6), (1, 3), (2.5, 3), (4, 7)]:
            self.play(range_tracker.animate.set_value(pair), run_time=2)
            self.wait()

        # Name the pdf
        long_name = Text("probability\ndensity\nfunction", alignment="LEFT")
        short_name = Text("pdf")
        long_name.move_to(axes.c2p(1, 0.75), UL)
        short_name.move_to(axes.c2p(2, 0.5))

        self.play(FadeIn(long_name, lag_ratio=0.1))
        self.wait()
        self.play(TransformMatchingStrings(long_name, short_name, lag_ratio=0.01, run_time=1))
        self.wait()

        # Show integral
        int_rhs = Tex(R"\int_a^b p_X(x) \, dx")
        int_rhs.move_to(rhs, LEFT)

        self.play(
            rhs.animate.set_opacity(0).shift(0.5 * DOWN + 1.0 * LEFT),
            FadeIn(int_rhs, DL)
        )
        self.wait()

        # Ambient range changing
        for pair in [(2.5, 7), (8, 10), (3.5, 9), (3, 4.5)]:
            self.play(range_tracker.animate.set_value(pair), run_time=3)
            self.wait()
