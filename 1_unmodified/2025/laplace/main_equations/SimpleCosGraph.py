# ==============================================================================
# Scene:      SimpleCosGraph
# Source:     videos/_2025/laplace/main_equations.py (lines 22-71)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleCosGraph.py SimpleCosGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleCosGraph(InteractiveScene):
    rotation_frequency = TAU / 4

    def construct(self):
        # Show graph
        def get_t():
            return self.time

        t_max = 20
        axes = Axes((0, t_max), (-1, 1), x_axis_config=dict(unit_size=0.6))
        axes.scale(1.25).to_edge(LEFT)

        x_axis = axes.x_axis

        x_axis.add(VGroup(
            Tex(tex, font_size=20).next_to(x_axis.n2p(n), DOWN)
            for n, tex in zip(it.count(1, 2), self.get_pi_frac_texs())
        ))

        def cos_func(t):
            return np.cos(self.rotation_frequency * t)

        graph = axes.get_graph(cos_func)
        graph.set_stroke(TEAL, 3)
        graph_ghost = graph.copy()
        graph_ghost.set_stroke(opacity=0.5)
        shown_graph = graph.copy()
        shown_graph.add_updater(lambda m: m.pointwise_become_partial(graph, 0, get_t() / t_max))

        output_dot = Group(TrueDot(), GlowDot()).set_color(YELLOW)
        output_dot.add_updater(lambda m: m.move_to(axes.y_axis.n2p(cos_func(get_t()))))

        h_line = Line()
        h_line.set_stroke(WHITE, 1)
        h_line.f_always.put_start_and_end_on(output_dot.get_center, shown_graph.get_end)

        cos_label = Tex(R"\cos(t)", font_size=60)
        cos_label.to_edge(UP)

        self.add(axes, graph_ghost, output_dot, shown_graph, h_line)
        self.wait(10)
        self.play(FadeOut(x_axis))
        self.wait(14)

    def get_pi_frac_texs(self):
        return [
            R"\pi / 2", R"\pi", R"3 \pi / 2", R"2\pi",
            R"5\pi / 2", R"3\pi", R"7 \pi / 2", R"4\pi",
            R"9\pi / 2", R"5\pi",
        ]
