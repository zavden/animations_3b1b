# ==============================================================================
# Scene:      LogBases
# Source:     videos/_2026/cross_entropy/robot.py (lines 8764-8799)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LogBases.py LogBases -w -m --fps 15
# ==============================================================================

from __future__ import annotations
import math
from manim_imports_ext import *

class LogBases(InteractiveScene):
    def construct(self):
        # Create two graphs
        axes_1 = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 5, 1],
            width=4,
            height=6,
            x_axis_config={"include_numbers": True, "numbers_to_exclude": [0.1 * i for i in range(1, 10)]}
        )
        axes_2 = Axes(
            x_range=[0, 1, 0.1],
            y_range=[0, 5, 1],
            width=4,
            height=6,
            x_axis_config={"include_numbers": True, "numbers_to_exclude": [0.1 * i for i in range(1, 10)]}
        )
        VGroup(axes_1, axes_2).arrange(buff=2.2).to_edge(DOWN, buff=1)
        self.add(axes_1, axes_2)

        graph_1 = axes_1.get_graph(lambda q: -math.log(q), x_range=[0.0001, 1, 0.001]).insert_n_curves(1000).set_color(TEAL_A)
        q_label_1 = Tex("q", font_size=32).next_to(axes_1.get_x_axis(), RIGHT)
        f_of_q_label_1 = Tex(R"-\ln q", font_size=32).next_to(axes_1.get_y_axis(), LEFT).set_color(TEAL_A)

        graph_2 = axes_2.get_graph(lambda q: -math.log2(q), x_range=[0.0001, 1, 0.001]).insert_n_curves(1000).set_color(TEAL_C)
        q_label_2 = q_label_1.copy().next_to(axes_2.get_x_axis(), RIGHT)
        f_of_q_label_2 = Tex(R"-\log_2 q", font_size=32).next_to(axes_2.get_y_axis(), LEFT).set_color(TEAL_C)

        self.play(
            ShowCreation(graph_1, run_time=3),
            Write(q_label_1),
            Write(f_of_q_label_1),
            ShowCreation(graph_2, run_time=3),
            Write(q_label_2),
            Write(f_of_q_label_2)
        )
