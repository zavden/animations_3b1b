# ==============================================================================
# Scene:      GraphicalIntuitions
# Source:     videos/_2018/alt_calc.py (lines 789-864)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GraphicalIntuitions.py GraphicalIntuitions -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class GraphicalIntuitions(GraphScene):
    CONFIG = {
        "func": lambda x: 0.1 * (x - 2) * (x - 5) * (x - 7) + 4,
        "x_labeled_nums": list(range(1, 10)),
    }

    def construct(self):
        self.setup_axes()
        axes = self.axes
        graph = self.get_graph(self.func)

        ss_group = self.get_secant_slope_group(
            x=8, graph=graph, dx=0.01,
            secant_line_length=6,
            secant_line_color=RED,
        )
        rects = self.get_riemann_rectangles(
            graph, x_min=2, x_max=8, dx=0.01, stroke_width=0
        )

        deriv_text = OldTexText(
            "Derivative $\\rightarrow$ slope",
            tex_to_color_map={"slope": ss_group.secant_line.get_color()}
        )
        deriv_text.to_edge(UP)
        integral_text = OldTexText(
            "Integral $\\rightarrow$ area",
            tex_to_color_map={"area": rects[0].get_color()}
        )
        integral_text.next_to(deriv_text, DOWN)

        self.play(
            Succession(Write(axes), ShowCreation(graph, run_time=2)),
            self.get_graph_words_anim(),
        )
        self.animate_secant_slope_group_change(
            ss_group,
            target_x=2,
            rate_func=smooth,
            run_time=2.5,
            added_anims=[
                Write(deriv_text),
                VFadeIn(ss_group, run_time=2),
            ]
        )
        self.play(FadeIn(integral_text))
        self.play(
            LaggedStartMap(
                GrowFromEdge, rects,
                lambda r: (r, DOWN)
            ),
            Animation(axes),
            Animation(graph),
        )
        self.wait()

    def get_graph_words_anim(self):
        words = VGroup(
            OldTexText("Graphs,"),
            OldTexText("graphs,"),
            OldTexText("non-stop graphs"),
            OldTexText("all day"),
            OldTexText("every day"),
            OldTexText("as if to visualize is to graph"),
        )
        for word in words:
            word.add_background_rectangle()
        words.arrange(DOWN)
        words.to_edge(UP)
        return LaggedStartMap(
            FadeIn, words,
            rate_func=there_and_back,
            run_time=len(words) - 1,
            lag_ratio=0.6,
            remover=True
        )
