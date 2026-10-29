# ==============================================================================
# Scene:      WhyPiQuestion
# Source:     videos/_2023/clt/wordy_scenes.py (lines 751-779)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyPiQuestion.py WhyPiQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhyPiQuestion(InteractiveScene):
    def construct(self):
        # Axes
        axes = Axes((-3, 3), (0, 2, 0.5), width=10, height=5)
        axes.x_axis.add_numbers(font_size=16)
        axes.y_axis.add_numbers(num_decimal_places=1, font_size=16)
        graph = axes.get_graph(lambda x: math.exp(-x**2))
        graph.set_stroke(BLUE, 2)
        graph.set_fill(TEAL, 0.5)

        self.add(axes, graph)

        # Labels
        graph_label = Tex("e^{-x^2}", font_size=72)
        graph_label.next_to(graph.pfp(0.4), UL)
        self.add(graph_label)

        area_label = Tex(R"\text{Area} = \sqrt{\pi}")
        area_label.move_to(graph, UR)
        area_label.shift(UL)
        arrow = Arrow(area_label.get_bottom(), graph.get_center() + 0.5 * RIGHT)

        self.add(area_label, arrow)

        question = Text("But where's the circle?", font_size=30)
        question.set_color(YELLOW)
        question.next_to(area_label, DOWN)
        question.to_edge(RIGHT)
        self.add(question)
