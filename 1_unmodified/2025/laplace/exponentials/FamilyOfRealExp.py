# ==============================================================================
# Scene:      FamilyOfRealExp
# Source:     videos/_2025/laplace/exponentials.py (lines 1092-1115)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FamilyOfRealExp.py FamilyOfRealExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FamilyOfRealExp(InteractiveScene):
    def construct(self):
        # Graphs
        axes = Axes((-1, 8), (-1, 5))
        axes.set_height(FRAME_HEIGHT - 1)

        s_tracker = ValueTracker(0.5)
        get_s = s_tracker.get_value
        graph = axes.get_graph(lambda t: np.exp(t))
        graph.set_stroke(BLUE)
        axes.bind_graph_to_func(graph, lambda t: np.exp(get_s() * t))

        label = Tex(R"e^{st}", font_size=90)
        label.move_to(UP)
        label["s"].set_color(YELLOW)

        self.add(axes, label)
        self.play(ShowCreation(graph, suspend_mobject_updating=True))
        self.play(
            s_tracker.animate.set_value(-1),
            graph.animate.set_color(YELLOW),
            run_time=4
        )
        self.wait()
