# ==============================================================================
# Scene:      PreviewThreeExamples
# Source:     videos/_2022/visual_proofs/lies.py (lines 71-112)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewThreeExamples.py PreviewThreeExamples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewThreeExamples(InteractiveScene):
    def construct(self):
        # Setup
        self.add(FullScreenRectangle())
        rects = Rectangle(3.5, 4.5).replicate(3)
        rects.set_stroke(WHITE, 2)
        rects.set_fill(BLACK, 1)
        rects.arrange(RIGHT, buff=0.75)
        rects.to_edge(DOWN, buff=0.25)

        # Titles
        titles = VGroup(
            OldTexText("S.A. = $\\pi^2 R^2$"),
            OldTex("\\pi = 4").scale(1.5),
            Text("All triangles\nare isosceles"),
        )
        titles.set_width(rects[0].get_width())
        for title, rect in zip(titles, rects):
            title.next_to(rect, UP)

        self.play(
            LaggedStartMap(DrawBorderThenFill, rects, lag_ratio=0.3),
            LaggedStartMap(FadeIn, titles, shift=0.25 * UP, lag_ratio=0.3),
        )
        self.wait()

        # Increasing subtlety
        arrow = Arrow(LEFT, RIGHT, stroke_width=10)
        arrow.set_width(FRAME_WIDTH - 1)
        arrow.next_to(titles, UP)
        arrow.set_stroke(opacity=(0.5, 0.9, 1))
        words = Text("Increasingly subtle", font_size=72, color=YELLOW)
        words.next_to(arrow, UP)
        VGroup(arrow, words).to_edge(UP)
        arrow.set_x(0)
        arrow.set_color(YELLOW)

        self.play(
            ShowCreation(arrow),
            FadeIn(words, lag_ratio=0.1),
        )
        self.wait()
