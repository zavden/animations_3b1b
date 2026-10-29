# ==============================================================================
# Scene:      WaysToCombineFunctions
# Source:     videos/_2022/borwein/main.py (lines 1154-1215)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WaysToCombineFunctions.py WaysToCombineFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WaysToCombineFunctions(InteractiveScene):
    def construct(self):
        # Axes
        axes1, axes2, axes3 = all_axes = VGroup(*(
            Axes((-5, 5), (0, 2), width=FRAME_WIDTH - 2, height=FRAME_HEIGHT / 3 - 1.0)
            for x in range(3)
        ))
        all_axes.arrange(DOWN, buff=1.0)

        self.add(all_axes)

        # Functions
        def f(x):
            return np.sin(x) + 1

        def g(x):
            return np.exp(-x**2)

        f_graph = axes1.get_graph(f, color=BLUE)
        g_graph = axes2.get_graph(g, color=YELLOW)

        f_label = OldTex(R"f(x) = \sin(x) + 1", color=BLUE)[0]
        g_label = OldTex(R"g(x) = e^{-x^2}", color=YELLOW)[0]
        f_label.move_to(axes1.c2p(-1.5, 1.5))
        g_label.move_to(axes2.c2p(-1.5, 1.5))

        self.play(
            LaggedStart(FadeIn(f_graph), FadeIn(g_graph)),
            LaggedStart(FadeIn(f_label), FadeIn(g_label)),
        )
        self.wait()

        # Combinations
        sum_graph = axes3.get_graph(lambda x: f(x) + g(x), color=GREEN)
        prod_graph = axes3.get_graph(lambda x: f(x) * g(x), color=GREEN)
        dx = 0.1
        x_samples = np.arange(*axes1.x_range[:2], dx)
        conv_samples = np.convolve(f(x_samples), g(x_samples), mode="same") * dx * 0.5
        conv_graph = VMobject().set_points_smoothly(axes3.c2p(x_samples, conv_samples))
        conv_graph.match_style(prod_graph)
        graphs = (sum_graph, prod_graph, conv_graph)

        sum_label = OldTex("[f + g](x)")
        prod_label = OldTex(R"[f \cdot g](x)")
        conv_label = OldTex(R"[f * g](x)")
        labels = (sum_label, prod_label, conv_label)
        for label in labels:
            label.move_to(axes3.c2p(-1.5, 1.5))

        words = VGroup(*map(Text, ["Addition", "Multiplication", "Convolution"]))
        for word, label in zip(words, labels):
            word.next_to(label, UP)

        for graph, label, word in zip(graphs, labels, words):
            self.play(
                Transform(f_graph.copy(), graph.copy(), remover=True),
                TransformFromCopy(g_graph, graph),
                TransformMatchingShapes(VGroup(*f_label[:4], *g_label[:4]).copy(), label),
                FadeIn(word)
            )
            self.wait()
            self.play(*map(FadeOut, [graph, label, word]))
