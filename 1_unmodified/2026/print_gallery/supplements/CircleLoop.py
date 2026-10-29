# ==============================================================================
# Scene:      CircleLoop
# Source:     videos/_2026/print_gallery/supplements.py (lines 733-750)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircleLoop.py CircleLoop -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircleLoop(InteractiveScene):
    def construct(self):
        # Test
        circle = Circle(radius=3)
        circle.set_stroke(RED, 8)
        circle.insert_n_curves(100)
        circle.flip(RIGHT)
        circle.rotate(5 * PI / 4)
        dot = GlowDot(color=RED)
        dot.move_to(circle.get_start())
        tail = TracingTail(dot, stroke_color=RED, time_traced=3, stroke_width=(0, 8))
        self.add(tail)
        self.play(FadeIn(dot))
        self.play(
            MoveAlongPath(dot, circle),
            run_time=8
        )
        self.wait(3)
