# ==============================================================================
# Scene:      ShowUncertaintyPrinciple
# Source:     videos/_2018/fourier.py (lines 3963-4022)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowUncertaintyPrinciple.py ShowUncertaintyPrinciple -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowUncertaintyPrinciple(Scene):
    def construct(self):
        title = OldTexText("Uncertainty principle")
        self.add(title)
        top_axes = Axes(
            x_min = -FRAME_X_RADIUS,
            x_max = FRAME_X_RADIUS,
            y_min = 0,
            y_max = 3,
            y_axis_config = {
                "unit_size" : 0.6,
                "include_tip" : False,
            }
        )
        bottom_axes = top_axes.deepcopy()
        arrow = Vector(DOWN, color = WHITE)
        group = VGroup(
            title, top_axes, arrow, bottom_axes
        )
        group.arrange(DOWN)
        title.shift(MED_SMALL_BUFF*UP)
        group.to_edge(UP)
        fourier_word = OldTexText("Fourier transform")
        fourier_word.next_to(arrow, RIGHT)
        self.add(group, fourier_word)

        ghost_dot = Dot(RIGHT, fill_opacity = 0)
        def get_bell_func(factor = 1):
            return lambda x : 2*np.exp(-factor*x**2)
        top_graph = top_axes.get_graph(get_bell_func())
        top_graph.set_color(YELLOW)
        bottom_graph = bottom_axes.get_graph(get_bell_func())
        bottom_graph.set_color(RED)
        def get_update_func(axes):
            def update_graph(graph):
                f = ghost_dot.get_center()[0]
                if axes == bottom_axes:
                    f = 1./f
                new_graph = axes.get_graph(get_bell_func(f))
                graph.set_points(new_graph.get_points())
            return update_graph

        factors = [0.3, 0.1, 2, 10, 100, 0.01, 0.5]

        self.play(ShowCreation(top_graph))
        self.play(ReplacementTransform(
            top_graph.copy(),
            bottom_graph,
        ))
        self.wait(2)
        self.add(*[
            Mobject.add_updater(graph, get_update_func(axes))
            for graph, axes in [(top_graph, top_axes), (bottom_graph, bottom_axes)]
        ])
        for factor in factors:
            self.play(
                ghost_dot.move_to, factor*RIGHT,
                run_time = 2
            )
            self.wait()
