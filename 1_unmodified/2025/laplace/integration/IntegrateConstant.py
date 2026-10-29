# ==============================================================================
# Scene:      IntegrateConstant
# Source:     videos/_2025/laplace/integration.py (lines 61-116)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntegrateConstant.py IntegrateConstant -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntegrateConstant(InteractiveScene):
    def construct(self):
        # Axes and graph
        axes = Axes((0, 100), (0, 2, 0.25), width=100, height=3)
        axes.add_coordinate_labels(num_decimal_places=2, font_size=20)
        axes.to_corner(DL)

        graph = axes.get_graph(lambda t: 1)
        graph.set_stroke(BLUE, 3)
        graph_label = Tex(R"f(t) = 1")
        graph_label.next_to(graph, UP)
        graph_label.to_edge(RIGHT)

        self.add(axes)
        self.add(graph, graph_label)

        # Integral
        t_tracker = ValueTracker(0.01)
        get_t = t_tracker.get_value

        v_tracker = ValueTracker(1)
        t_tracker.add_updater(lambda m, dt: m.increment_value(v_tracker.get_value() * dt))

        integral = Tex(R"\int^{0.01}_0 1 \, dt = 0.01", font_size=72)
        integral.to_edge(UP, buff=3.0)
        integral["1"].set_color(BLUE)
        decimals = integral.make_number_changeable("0.01", replace_all=True)
        decimals[0].scale(0.5, about_edge=LEFT)
        integral[2].scale(0.5, about_edge=LEFT)
        integral[:3].shift(0.5 * RIGHT)
        integral.set_scale_stroke_with_zoom(True)
        for dec in decimals:
            dec.add_updater(lambda m: m.set_value(get_t()))

        rect = Rectangle()
        rect.set_fill(BLUE, 0.5)
        rect.set_stroke(WHITE, 2)
        rect.set_z_index(-1)
        x_unit = axes.x_axis.get_unit_size()
        y_unit = axes.y_axis.get_unit_size()
        origin = axes.get_origin()
        rect.add_updater(
            lambda m: m.set_shape(get_t() * x_unit, y_unit).move_to(origin, DL)
        )

        integral.fix_in_frame()

        self.add(rect, integral, t_tracker)

        # Grow
        v_tracker.set_value(1)
        self.play(
            v_tracker.animate.set_value(12),
            self.frame.animate.reorient(0, 0, 0, (42.64, 14.41, 0.0), 58.35).set_anim_args(time_span=(6, 15)),
            run_time=20
        )
