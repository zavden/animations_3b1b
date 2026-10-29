# ==============================================================================
# Scene:      ThreeFoldRelationship
# Source:     videos/_2026/cross_entropy/supplements.py (lines 415-465)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeFoldRelationship.py ThreeFoldRelationship -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeFoldRelationship(InteractiveScene):
    def construct(self):
        # Set up
        tri = Triangle(start_angle=0)
        tri.set_height(4)

        radius = 1.7
        circles = Circle(radius=1.7).replicate(3)
        circles.set_stroke(WHITE, 2)
        circles[:2].arrange(DOWN, buff=LARGE_BUFF)
        circles[2].next_to(circles[:2], RIGHT, buff=1.5)
        circles.center()

        lines = VGroup(
            Line(c1.get_center(), c2.get_center(), buff=radius + SMALL_BUFF)
            for c1, c2 in it.combinations(circles, 2)
        )
        arrows = VGroup(
            Tex(R"\Leftrightarrow"),
            Tex(R"\longleftrightarrow"),
            Tex(R"\longleftrightarrow"),
        )
        for arrow, line in zip(arrows, lines):
            arrow.scale(1.5)
            arrow.rotate(line.get_angle())
            arrow.move_to(line)

        labels = VGroup(
            Text("Prediction").set_color("#951FF5"),
            Text("Compression").set_color(TEAL),
            Text("Intelligence").set_color(YELLOW),
        )
        for label, circle, vect in zip(labels, circles, [LEFT, LEFT, RIGHT]):
            label.next_to(circle, vect, buff=0.2)

        self.add(circles)
        self.play(LaggedStartMap(FadeIn, arrows, scale=10, lag_ratio=0.5))
        self.wait()
        self.play(LaggedStartMap(Write, labels, lag_ratio=0.5, run_time=3))
        self.wait()

        # Transition to AI
        ai = Text("Artificial\nIntelligence")
        ai.set_color(YELLOW_D)
        ai.move_to(labels[2], LEFT)

        self.play(
            ReplacementTransform(labels[2], ai["Intelligence"][0]),
            FadeIn(ai["Artificial"][0], lag_ratio=0.2, shift=0.1 * UP),
        )
        self.wait()
