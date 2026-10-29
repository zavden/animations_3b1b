# ==============================================================================
# Scene:      SimpleLineWithEndPoints
# Source:     videos/_2026/spheres_talk/volumes.py (lines 883-905)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleLineWithEndPoints.py SimpleLineWithEndPoints -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleLineWithEndPoints(InteractiveScene):
    def construct(self):
        # Test
        line = Line(LEFT, RIGHT)
        line.set_width(6)
        line.set_stroke(TEAL, 3)
        center_dot = Dot(ORIGIN, radius=0.05)

        brace = Brace(line, UP, buff=MED_SMALL_BUFF)
        brace.stretch(0.5, 0, about_edge=RIGHT)
        brace_label = brace.get_tex("r")

        end_points = Group(
            Group(Dot(), GlowDot()).move_to(point)
            for point in line.get_start_and_end()
        )
        end_points.set_color(YELLOW)

        self.add(line, center_dot)
        self.play(GrowFromCenter(brace), Write(brace_label))
        self.wait()
        self.play(FadeIn(end_points, lag_ratio=0.75))
        self.wait()
