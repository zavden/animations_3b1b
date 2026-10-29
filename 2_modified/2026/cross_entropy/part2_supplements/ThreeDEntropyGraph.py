# ==============================================================================
# Scene:      ThreeDEntropyGraph
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 280-371)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThreeDEntropyGraph.py ThreeDEntropyGraph -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed the call graph.sort_faces_back_to_front(DOWN): ParametricSurface no longer has it; this version of manimgl sorts the semi-transparent faces by itself (Surface.set_sort_to_camera).
# ==============================================================================

from manim_imports_ext import *

class ThreeDEntropyGraph(InteractiveScene):
    graph_resolution = (101, 101)

    def construct(self):
        # Test
        frame = self.frame
        epsilon = 1e-8
        axes = ThreeDAxes(
            (0, 1, 0.1), (0, 1, 0.1), (0, 5, 1),
            width=10,
            height=10,
            depth=10,
        )
        plane = NumberPlane((0, 1), (0, 1), width=10, height=10)
        plane.shift(axes.get_origin() - plane.get_origin())

        p_tracker = ValueTracker(np.array([0.1, 0.2, 0.7]))

        p_labels = VGroup(Tex(R"p_1"), Tex(R"p_2"))
        p_labels.rotate(90 * DEG, RIGHT)
        p_labels.scale(2)
        p_labels.set_color(GREEN)
        p_labels[0].next_to(axes.x_axis, RIGHT, SMALL_BUFF)
        p_labels[1].next_to(axes.y_axis.get_top(), LEFT, SMALL_BUFF)

        self.add(axes, plane, p_labels)

        # Add graph
        def ce_func(q1, q2):
            ps = p_tracker.get_value()
            qs = (q1, q2, 1 - q1 - q2)
            return sum([-p * np.log2(abs(q)) for p, q in zip(ps, qs)])

        def ent_func(p1, p2):
            # Do a check on domain?
            probs = (p1, p2, 1 - p1 - p2)
            return sum([-p * np.log2(abs(p)) for p in probs])

        ce_graph = always_redraw(lambda: self.get_simplex_graph(ce_func, axes, "#6B81FF"))
        ent_graph = self.get_simplex_graph(ent_func, axes, GREEN)

        frame.reorient(-30, 85, 0, (-3.28, 0.09, 2.49), 15.68)
        self.add(ent_graph)
        self.add(ce_graph)

        # Add line
        v_line = Line(IN, OUT)
        v_line.set_stroke(GREEN, 2)

        def update_line(line):
            x, y = p_tracker.get_value()[:2]
            z = ent_func(x, y)
            v_line.put_start_and_end_on(
                axes.c2p(x, y, 0),
                axes.c2p(x, y, z),
            )
            return v_line

        v_line.add_updater(update_line)
        dot = GlowDot().set_color(GREEN)
        dot.f_always.move_to(v_line.get_end)

        self.add(v_line)
        self.add(dot)

        # Animate
        self.play(
            frame.animate.reorient(34, 90, 0, (-3.28, 0.09, 2.49), 15.68),
            p_tracker.animate.set_value([0.7, 0.1, 0.2]),
            run_time=12
        )
        ce_graph.clear_updaters()

    def get_simplex_graph(self, func, axes, color, opacity=0.5, epsilon=1e-8):
        x_range = (epsilon, 1 - epsilon)
        matrix = np.array([
            axes.x_axis.n2p(1) - axes.x_axis.n2p(0),
            axes.y_axis.n2p(1) - axes.y_axis.n2p(0),
            axes.z_axis.n2p(1) - axes.z_axis.n2p(0),
        ]).T
        graph = ParametricSurface(
            lambda u, v: [u, (1 - u) * v, func(u, (1 - u) * v)],
            u_range=x_range,
            v_range=x_range,
            color=color,
            opacity=opacity,
            resolution=self.graph_resolution
        )
        graph.apply_matrix(matrix, about_point=ORIGIN)
        graph.shift(axes.c2p(0, 0, 0))
        # CHANGE: ParametricSurface no longer has sort_faces_back_to_front; this version of manimgl draws
        # semi-transparent surfaces back to front by itself (see Surface.set_sort_to_camera).
        return graph
