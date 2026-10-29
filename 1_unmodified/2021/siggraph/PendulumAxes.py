# ==============================================================================
# Scene:      PendulumAxes
# Source:     videos/_2021/siggraph.py (lines 30-57)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PendulumAxes.py PendulumAxes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PendulumAxes(Scene):
    def construct(self):
        plane = NumberPlane(
            (-2, 2),
            (-2, 2),
            height=8,
            width=8,
            background_line_style={
                "stroke_color": WHITE,
            }
        )
        theta1 = OldTex("\\theta_1").next_to(plane.c2p(2, 0), RIGHT, SMALL_BUFF)
        theta2 = OldTex("\\theta_2").next_to(plane.c2p(0, 2), DR, SMALL_BUFF)
        labels = VGroup(theta1, theta2)

        x_labels = VGroup(OldTex("-\\pi"), OldTex("-{\\pi \\over 2}"), OldTex("{\\pi \\over 2}"), OldTex("\\pi"))
        y_labels = VGroup()
        for label, x in zip(x_labels, (-2, -1, 1, 2)):
            label.scale(0.5)
            label.set_stroke(BLACK, 5, background=True)
            label.next_to(plane.c2p(x, 0), DL, SMALL_BUFF)
            y_label = label.copy()
            y_label.next_to(plane.c2p(0, x), DL, SMALL_BUFF)
            y_labels.add(y_label)

        self.add(plane)
        self.add(labels)
        self.add(x_labels, y_labels)
