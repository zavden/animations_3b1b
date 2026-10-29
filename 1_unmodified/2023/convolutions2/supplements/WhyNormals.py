# ==============================================================================
# Scene:      WhyNormals
# Source:     videos/_2023/convolutions2/supplements.py (lines 489-540)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyNormals.py WhyNormals -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WhyNormals(InteractiveScene):
    def construct(self):
        # Add graph
        plane = NumberPlane(
            (-4, 4), (0, 0.75, 0.125),
            width=7, height=5,
            axis_config=dict(stroke_width=1),
            background_line_style=dict(stroke_color=GREY_B, stroke_width=1, stroke_opacity=0.5)
        )
        plane.to_edge(RIGHT)
        graph = plane.get_graph(lambda x: np.exp(-x**2 / 2) / math.sqrt(TAU))
        graph.set_stroke(BLUE, 3)

        formula = Tex(R"\frac{1}{\sqrt{2\pi}} e^{-x^2 / 2}")
        formula.next_to(graph.pfp(0.45), UL, buff=-0.25)
        formula.set_backstroke()
        name = Text("Standard normal distribution", font_size=48)
        name.next_to(plane.get_top(), DOWN, buff=0.2)
        name.set_backstroke()

        self.add(plane)
        self.add(graph)
        self.add(formula)
        self.add(name)

        # Ask question
        randy = Randolph(height=2)
        randy.move_to(interpolate(plane.get_left(), LEFT_SIDE, 0.75))
        randy.align_to(plane, DOWN)
        morty = Mortimer(height=2)
        morty.next_to(randy, RIGHT, buff=1.0)

        self.add(randy)
        self.play(LaggedStart(
            randy.thinks(
                Text("Why this\nfunction?", font_size=32),
                mode="pondering", look_at=formula, run_time=1
            ),
            FlashAround(formula, run_time=3, time_width=1.5)
        ))
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.debubble(mode="tease", look_at=morty.eyes),
            VFadeIn(morty),
            morty.says(
                Text("There's a very\nfun answer", font_size=32),
                look_at=randy.eyes,
                run_time=1
            ),
        )
        self.wait(4)
