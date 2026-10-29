# ==============================================================================
# Scene:      HarmonicSum
# Source:     videos/_2020/ldm.py (lines 934-986)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HarmonicSum.py HarmonicSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HarmonicSum(Scene):
    def construct(self):
        axes = Axes(
            x_min=0,
            x_max=13,
            y_min=0,
            y_max=1.25,
            y_axis_config={
                "unit_size": 4,
                "tick_frequency": 0.25,
            }
        )
        axes.to_corner(DL, buff=1)
        axes.x_axis.add_numbers()
        axes.y_axis.add_numbers(
            *np.arange(0.25, 1.25, 0.25),
            num_decimal_places=2,
        )
        self.add(axes)

        graph = axes.get_graph(lambda x: 1 / x, x_min=0.1, x_max=15)
        graph_fill = graph.copy()
        graph_fill.add_line_to(axes.c2p(15, 0))
        graph_fill.add_line_to(axes.c2p(1, 0))
        graph_fill.add_line_to(axes.c2p(1, 1))
        graph.set_stroke(WHITE, 3)
        graph_fill.set_fill(BLUE_E, 0.5)
        graph_fill.set_stroke(width=0)
        self.add(graph, graph_fill)

        bars = VGroup()
        bar_labels = VGroup()
        for x in range(1, 15):
            line = Line(axes.c2p(x, 0), axes.c2p(x + 1, 1 / x))
            bar = Rectangle()
            bar.set_fill(GREEN_E, 1)
            bar.replace(line, stretch=True)
            bars.add(bar)

            label = OldTex(f"1 \\over {x}")
            label.set_height(0.7)
            label.next_to(bar, UP, SMALL_BUFF)
            bar_labels.add(label)

        bars.set_submobject_colors_by_gradient(GREEN_C, GREEN_E)
        bars.set_stroke(WHITE, 1)
        bars.set_fill(opacity=0.25)

        self.add(bars)
        self.add(bar_labels)


        self.embed()
