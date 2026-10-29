# ==============================================================================
# Scene:      WideGraph
# Source:     videos/_2022/puzzles/subsets.py (lines 2043-2072)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WideGraph.py WideGraph -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - background_line_style without stroke_color raises KeyError (coordinate_systems.py:668, it is no longer merged with the default): stroke_color=BLUE_D is added
# ==============================================================================

from manim_imports_ext import *

class WideGraph(InteractiveScene):
    def construct(self):
        # Start
        def func(x, n=10):
            return np.product([1 + x**n for n in range(1, n + 1)])

        plane = NumberPlane(
            x_range=(-1, 1, 1),
            y_range=(0, 10, 1),
            width=FRAME_WIDTH - 1,
            height=6,
            # CHANGE: NumberPlane requires stroke_color in background_line_style (before it was merged with the default value BLUE_D)
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 1.5},
            faded_line_ratio=10,
        )
        plane.to_edge(DOWN)
        graph = plane.get_graph(func, (-1, 0.75))
        graph.set_stroke(YELLOW, 2)
        graph_label = OldTex("f(x)")
        graph_label.set_color(YELLOW)
        graph_label.next_to(plane.i2gp(0.73, graph), LEFT)
        graph_label.set_backstroke()

        x_tracker = ValueTracker(0.75)
        dot = GlowDot(color=WHITE)
        dot.add_updater(lambda d: d.move_to(plane.i2gp(x_tracker.get_value(), graph)))

        self.add(plane, graph, graph_label, dot)
        self.add(x_tracker)
        self.play(x_tracker.animate.set_value(0), run_time=3)
        self.wait()
