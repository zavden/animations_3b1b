# ==============================================================================
# Scene:      NotGraphsForProducts
# Source:     videos/_2017/eoc/chapter4.py (lines 713-762)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotGraphsForProducts.py NotGraphsForProducts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


PRODUCT_COLOR = YELLOW


class NotGraphsForProducts(GraphScene):
    CONFIG = {
        "y_max" : 25,
        "x_max" : 7,
    }
    def construct(self):
        self.setup_axes()
        sine_graph = self.get_graph(np.sin, color = SINE_COLOR)
        sine_graph.label = self.get_graph_label(
            sine_graph, "\\sin(x)",
            x_val = 3*np.pi/2,
            direction = DOWN
        )
        parabola = self.get_graph(
            lambda x : x**2, color = X_SQUARED_COLOR
        )
        parabola.label = self.get_graph_label(
            parabola, "x^2",
            x_val = 2.5,
            direction = UP+LEFT,
        )
        product_graph = self.get_graph(
            lambda x : np.sin(x)*(x**2), color = PRODUCT_COLOR
        )
        product_graph.label = self.get_graph_label(
            product_graph, "\\sin(x)x^2",
            x_val = 2.8,
            direction = UP+RIGHT,
            buff = 0
        )

        graphs = [sine_graph, parabola, product_graph]
        for graph in graphs:
            self.play(
                ShowCreation(graph),
                Write(graph.label, run_time = 2)
            )
        self.wait()

        everything = VGroup(*[m for m in self.get_mobjects() if not m.is_subpath])
        words = OldTexText("Not the best visualization")
        words.scale(1.5)
        words.shift(FRAME_Y_RADIUS*UP/2)
        words.add_background_rectangle()
        words.set_color(RED)
        self.play(
            everything.fade,
            Write(words)
        )
        self.wait()
