# ==============================================================================
# Scene:      CirclesToPopulation
# Source:     videos/_2023/gauss_int/supplements.py (lines 147-171)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CirclesToPopulation.py CirclesToPopulation -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class CirclesToPopulation(InteractiveScene):
    def construct(self):
        # Show arrow
        circle = Circle(radius=1.5)
        circle.set_stroke(RED, 3)
        circle.set_fill(RED, 0.25)
        circle.to_corner(UL)

        screen = ScreenRectangle(height=5)
        screen.to_corner(DR)
        title = Text("Population statistics")
        title.next_to(screen, UP, SMALL_BUFF)

        arrow = Arrow(circle.get_right() + UP, title, path_arc=-0.5 * PI)
        q_marks = Text("???")
        q_marks.move_to(arrow)

        self.add(circle)
        self.play(
            ShowCreation(arrow),
            FadeIn(title, DR)
        )
        self.wait()
        self.play(Write(q_marks))
        self.wait()
