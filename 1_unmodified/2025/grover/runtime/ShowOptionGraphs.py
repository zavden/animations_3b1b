# ==============================================================================
# Scene:      ShowOptionGraphs
# Source:     videos/_2025/grover/runtime.py (lines 175-214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowOptionGraphs.py ShowOptionGraphs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowOptionGraphs(InteractiveScene):
    def construct(self):
        # Axes
        x_max = 15
        axes = Axes((-1, x_max), (-1, x_max))
        axes.set_height(7)
        self.add(axes)

        # Add graphs
        graphs = VGroup(
            axes.get_graph(func, x_range=(0.01, x_max))
            for func in [
                lambda n: n,
                lambda n: math.sqrt(n),
                lambda n: 0.8 * math.log(n + 1),
                lambda n: math.log(math.log(n + 1) + 1),
                lambda n: 1,
            ]
        )
        graphs.set_submobject_colors_by_gradient(YELLOW, ORANGE, RED, RED_E, BLUE)
        labels = VGroup(
            Tex(sym, font_size=30).match_color(graph).next_to(graph.get_end(), RIGHT, SMALL_BUFF)
            for graph, sym in zip(graphs, [
                R"\mathcal{O}\left(N\right)",
                R"\mathcal{O}\left(\sqrt{N}\right)",
                R"\mathcal{O}\left(\log(N)\right)",
                R"\mathcal{O}\left(\log(\log(N))\right)",
                R"\mathcal{O}\left(1\right)",
            ])
        )
        labels[-1].shift(2 * SMALL_BUFF * DOWN)

        for graph, label in zip(graphs, labels):
            vect = label.get_center() - graph.get_end()
            self.play(
                ShowCreation(graph),
                VFadeIn(label),
                UpdateFromFunc(label, lambda m: m.move_to(graph.get_end() + vect)),
            )
        self.wait()
